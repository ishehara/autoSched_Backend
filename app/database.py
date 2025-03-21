from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment variables
mongo_uri = os.getenv("MONGO_URI")

# Create a MongoDB client
client = MongoClient(mongo_uri)

# Get the database
db = client.get_database("autosched")

# Create a function to test the connection
def test_connection():
    try:
        # Force a connection to verify it works
        client.admin.command('ping')
        print("MongoDB connection successful!")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {str(e)}")
        return False