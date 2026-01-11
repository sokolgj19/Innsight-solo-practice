"""
Configuration file for InnSight data processing pipeline
"""

import os
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Supported cities
CITIES = ['london', 'paris', 'amsterdam']

# Data directories
RAW_DATA_DIR = BASE_DIR / 'data' / 'raw'
PROCESSED_DATA_DIR = BASE_DIR / 'data' / 'processed'

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_city_paths(city_name):
    """
    Get file paths for a specific city's raw data files.
    
    Args:
        city_name: Name of the city (e.g., 'london', 'paris', 'amsterdam')
    
    Returns:
        Dictionary with paths to all data files for that city
    """
    city_raw = RAW_DATA_DIR / city_name
    city_raw.mkdir(parents=True, exist_ok=True)
    
    return {
        'listings': city_raw / 'listings.csv',
        'reviews': city_raw / 'reviews.csv',
        'calendar': city_raw / 'calendar.csv',
        'neighbourhoods': city_raw / 'neighbourhoods.csv',
        'geojson': city_raw / 'neighbourhoods.geojson'
    }


def get_processed_paths(city_name):
    """
    Get file paths for a specific city's processed data files.
    
    Args:
        city_name: Name of the city
    
    Returns:
        Dictionary with paths to processed data files
    """
    return {
        'listings': PROCESSED_DATA_DIR / f'{city_name}_listings_clean.csv',
        'reviews': PROCESSED_DATA_DIR / f'{city_name}_reviews_clean.csv',
        'calendar': PROCESSED_DATA_DIR / f'{city_name}_calendar_clean.csv',
        'neighbourhoods': PROCESSED_DATA_DIR / f'{city_name}_neighbourhoods_clean.csv',
        'geojson': PROCESSED_DATA_DIR / f'{city_name}_neighbourhoods.geojson'
    }


# MongoDB configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = 'innsight_db'

COLLECTIONS = {
    'listings': 'listings',
    'reviews': 'reviews',
    'calendar': 'calendar',
    'neighbourhoods': 'neighbourhoods'
}

# Columns to keep from listings.csv
LISTINGS_COLUMNS = [
    'id', 'listing_url', 'name', 'description',
    'host_id', 'host_name', 'host_since',
    'host_response_rate', 'host_is_superhost',
    'host_listings_count', 'neighbourhood_cleansed',
    'latitude', 'longitude', 'property_type',
    'room_type', 'accommodates', 'bathrooms',
    'bedrooms', 'beds', 'amenities', 'price',
    'minimum_nights', 'maximum_nights',
    'number_of_reviews', 'review_scores_rating',
    'instant_bookable'
]

# Columns to keep from reviews.csv
REVIEWS_COLUMNS = [
    'listing_id', 'id', 'date',
    'reviewer_id', 'reviewer_name', 'comments'
]

# Columns to keep from calendar.csv
CALENDAR_COLUMNS = [
    'listing_id', 'date', 'available',
    'price', 'minimum_nights', 'maximum_nights'
]

# Coordinate validation ranges for each city
COORDINATE_RANGES = {
    'london': {
        'latitude': (51.28, 51.70),
        'longitude': (-0.51, 0.34)
    },
    'paris': {
        'latitude': (48.81, 48.90),
        'longitude': (2.22, 2.47)
    },
    'amsterdam': {
        'latitude': (52.28, 52.43),
        'longitude': (4.73, 5.08)
    }
}

# Data validation rules
VALIDATION_RULES = {
    'listings': {
        'required_columns': ['id', 'name', 'latitude', 'longitude', 'price'],
        'numeric_columns': ['latitude', 'longitude', 'accommodates', 'bedrooms', 'beds', 'price'],
        'price_range': (0, 10000)
    },
    'reviews': {
        'required_columns': ['listing_id', 'date', 'comments'],
        'min_comment_length': 10
    },
    'calendar': {
        'required_columns': ['listing_id', 'date', 'available']
    }
}

# ETL settings
CHUNK_SIZE = 10000  # Process large files in chunks
DATE_FORMAT = '%Y-%m-%d'

# Inside Airbnb data URLs
DATA_URLS = {
    'london': 'http://data.insideairbnb.com/united-kingdom/england/london/',
    'paris': 'http://data.insideairbnb.com/france/ile-de-france/paris/',
    'amsterdam': 'http://data.insideairbnb.com/the-netherlands/north-holland/amsterdam/'
}