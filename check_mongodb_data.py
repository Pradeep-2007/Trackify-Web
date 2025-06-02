"""
Script to check MongoDB collections and data
"""
import pymongo
import os
import django
from pprint import pprint

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackify.settings')
django.setup()

def check_mongodb_data():
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["trackify"]
        
        # Get all collections
        collections = db.list_collection_names()
        print(f"Collections in 'trackify' database: {collections}")
        
        # Check each collection
        for collection_name in collections:
            collection = db[collection_name]
            count = collection.count_documents({})
            print(f"\n{collection_name}: {count} documents")
            
            # Show sample documents (up to 3)
            if count > 0:
                print(f"Sample documents from {collection_name}:")
                for doc in collection.find().limit(3):
                    pprint(doc)
                    print("---")
        
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    check_mongodb_data()
