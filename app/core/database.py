from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Create MongoDB client
try:
    client = MongoClient(MONGODB_URL)
    # Test connection
    client.admin.command('ping')
    print("✅ MongoDB Connected Successfully!")
    
    # Get database
    db = client[DATABASE_NAME]
    
except ConnectionFailure as e:
    print(f"❌ MongoDB Connection Failed: {e}")
    db = None

# Collections
users_collection = db["users"] if db else None
resumes_collection = db["resumes"] if db else None
analyses_collection = db["analyses"] if db else None

def get_database():
    """Returns database instance"""
    return db

def get_users_collection():
    """Returns users collection"""
    return users_collection

def get_resumes_collection():
    """Returns resumes collection"""
    return resumes_collection

def get_analyses_collection():
    """Returns analyses collection"""
    return analyses_collection