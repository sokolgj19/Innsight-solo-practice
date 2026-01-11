"""
ETL Pipeline for processing Airbnb data
"""

import pandas as pd
import logging
from pathlib import Path
from .config import get_city_paths, get_processed_paths, CHUNK_SIZE
from .data_cleaner import DataCleaner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ETLPipeline:
    """Main ETL pipeline orchestrator."""
    
    def __init__(self, city_name: str):
        """
        Initialize ETL pipeline for a specific city.
        
        Args:
            city_name: Name of the city (e.g., 'london', 'paris', 'amsterdam')
        """
        self.city_name = city_name
        self.cleaner = DataCleaner(city_name)
        self.raw_paths = get_city_paths(city_name)
        self.processed_paths = get_processed_paths(city_name)
    
    def process_listings(self) -> pd.DataFrame:
        """
        Process listings data: Extract -> Clean -> Save
        
        Returns:
            Cleaned listings DataFrame
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"PROCESSING {self.city_name.upper()} LISTINGS")
        logger.info(f"{'='*60}")
        
        # Extract
        logger.info(f"Loading from: {self.raw_paths['listings']}")
        df = pd.read_csv(self.raw_paths['listings'], low_memory=False)
        logger.info(f"Loaded {len(df):,} raw listings")
        
        # Clean
        df_clean = self.cleaner.clean_listings(df)
        
        # Save
        output_path = self.processed_paths['listings']
        df_clean.to_csv(output_path, index=False)
        logger.info(f"✅ Saved to: {output_path}")
        logger.info(f"Final row count: {len(df_clean):,}")
        
        return df_clean
    
    def process_reviews(self, use_chunks: bool = True) -> pd.DataFrame:
        """
        Process reviews data (may be large, so use chunks).
        
        Args:
            use_chunks: Whether to process in chunks
            
        Returns:
            Cleaned reviews DataFrame
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"PROCESSING {self.city_name.upper()} REVIEWS")
        logger.info(f"{'='*60}")
        
        raw_path = self.raw_paths['reviews']
        output_path = self.processed_paths['reviews']
        
        if use_chunks:
            logger.info("Processing reviews in chunks...")
            chunks = []
            
            for i, chunk in enumerate(pd.read_csv(raw_path, chunksize=CHUNK_SIZE)):
                logger.info(f"Processing chunk {i+1}...")
                cleaned_chunk = self.cleaner.clean_reviews(chunk)
                chunks.append(cleaned_chunk)
            
            df_clean = pd.concat(chunks, ignore_index=True)
        else:
            logger.info(f"Loading from: {raw_path}")
            df = pd.read_csv(raw_path)
            df_clean = self.cleaner.clean_reviews(df)
        
        # Save
        df_clean.to_csv(output_path, index=False)
        logger.info(f"✅ Saved to: {output_path}")
        logger.info(f"Final row count: {len(df_clean):,}")
        
        return df_clean
    
    def process_calendar(self, use_chunks: bool = True) -> pd.DataFrame:
        """
        Process calendar data (very large, use chunks).
        
        Args:
            use_chunks: Whether to process in chunks
            
        Returns:
            Cleaned calendar DataFrame
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"PROCESSING {self.city_name.upper()} CALENDAR")
        logger.info(f"{'='*60}")
        
        raw_path = self.raw_paths['calendar']
        output_path = self.processed_paths['calendar']
        
        if use_chunks:
            logger.info("Processing calendar in chunks (this may take a few minutes)...")
            chunks = []
            
            for i, chunk in enumerate(pd.read_csv(raw_path, chunksize=CHUNK_SIZE)):
                logger.info(f"Processing chunk {i+1}...")
                cleaned_chunk = self.cleaner.clean_calendar(chunk)
                chunks.append(cleaned_chunk)
            
            df_clean = pd.concat(chunks, ignore_index=True)
        else:
            logger.info(f"Loading from: {raw_path}")
            df = pd.read_csv(raw_path)
            df_clean = self.cleaner.clean_calendar(df)
        
        # Save
        df_clean.to_csv(output_path, index=False)
        logger.info(f"✅ Saved to: {output_path}")
        logger.info(f"Final row count: {len(df_clean):,}")
        
        return df_clean
    
    def run_full_pipeline(self, skip_calendar: bool = False):
        """
        Run the complete ETL pipeline for all datasets.
        
        Args:
            skip_calendar: Whether to skip calendar processing (it's very large)
        
        Returns:
            Dictionary with all processed DataFrames
        """
        logger.info(f"\n{'#'*60}")
        logger.info(f"# STARTING FULL ETL PIPELINE FOR {self.city_name.upper()}")
        logger.info(f"{'#'*60}\n")
        
        results = {}
        
        try:
            # Process listings
            results['listings'] = self.process_listings()
            
            # Process reviews
            results['reviews'] = self.process_reviews()
            
            # Process calendar (optional, as it's very large)
            if not skip_calendar:
                results['calendar'] = self.process_calendar()
            else:
                logger.info("\n⏭️  Skipping calendar processing (use skip_calendar=False to process)")
            
            logger.info(f"\n{'#'*60}")
            logger.info(f"# ETL PIPELINE COMPLETED SUCCESSFULLY")
            logger.info(f"{'#'*60}")
            
            # Print summary
            logger.info(f"\n📊 Final Summary for {self.city_name.title()}:")
            logger.info(f"  Listings: {len(results['listings']):,} rows")
            logger.info(f"  Reviews: {len(results['reviews']):,} rows")
            if not skip_calendar:
                logger.info(f"  Calendar: {len(results['calendar']):,} rows")
            
        except Exception as e:
            logger.error(f"❌ ETL Pipeline failed: {e}")
            raise
        
        return results


def main():
    """Run ETL pipeline from command line."""
    import sys
    
    city = sys.argv[1] if len(sys.argv) > 1 else 'london'
    skip_cal = '--skip-calendar' in sys.argv
    
    logger.info(f"Running ETL for city: {city}")
    
    pipeline = ETLPipeline(city)
    pipeline.run_full_pipeline(skip_calendar=skip_cal)


if __name__ == "__main__":
    main()