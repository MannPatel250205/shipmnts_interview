from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config import Config
from src import logger

class database:
    def __init__(self):
        try:
            self.client = MongoClient(Config.MONGODB_URI)
            self.db = self.client[Config.DATABASE_NAME]
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {e}")