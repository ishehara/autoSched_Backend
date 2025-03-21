from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

def test_connection():
    try:
        # Get connection string from environment variable
        mongo_uri = os.getenv("MONGO_URI")
        print(f"Attempting to connect to: {mongo_uri}")
        
        # Create a MongoDB client
        client = MongoClient(mongo_uri)
        
        # Force a connection to verify it works
        server_info = client.server_info()
        
        print("MongoDB connection successful!")
        print(f"Server info: {server_info['version']}")
        
        # List databases
        databases = client.list_database_names()
        print(f"Available databases: {databases}")
        
        # Try to access our specific database
        db = client.get_database("autosched")
        print(f"Connected to database: {db.name}")
        
        # List collections
        collections = db.list_collection_names()
        print(f"Collections in database: {collections}")
        
        # Try to insert a test document
        result = db.test_collection.insert_one({"test": "Remote connection test"})
        print(f"Inserted document with ID: {result.inserted_id}")
        
        # Clean up by deleting the test document
        db.test_collection.delete_one({"_id": result.inserted_id})
        print("Test document deleted")
        
    except Exception as e:
        print(f"MongoDB connection failed: {str(e)}")

if __name__ == "__main__":
    test_connection()