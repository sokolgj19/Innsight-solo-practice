"""
MongoDB data loader - loads cleaned CSV files into MongoDB
"""

import pandas as pd
import logging
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, BulkWriteError
from pathlib import Path
from .config import MONGO_URI, DB_NAME, COLLECTIONS, get_processed_paths

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoDBLoader:
    """Load cleaned data into MongoDB."""
    
    def __init__(self, uri: str = MONGO_URI, db_name: str = DB_NAME):
        """
        Initialize MongoDB connection.
        
        Args:
            uri: MongoDB connection URI
            db_name: Database name
        """
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None
    
    def connect(self):
        """Establish connection to MongoDB."""
        try:
            logger.info(f"Connecting to MongoDB at {self.uri}...")
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            
            # Test connection
            self.client.admin.command('ping')
            
            self.db = self.client[self.db_name]
            logger.info(f"✅ Connected to database: {self.db_name}")
            
        except ConnectionFailure as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise
    
    def disconnect(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    def drop_collections(self):
        """Drop all existing collections (use with caution!)."""
        logger.warning("⚠️  Dropping all existing collections...")
        
        for collection_name in COLLECTIONS.values():
            if collection_name in self.db.list_collection_names():
                self.db[collection_name].drop()
                logger.info(f"  Dropped: {collection_name}")
    
    def create_indexes(self):
        """Create indexes for better query performance."""
        logger.info("\n📊 Creating database indexes...")
        
        # Listings indexes
        listings = self.db[COLLECTIONS['listings']]
        listings.create_index([('id', ASCENDING)], unique=True)
        listings.create_index([('city', ASCENDING)])
        listings.create_index([('neighbourhood_cleansed', ASCENDING)])
        listings.create_index([('price', ASCENDING)])
        listings.create_index([('room_type', ASCENDING)])
        logger.info("  ✅ Listings indexes created")
        
        # Reviews indexes
        reviews = self.db[COLLECTIONS['reviews']]
        reviews.create_index([('id', ASCENDING)], unique=True)
        reviews.create_index([('listing_id', ASCENDING)])
        reviews.create_index([('city', ASCENDING)])
        reviews.create_index([('date', DESCENDING)])
        logger.info("  ✅ Reviews indexes created")
        
        logger.info("✅ All indexes created successfully")
    
    def load_listings(self, city: str, batch_size: int = 1000) -> int:
        """
        Load listings into MongoDB in batches.
        
        Args:
            city: City name (e.g., 'london')
            batch_size: Number of records per batch
            
        Returns:
            Number of documents inserted
        """
        processed_paths = get_processed_paths(city)
        filepath = processed_paths['listings']
        
        logger.info(f"\n📥 Loading {city} listings from: {filepath}")
        
        if not filepath.exists():
            logger.error(f"❌ File not found: {filepath}")
            return 0
        
        collection = self.db[COLLECTIONS['listings']]
        total_inserted = 0
        
        # Read in chunks
        for chunk_num, chunk in enumerate(pd.read_csv(filepath, chunksize=batch_size)):
            records = chunk.to_dict('records')
            
            # Clean records (convert NaN to None)
            for record in records:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
                    elif hasattr(value, 'item'):
                        record[key] = value.item()
            
            try:
                result = collection.insert_many(records, ordered=False)
                total_inserted += len(result.inserted_ids)
                
                if (chunk_num + 1) % 10 == 0:
                    logger.info(f"  Processed {total_inserted:,} listings...")
                    
            except BulkWriteError as e:
                total_inserted += e.details['nInserted']
                logger.warning(f"  Some records failed in batch {chunk_num + 1}")
        
        logger.info(f"✅ Inserted {total_inserted:,} {city} listings")
        return total_inserted
    
    def load_reviews(self, city: str, batch_size: int = 5000) -> int:
        """
        Load reviews into MongoDB in batches.
        
        Args:
            city: City name
            batch_size: Number of records per batch
            
        Returns:
            Number of documents inserted
        """
        processed_paths = get_processed_paths(city)
        filepath = processed_paths['reviews']
        
        logger.info(f"\n📥 Loading {city} reviews from: {filepath}")
        logger.info("  (This may take a few minutes...)")
        
        if not filepath.exists():
            logger.error(f"❌ File not found: {filepath}")
            return 0
        
        collection = self.db[COLLECTIONS['reviews']]
        total_inserted = 0
        
        # Read in chunks
        for chunk_num, chunk in enumerate(pd.read_csv(filepath, chunksize=batch_size)):
            records = chunk.to_dict('records')
            
            # Clean records
            for record in records:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
                    elif hasattr(value, 'item'):
                        record[key] = value.item()
            
            try:
                result = collection.insert_many(records, ordered=False)
                total_inserted += len(result.inserted_ids)
                
                if (chunk_num + 1) % 20 == 0:
                    logger.info(f"  Processed {total_inserted:,} reviews...")
                    
            except BulkWriteError as e:
                total_inserted += e.details['nInserted']
        
        logger.info(f"✅ Inserted {total_inserted:,} {city} reviews")
        return total_inserted
    
    def load_city(self, city: str, drop_existing: bool = False):
        """
        Load all data for a specific city.
        
        Args:
            city: City name
            drop_existing: Whether to drop existing data first
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"LOADING {city.upper()} DATA INTO MONGODB")
        logger.info(f"{'='*60}")
        
        self.connect()
        
        try:
            if drop_existing:
                self.drop_collections()
            
            # Load listings
            listings_count = self.load_listings(city)
            
            # Load reviews
            reviews_count = self.load_reviews(city)
            
            # Create indexes
            self.create_indexes()
            
            logger.info(f"\n{'='*60}")
            logger.info(f"✅ {city.upper()} DATA LOADED SUCCESSFULLY")
            logger.info(f"{'='*60}")
            logger.info(f"\n📊 Summary:")
            logger.info(f"  Listings: {listings_count:,}")
            logger.info(f"  Reviews: {reviews_count:,}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load data: {e}")
            raise
        finally:
            self.disconnect()


def main():
    """Run MongoDB loader from command line."""
    import sys
    
    city = sys.argv[1] if len(sys.argv) > 1 else 'london'
    drop = '--drop' in sys.argv
    
    loader = MongoDBLoader()
    loader.load_city(city, drop_existing=drop)


if __name__ == "__main__":
    main()