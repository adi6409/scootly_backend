from pymongo import MongoClient
from config import MONGODB_URI, DATABASE_NAME, COLLECTION_NAME

def get_database():
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    return db[COLLECTION_NAME]

def init_db():
    """Initialize database indexes"""
    collection = get_database()
    collection.create_index("system_id", unique=True)
    collection.create_index("location") 