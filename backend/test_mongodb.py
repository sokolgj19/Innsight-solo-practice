"""
Quick test to verify MongoDB connection
"""

from pymongo import MongoClient

try:
    print("Testing MongoDB connection...")
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
    
    # Test connection
    client.admin.command('ping')
    
    print("✅ MongoDB is running!")
    print(f"✅ Server version: {client.server_info()['version']}")
    
    # List databases
    print(f"✅ Available databases: {client.list_database_names()}")
    
    client.close()
    
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    print("\nMake sure MongoDB is running:")
    print("  brew services start mongodb-community")