"""
Test script to clean a small sample of London data
"""

import sys
sys.path.append('.')

from data.config import get_city_paths, get_processed_paths
from data.data_cleaner import DataCleaner
import pandas as pd

print("="*60)
print("TESTING DATA CLEANING")
print("="*60)

# Initialize cleaner for London
cleaner = DataCleaner('london')

# Get file paths
raw_paths = get_city_paths('london')

# Test with first 1000 rows of listings
print("\n1. Loading sample of listings...")
df_listings = pd.read_csv(raw_paths['listings'], nrows=1000)
print(f"Loaded {len(df_listings)} rows")

# Clean it
print("\n2. Cleaning listings...")
df_clean = cleaner.clean_listings(df_listings)

print("\n3. Sample of cleaned data:")
print(df_clean[['id', 'name', 'price', 'latitude', 'longitude', 'city']].head())

print("\n✅ Cleaning test successful!")