from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['innsight_db']
total = db.reviews.count_documents({'city': 'london'})
print(f"Total London reviews: {total:,}")
sample = db.reviews.find_one({'city': 'london'})
print(f"\nSample review:")
print(f"  ID: {sample.get('id')}")
print(f"  Comments: {sample.get('comments', '')[:100]}...")
print(f"  Has sentiment: {'sentiment' in sample}")
client.close()
