"""
Sentiment Analysis for Airbnb Reviews using NLTK VADER
"""

import logging
from nltk.sentiment import SentimentIntensityAnalyzer
from typing import Dict, List, Tuple
import nltk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReviewSentimentAnalyzer:
    """Analyze sentiment of Airbnb reviews."""
    
    def __init__(self):
        """Initialize the sentiment analyzer."""
        # Ensure VADER lexicon is downloaded
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            logger.info("Downloading VADER lexicon...")
            nltk.download('vader_lexicon')
        
        self.sia = SentimentIntensityAnalyzer()
        logger.info("✅ Sentiment Analyzer initialized")
    
    def analyze_text(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of a single text.
        
        Args:
            text: Review text to analyze
            
        Returns:
            Dictionary with sentiment scores:
            {
                'neg': negative score (0-1),
                'neu': neutral score (0-1),
                'pos': positive score (0-1),
                'compound': compound score (-1 to 1)
            }
        """
        if not text or not isinstance(text, str):
            return {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
        
        scores = self.sia.polarity_scores(text)
        return scores
    
    def classify_sentiment(self, compound_score: float) -> str:
        """
        Classify sentiment based on compound score.
        
        Args:
            compound_score: Compound sentiment score (-1 to 1)
            
        Returns:
            'positive', 'negative', or 'neutral'
        """
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_review(self, review_text: str) -> Tuple[str, float, Dict[str, float]]:
        """
        Analyze a review and return classification with scores.
        
        Args:
            review_text: Review text
            
        Returns:
            Tuple of (sentiment_label, compound_score, all_scores)
        """
        scores = self.analyze_text(review_text)
        sentiment = self.classify_sentiment(scores['compound'])
        
        return sentiment, scores['compound'], scores
    
    def analyze_reviews_batch(self, reviews: List[str]) -> List[Dict]:
        """
        Analyze multiple reviews at once.
        
        Args:
            reviews: List of review texts
            
        Returns:
            List of sentiment results
        """
        results = []
        
        for review in reviews:
            sentiment, compound, scores = self.analyze_review(review)
            results.append({
                'sentiment': sentiment,
                'sentiment_score': compound,
                'scores': scores
            })
        
        return results
    
    def get_sentiment_stats(self, reviews: List[str]) -> Dict:
        """
        Get overall sentiment statistics for a list of reviews.
        
        Args:
            reviews: List of review texts
            
        Returns:
            Dictionary with sentiment statistics
        """
        results = self.analyze_reviews_batch(reviews)
        
        total = len(results)
        positive = sum(1 for r in results if r['sentiment'] == 'positive')
        negative = sum(1 for r in results if r['sentiment'] == 'negative')
        neutral = sum(1 for r in results if r['sentiment'] == 'neutral')
        
        avg_score = sum(r['sentiment_score'] for r in results) / total if total > 0 else 0
        
        return {
            'total_reviews': total,
            'positive': positive,
            'negative': negative,
            'neutral': neutral,
            'positive_pct': (positive / total * 100) if total > 0 else 0,
            'negative_pct': (negative / total * 100) if total > 0 else 0,
            'neutral_pct': (neutral / total * 100) if total > 0 else 0,
            'average_score': round(avg_score, 3)
        }


def test_analyzer():
    """Test the sentiment analyzer with sample reviews."""
    analyzer = ReviewSentimentAnalyzer()
    
    test_reviews = [
        "This place was absolutely amazing! The host was super friendly and the location was perfect.",
        "Terrible experience. The place was dirty and the host was rude.",
        "It was okay. Nothing special but nothing terrible either.",
        "Great location but a bit noisy at night. Overall good value for money.",
        "Beautiful apartment with stunning views! Highly recommend!"
    ]
    
    print("\n" + "="*60)
    print("TESTING SENTIMENT ANALYZER")
    print("="*60)
    
    for i, review in enumerate(test_reviews, 1):
        sentiment, score, scores = analyzer.analyze_review(review)
        
        print(f"\n{i}. Review: {review[:60]}...")
        print(f"   Sentiment: {sentiment.upper()} (score: {score:.3f})")
        print(f"   Breakdown: pos={scores['pos']:.2f}, neu={scores['neu']:.2f}, neg={scores['neg']:.2f}")
    
    # Overall stats
    print("\n" + "="*60)
    print("OVERALL STATISTICS")
    print("="*60)
    stats = analyzer.get_sentiment_stats(test_reviews)
    print(f"Total reviews: {stats['total_reviews']}")
    print(f"Positive: {stats['positive']} ({stats['positive_pct']:.1f}%)")
    print(f"Neutral: {stats['neutral']} ({stats['neutral_pct']:.1f}%)")
    print(f"Negative: {stats['negative']} ({stats['negative_pct']:.1f}%)")
    print(f"Average score: {stats['average_score']}")
    print("="*60)


if __name__ == "__main__":
    test_analyzer()