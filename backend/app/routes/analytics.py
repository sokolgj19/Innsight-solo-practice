"""
Analytics API endpoints - Price stats, sentiment, occupancy, etc.
"""

from flask import Blueprint, jsonify, request
from ..database import get_db
from collections import Counter

bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


@bp.route('/<city>/price-stats')
def get_price_stats(city):
    """
    Get price statistics overall and by neighbourhood.
    """
    db = get_db()
    
    # Overall average price
    overall_pipeline = [
        {'$match': {'city': city, 'price': {'$exists': True, '$ne': None}}},
        {'$group': {
            '_id': None,
            'avg_price': {'$avg': '$price'},
            'min_price': {'$min': '$price'},
            'max_price': {'$max': '$price'},
            'count': {'$sum': 1}
        }}
    ]
    
    overall = list(db.listings.aggregate(overall_pipeline))
    
    # By neighbourhood
    by_neighbourhood_pipeline = [
        {'$match': {'city': city, 'price': {'$exists': True, '$ne': None}}},
        {'$group': {
            '_id': '$neighbourhood_cleansed',
            'avg_price': {'$avg': '$price'},
            'min_price': {'$min': '$price'},
            'max_price': {'$max': '$price'},
            'count': {'$sum': 1}
        }},
        {'$sort': {'avg_price': -1}}
    ]
    
    by_neighbourhood = list(db.listings.aggregate(by_neighbourhood_pipeline))
    
    return jsonify({
        'city': city,
        'overall': overall[0] if overall else {},
        'by_neighbourhood': by_neighbourhood
    })


@bp.route('/<city>/room-type-distribution')
def get_room_type_distribution(city):
    """
    Get distribution of room types.
    """
    db = get_db()
    
    pipeline = [
        {'$match': {'city': city}},
        {'$group': {
            '_id': '$room_type',
            'count': {'$sum': 1},
            'avg_price': {'$avg': '$price'}
        }},
        {'$sort': {'count': -1}}
    ]
    
    results = list(db.listings.aggregate(pipeline))
    
    total = sum(r['count'] for r in results)
    
    # Add percentages
    for r in results:
        r['percentage'] = round((r['count'] / total * 100), 1) if total > 0 else 0
    
    return jsonify({
        'city': city,
        'total_listings': total,
        'distribution': results
    })


@bp.route('/<city>/occupancy')
def get_occupancy_stats(city):
    """
    Get occupancy statistics from calendar data.
    Note: This endpoint might be slow if calendar data is large.
    """
    db = get_db()
    
    # Get occupancy by month
    pipeline = [
        {'$match': {'city': city}},
        {'$group': {
            '_id': {
                '$dateToString': {
                    'format': '%Y-%m',
                    'date': '$date'
                }
            },
            'total_days': {'$sum': 1},
            'booked_days': {
                '$sum': {
                    '$cond': [{'$eq': ['$available', False]}, 1, 0]
                }
            }
        }},
        {'$sort': {'_id': 1}},
        {'$limit': 12}  # Last 12 months
    ]
    
    results = list(db.calendar.aggregate(pipeline))
    
    # Calculate occupancy percentage
    for r in results:
        r['occupancy_rate'] = round((r['booked_days'] / r['total_days'] * 100), 1) if r['total_days'] > 0 else 0
    
    return jsonify({
        'city': city,
        'by_month': results
    })


@bp.route('/<city>/top-hosts')
def get_top_hosts(city):
    """
    Get top hosts by number of listings.
    """
    db = get_db()
    
    limit = request.args.get('limit', default=10, type=int)
    
    pipeline = [
        {'$match': {'city': city}},
        {'$group': {
            '_id': '$host_id',
            'host_name': {'$first': '$host_name'},
            'listing_count': {'$sum': 1},
            'avg_price': {'$avg': '$price'},
            'avg_rating': {'$avg': '$review_scores_rating'}
        }},
        {'$sort': {'listing_count': -1}},
        {'$limit': limit}
    ]
    
    results = list(db.listings.aggregate(pipeline))
    
    return jsonify({
        'city': city,
        'top_hosts': results
    })


@bp.route('/<city>/sentiment')
def get_sentiment_overall(city):
    """
    Get overall sentiment statistics for a city.
    """
    db = get_db()
    
    pipeline = [
        {'$match': {'city': city, 'sentiment': {'$exists': True}}},
        {'$group': {
            '_id': '$sentiment',
            'count': {'$sum': 1},
            'avg_score': {'$avg': '$sentiment_score'}
        }}
    ]
    
    results = list(db.reviews.aggregate(pipeline))
    
    sentiment_data = {
        'positive': {'count': 0, 'percentage': 0, 'avg_score': 0},
        'neutral': {'count': 0, 'percentage': 0, 'avg_score': 0},
        'negative': {'count': 0, 'percentage': 0, 'avg_score': 0}
    }
    
    total = sum(r['count'] for r in results)
    
    for r in results:
        sentiment = r['_id']
        count = r['count']
        sentiment_data[sentiment] = {
            'count': count,
            'percentage': round((count / total * 100), 1) if total > 0 else 0,
            'avg_score': round(r['avg_score'], 3)
        }
    
    return jsonify({
        'city': city,
        'total_reviews': total,
        'sentiment': sentiment_data
    })


@bp.route('/<city>/sentiment/by-neighbourhood')
def get_sentiment_by_neighbourhood(city):
    """
    Get sentiment breakdown by neighbourhood.
    """
    db = get_db()
    
    # First, get listing_id to neighbourhood mapping
    listing_neighbourhood_map = {}
    for listing in db.listings.find({'city': city}, {'id': 1, 'neighbourhood_cleansed': 1}):
        listing_neighbourhood_map[listing['id']] = listing.get('neighbourhood_cleansed')
    
    # Get all reviews with sentiment
    reviews = db.reviews.find(
        {'city': city, 'sentiment': {'$exists': True}},
        {'listing_id': 1, 'sentiment': 1, 'sentiment_score': 1}
    )
    
    # Aggregate by neighbourhood
    neighbourhood_sentiments = {}
    
    for review in reviews:
        listing_id = review['listing_id']
        neighbourhood = listing_neighbourhood_map.get(listing_id)
        
        if not neighbourhood:
            continue
        
        if neighbourhood not in neighbourhood_sentiments:
            neighbourhood_sentiments[neighbourhood] = {
                'positive': 0,
                'neutral': 0,
                'negative': 0,
                'scores': []
            }
        
        sentiment = review['sentiment']
        neighbourhood_sentiments[neighbourhood][sentiment] += 1
        neighbourhood_sentiments[neighbourhood]['scores'].append(review.get('sentiment_score', 0))
    
    # Calculate statistics
    result = []
    for neighbourhood, data in neighbourhood_sentiments.items():
        total = data['positive'] + data['neutral'] + data['negative']
        avg_score = sum(data['scores']) / len(data['scores']) if data['scores'] else 0
        
        result.append({
            'neighbourhood': neighbourhood,
            'total_reviews': total,
            'positive': data['positive'],
            'positive_pct': round((data['positive'] / total * 100), 1) if total > 0 else 0,
            'neutral': data['neutral'],
            'neutral_pct': round((data['neutral'] / total * 100), 1) if total > 0 else 0,
            'negative': data['negative'],
            'negative_pct': round((data['negative'] / total * 100), 1) if total > 0 else 0,
            'avg_sentiment_score': round(avg_score, 3)
        })
    
    # Sort by positive percentage
    result.sort(key=lambda x: x['positive_pct'], reverse=True)
    
    return jsonify({
        'city': city,
        'neighbourhoods': result
    })


@bp.route('/<city>/wordcloud')
def get_wordcloud_data(city):
    """
    Get word frequency data for word cloud generation.
    """
    db = get_db()
    
    neighbourhood = request.args.get('neighbourhood')
    sentiment_filter = request.args.get('sentiment')  # 'positive', 'negative', or None
    limit = request.args.get('limit', default=100, type=int)
    
    # Build query
    query = {'city': city, 'sentiment': {'$exists': True}}
    
    if sentiment_filter:
        query['sentiment'] = sentiment_filter
    
    # If neighbourhood specified, need to filter by listing_id
    if neighbourhood:
        listing_ids = [
            doc['id'] for doc in 
            db.listings.find({'city': city, 'neighbourhood_cleansed': neighbourhood}, {'id': 1})
        ]
        query['listing_id'] = {'$in': listing_ids}
    
    # Get reviews (limit to avoid memory issues)
    reviews = db.reviews.find(query, {'comments': 1}).limit(10000)
    
    # Count words (simple implementation)
    from collections import Counter
    import re
    
    word_counts = Counter()
    
    # Common stop words to exclude
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has',
        'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
        'might', 'can', 'it', 'its', 'i', 'we', 'you', 'he', 'she', 'they',
        'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'their',
        'very', 'really', 'just', 'so', 'also', 'more', 'most', 'much'
    }
    
    for review in reviews:
        text = review.get('comments', '').lower()
        words = re.findall(r'\b[a-z]{3,}\b', text)  # Words with 3+ letters
        
        for word in words:
            if word not in stop_words:
                word_counts[word] += 1
    
    # Get top words
    top_words = [
        {'word': word, 'count': count}
        for word, count in word_counts.most_common(limit)
    ]
    
    return jsonify({
        'city': city,
        'neighbourhood': neighbourhood,
        'sentiment': sentiment_filter,
        'words': top_words
    })