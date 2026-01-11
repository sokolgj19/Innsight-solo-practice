"""
Add sentiment analysis to all reviews in MongoDB
"""

import sys
sys.path.append('..')

from pymongo import MongoClient
from sentiment_analyzer import ReviewSentimentAnalyzer
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'innsight_db'
BATCH_SIZE = 1000  # Process 1000 reviews at a time


def add_sentiment_to_reviews(city: str = 'london'):
    """
    Add sentiment analysis to all reviews in the database.
    
    Args:
        city: City name to process
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"ADDING SENTIMENT TO {city.upper()} REVIEWS")
    logger.info(f"{'='*60}\n")
    
    # Connect to MongoDB
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[DB_NAME]
    reviews_collection = db['reviews']
    
    # Initialize sentiment analyzer
    analyzer = ReviewSentimentAnalyzer()
    
    # Get total count
    total_reviews = reviews_collection.count_documents({'city': city})
    logger.info(f"Total reviews in database: {total_reviews:,}")
    
    if total_reviews == 0:
        logger.error("❌ No reviews found! Check if data was loaded correctly.")
        client.close()
        return
    
    # Check how many already have sentiment
    with_sentiment = reviews_collection.count_documents({
        'city': city,
        'sentiment': {'$exists': True}
    })
    
    logger.info(f"Reviews with sentiment: {with_sentiment:,}")
    
    # Decide what to process
    if with_sentiment > 0:
        logger.info(f"\n⚠️  Found {with_sentiment:,} reviews already with sentiment")
        response = input("Re-process ALL reviews? (y/n): ").strip().lower()
        if response != 'y':
            logger.info("Processing only reviews without sentiment...")
            query = {'city': city, 'sentiment': {'$exists': False}}
        else:
            logger.info("Re-processing ALL reviews...")
            query = {'city': city}
    else:
        query = {'city': city}
    
    # Count reviews to process
    to_process = reviews_collection.count_documents(query)
    logger.info(f"\n🔄 Processing {to_process:,} reviews...\n")
    
    if to_process == 0:
        logger.info("✅ All reviews already have sentiment!")
        client.close()
        return
    
    # Process in batches
    processed = 0
    updated = 0
    errors = 0
    
    # Get cursor
    cursor = reviews_collection.find(query).batch_size(BATCH_SIZE)
    
    # Use tqdm for progress bar
    with tqdm(total=to_process, desc="Analyzing sentiment", unit="reviews") as pbar:
        batch = []
        
        for review in cursor:
            batch.append(review)
            
            # Process batch when it reaches BATCH_SIZE
            if len(batch) >= BATCH_SIZE:
                batch_updated, batch_errors = process_batch(batch, reviews_collection, analyzer)
                updated += batch_updated
                errors += batch_errors
                processed += len(batch)
                pbar.update(len(batch))
                batch = []
        
        # Process remaining reviews
        if batch:
            batch_updated, batch_errors = process_batch(batch, reviews_collection, analyzer)
            updated += batch_updated
            errors += batch_errors
            processed += len(batch)
            pbar.update(len(batch))
    
    logger.info(f"\n{'='*60}")
    logger.info(f"✅ SENTIMENT ANALYSIS COMPLETE")
    logger.info(f"{'='*60}")
    logger.info(f"Processed: {processed:,} reviews")
    logger.info(f"Updated: {updated:,} reviews")
    if errors > 0:
        logger.warning(f"Errors: {errors:,} reviews")
    
    # Get final statistics
    stats = get_sentiment_statistics(reviews_collection, city)
    print_statistics(stats)
    
    client.close()


def process_batch(batch, collection, analyzer):
    """Process a batch of reviews."""
    updated_count = 0
    error_count = 0
    
    for review in batch:
        try:
            comment = review.get('comments', '')
            
            if not comment or not isinstance(comment, str):
                continue
            
            # Analyze sentiment
            sentiment, score, scores = analyzer.analyze_review(comment)
            
            # Update document directly
            result = collection.update_one(
                {'_id': review['_id']},
                {'$set': {
                    'sentiment': sentiment,
                    'sentiment_score': round(score, 4),
                    'sentiment_scores': {
                        'positive': round(scores['pos'], 4),
                        'neutral': round(scores['neu'], 4),
                        'negative': round(scores['neg'], 4)
                    }
                }}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                
        except Exception as e:
            error_count += 1
            if error_count <= 5:  # Only log first 5 errors
                logger.error(f"Error processing review {review.get('id')}: {e}")
    
    return updated_count, error_count


def get_sentiment_statistics(collection, city):
    """Get sentiment statistics for a city."""
    pipeline = [
        {'$match': {'city': city, 'sentiment': {'$exists': True}}},
        {'$group': {
            '_id': '$sentiment',
            'count': {'$sum': 1},
            'avg_score': {'$avg': '$sentiment_score'}
        }}
    ]
    
    results = list(collection.aggregate(pipeline))
    
    stats = {
        'positive': 0,
        'negative': 0,
        'neutral': 0,
        'total': 0,
        'avg_scores': {}
    }
    
    for result in results:
        sentiment = result['_id']
        count = result['count']
        stats[sentiment] = count
        stats['total'] += count
        stats['avg_scores'][sentiment] = round(result['avg_score'], 3)
    
    return stats


def print_statistics(stats):
    """Print sentiment statistics."""
    total = stats['total']
    
    if total == 0:
        logger.warning("\n⚠️  No sentiment data found in database.")
        logger.warning("This might mean the updates didn't work.")
        return
    
    logger.info(f"\n📊 SENTIMENT STATISTICS:")
    logger.info(f"  Total reviews analyzed: {total:,}")
    logger.info(f"  ")
    logger.info(f"  Positive: {stats['positive']:,} ({stats['positive']/total*100:.1f}%)")
    logger.info(f"    Average score: {stats['avg_scores'].get('positive', 0):.3f}")
    logger.info(f"  ")
    logger.info(f"  Neutral: {stats['neutral']:,} ({stats['neutral']/total*100:.1f}%)")
    logger.info(f"    Average score: {stats['avg_scores'].get('neutral', 0):.3f}")
    logger.info(f"  ")
    logger.info(f"  Negative: {stats['negative']:,} ({stats['negative']/total*100:.1f}%)")
    logger.info(f"    Average score: {stats['avg_scores'].get('negative', 0):.3f}")


def main():
    """Run sentiment analysis from command line."""
    city = sys.argv[1] if len(sys.argv) > 1 else 'london'
    
    try:
        add_sentiment_to_reviews(city)
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()