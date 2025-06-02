"""
Simple MongoDB connection test
"""
import pymongo

def test_simple_connection():
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["trackify"]
        collection = db["tasks"]
        
        # Insert a document
        test_doc = {
            "title": "Test Task",
            "description": "This is a test task",
            "completed": False
        }
        
        result = collection.insert_one(test_doc)
        print(f"Inserted document with ID: {result.inserted_id}")
        
        # Find the document
        found_doc = collection.find_one({"_id": result.inserted_id})
        print(f"Found document: {found_doc}")
        
        # Delete the document
        collection.delete_one({"_id": result.inserted_id})
        print("Document deleted")
        
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    test_simple_connection()
