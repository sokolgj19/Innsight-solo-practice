"""
Listings API endpoints
"""

from flask import Blueprint, jsonify, request
from ..database import get_db
from bson import json_util
import json

bp = Blueprint('listings', __name__, url_prefix='/api/listings')


@bp.route('/<city>')
def get_listings(city):
    """
    Get listings for a city with optional filters.
    
    Query params:
        - min_price: Minimum price
        - max_price: Maximum price
        - room_type: Room type filter
        - neighbourhood: Neighbourhood filter
        - limit: Max results (default 1000)
    """
    db = get_db()
    
    # Build query
    query = {'city': city}
    
    # Price filters
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    if min_price is not None or max_price is not None:
        query['price'] = {}
        if min_price is not None:
            query['price']['$gte'] = min_price
        if max_price is not None:
            query['price']['$lte'] = max_price
    
    # Room type filter
    room_type = request.args.get('room_type')
    if room_type:
        query['room_type'] = room_type
    
    # Neighbourhood filter
    neighbourhood = request.args.get('neighbourhood')
    if neighbourhood:
        query['neighbourhood_cleansed'] = neighbourhood
    
    # Limit
    limit = request.args.get('limit', default=1000, type=int)
    limit = min(limit, 5000)  # Cap at 5000
    
    # Fields to return (exclude large fields)
    projection = {
        'id': 1,
        'name': 1,
        'latitude': 1,
        'longitude': 1,
        'price': 1,
        'room_type': 1,
        'neighbourhood_cleansed': 1,
        'number_of_reviews': 1,
        'review_scores_rating': 1
    }
    
    # Query database
    listings = list(db.listings.find(query, projection).limit(limit))
    
    # Convert ObjectId to string
    listings_json = json.loads(json_util.dumps(listings))
    
    return jsonify({
        'city': city,
        'count': len(listings_json),
        'listings': listings_json
    })


@bp.route('/<city>/<listing_id>')
def get_listing_detail(city, listing_id):
    """Get detailed information for a single listing."""
    db = get_db()
    
    listing = db.listings.find_one({
        'city': city,
        'id': listing_id
    })
    
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404
    
    # Get review sentiment for this listing
    review_pipeline = [
        {'$match': {'listing_id': listing_id, 'sentiment': {'$exists': True}}},
        {'$group': {
            '_id': '$sentiment',
            'count': {'$sum': 1}
        }}
    ]
    
    sentiment_data = list(db.reviews.aggregate(review_pipeline))
    
    sentiment_summary = {
        'positive': 0,
        'neutral': 0,
        'negative': 0
    }
    
    for item in sentiment_data:
        sentiment_summary[item['_id']] = item['count']
    
    # Convert ObjectId to string
    listing_json = json.loads(json_util.dumps(listing))
    listing_json['sentiment'] = sentiment_summary
    
    return jsonify(listing_json)


@bp.route('/<city>/neighbourhoods')
def get_neighbourhoods(city):
    """Get list of neighbourhoods for a city."""
    db = get_db()
    
    neighbourhoods = db.listings.distinct('neighbourhood_cleansed', {'city': city})
    
    return jsonify({
        'city': city,
        'neighbourhoods': sorted(neighbourhoods)
    })


@bp.route('/<city>/room-types')
def get_room_types(city):
    """Get list of room types for a city."""
    db = get_db()
    
    room_types = db.listings.distinct('room_type', {'city': city})
    
    return jsonify({
        'city': city,
        'room_types': sorted(room_types)
    })