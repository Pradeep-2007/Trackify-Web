"""
Test script to verify MongoDB connection
"""
import pymongo
import sys

def test_connection():
    try:
        # Connect to MongoDB running on localhost
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        
        # Check if the connection is successful
        client.server_info()  # This will raise an exception if connection fails
        
        # Get database list to verify connection
        db_list = client.list_database_names()
        
        print("MongoDB connection successful!")
        print(f"Available databases: {db_list}")
        
        # Create or access the 'trackify' database
        db = client['trackify']
        print(f"Connected to 'trackify' database")
        
        # List collections in the database
        collections = db.list_collection_names()
        print(f"Collections in 'trackify': {collections}")
        
        return True
    except pymongo.errors.ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if not success:
        sys.exit(1)
