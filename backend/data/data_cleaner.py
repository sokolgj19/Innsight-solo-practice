"""
Data cleaning module with language detection for English-only reviews
"""

import pandas as pd
import logging
from .config import LISTINGS_COLUMNS, REVIEWS_COLUMNS, CALENDAR_COLUMNS
from .utils import (
    clean_price, 
    parse_date, 
    clean_percentage, 
    parse_boolean,
    clean_text,
    parse_amenities,
    remove_duplicates,
    log_data_summary
)

# For language detection
try:
    from langdetect import detect, LangDetectException
except ImportError:
    print("Installing langdetect...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'langdetect'])
    from langdetect import detect, LangDetectException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def is_english(text):
    """
    Check if text is in English.
    
    Args:
        text: Text to check
    
    Returns:
        True if English, False otherwise
    """
    if not text or len(str(text).strip()) < 10:
        return False
    
    try:
        return detect(str(text)) == 'en'
    except LangDetectException:
        return False


class DataCleaner:
    """Cleans and transforms raw data from CSV files."""
    
    def __init__(self, city_name: str):
        """
        Initialize data cleaner for a specific city.
        
        Args:
            city_name: Name of the city (e.g., 'london', 'paris', 'amsterdam')
        """
        self.city_name = city_name
    
    def clean_listings(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean listings data and handle null prices.
        
        Args:
            df: Raw listings DataFrame
            
        Returns:
            Cleaned listings DataFrame
        """
        logger.info(f"Cleaning {self.city_name} listings data...")
        
        # Select only required columns (if they exist)
        available_cols = [col for col in LISTINGS_COLUMNS if col in df.columns]
        df = df[available_cols].copy()
        
        # Add city column
        df['city'] = self.city_name
        
        # Clean price
        if 'price' in df.columns:
            df['price'] = df['price'].apply(clean_price)
            
            # Calculate neighbourhood averages for null prices
            if df['price'].isna().any():
                logger.info("Handling null prices by setting to neighbourhood average...")
                
                # Calculate average price per neighbourhood
                neighbourhood_avg = df.groupby('neighbourhood_cleansed')['price'].mean()
                
                # Fill null prices with neighbourhood average
                def fill_null_price(row):
                    if pd.isna(row['price']) and row['neighbourhood_cleansed'] in neighbourhood_avg:
                        return neighbourhood_avg[row['neighbourhood_cleansed']]
                    return row['price']
                
                df['price'] = df.apply(fill_null_price, axis=1)
                
                # If still null (neighbourhood had no prices), use city average
                city_avg = df['price'].mean()
                df['price'] = df['price'].fillna(city_avg)
                
                logger.info(f"  Filled null prices with averages")
        
        # Clean host response rate
        if 'host_response_rate' in df.columns:
            df['host_response_rate'] = df['host_response_rate'].apply(clean_percentage)
        
        # Parse boolean fields
        boolean_fields = ['host_is_superhost', 'instant_bookable']
        for field in boolean_fields:
            if field in df.columns:
                df[field] = df[field].apply(parse_boolean)
        
        # Clean text fields
        text_fields = ['name', 'description']
        for field in text_fields:
            if field in df.columns:
                df[field] = df[field].apply(clean_text)
        
        # Parse amenities
        if 'amenities' in df.columns:
            df['amenities'] = df['amenities'].apply(parse_amenities)
        
        # Convert numeric fields
        numeric_fields = [
            'latitude', 'longitude', 'accommodates', 
            'bathrooms', 'bedrooms', 'beds',
            'minimum_nights', 'maximum_nights',
            'number_of_reviews', 'review_scores_rating',
            'host_listings_count'
        ]
        
        for field in numeric_fields:
            if field in df.columns:
                df[field] = pd.to_numeric(df[field], errors='coerce')
        
        # Parse dates
        if 'host_since' in df.columns:
            df['host_since'] = pd.to_datetime(df['host_since'], errors='coerce')
        
        # Remove duplicates
        df = remove_duplicates(df, subset=['id'])
        
        # Convert id to string for consistency
        df['id'] = df['id'].astype(str)
        if 'host_id' in df.columns:
            df['host_id'] = df['host_id'].astype(str)
        
        log_data_summary(df, f"{self.city_name.title()} Cleaned Listings")
        logger.info("Listings cleaning complete")
        
        return df
    
    def clean_reviews(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean reviews data and filter for English-only reviews.
        
        Args:
            df: Raw reviews DataFrame
            
        Returns:
            Cleaned reviews DataFrame (English only)
        """
        logger.info(f"Cleaning {self.city_name} reviews data...")
        
        initial_count = len(df)
        
        # Select only required columns
        available_cols = [col for col in REVIEWS_COLUMNS if col in df.columns]
        df = df[available_cols].copy()
        
        # Add city column
        df['city'] = self.city_name
        
        # Convert IDs to string
        df['listing_id'] = df['listing_id'].astype(str)
        df['id'] = df['id'].astype(str)
        if 'reviewer_id' in df.columns:
            df['reviewer_id'] = df['reviewer_id'].astype(str)
        
        # Parse date
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Clean comments text
        if 'comments' in df.columns:
            df['comments'] = df['comments'].apply(lambda x: clean_text(x, remove_html=True))
            
            # Remove rows with empty comments after cleaning
            df = df[df['comments'].notna()]
            df = df[df['comments'].str.len() >= 10]  # Minimum 10 characters
            
            # Filter for English-only reviews
            logger.info("  Filtering for English-only reviews (this may take a few minutes)...")
            df['is_english'] = df['comments'].apply(is_english)
            df = df[df['is_english'] == True]
            df = df.drop('is_english', axis=1)
            
            english_count = len(df)
            removed = initial_count - english_count
            logger.info(f"  Kept {english_count:,} English reviews, removed {removed:,} non-English")
        
        # Clean reviewer name
        if 'reviewer_name' in df.columns:
            df['reviewer_name'] = df['reviewer_name'].apply(lambda x: clean_text(x, remove_html=False))
        
        # Remove duplicates
        df = remove_duplicates(df, subset=['id'])
        
        # Sort by date
        if 'date' in df.columns:
            df = df.sort_values('date')
        
        log_data_summary(df, f"{self.city_name.title()} Cleaned Reviews (English Only)")
        logger.info("Reviews cleaning complete")
        
        return df
    
    def clean_calendar(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean calendar data.
        
        Args:
            df: Raw calendar DataFrame
            
        Returns:
            Cleaned calendar DataFrame
        """
        logger.info(f"Cleaning {self.city_name} calendar data...")
        
        # Select only required columns
        available_cols = [col for col in CALENDAR_COLUMNS if col in df.columns]
        df = df[available_cols].copy()
        
        # Add city column
        df['city'] = self.city_name
        
        # Convert listing_id to string
        df['listing_id'] = df['listing_id'].astype(str)
        
        # Parse date
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])
        
        # Parse available field
        if 'available' in df.columns:
            df['available'] = df['available'].apply(parse_boolean)
        
        # Clean price
        if 'price' in df.columns:
            df['price'] = df['price'].apply(clean_price)
        
        # Convert numeric fields
        numeric_fields = ['minimum_nights', 'maximum_nights']
        for field in numeric_fields:
            if field in df.columns:
                df[field] = pd.to_numeric(df[field], errors='coerce')
        
        # Remove duplicates (listing_id + date should be unique)
        df = remove_duplicates(df, subset=['listing_id', 'date'])
        
        # Sort by listing_id and date
        df = df.sort_values(['listing_id', 'date'])
        
        log_data_summary(df, f"{self.city_name.title()} Cleaned Calendar")
        logger.info("Calendar cleaning complete")
        
        return df