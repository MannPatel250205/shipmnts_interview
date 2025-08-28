from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config import Config
from src import logger
from src.utils.database import database
from flask import jsonify

def create_location(loc_code, parent_code):
    db = database()
    db = db.db.location

    if db.find_one({"location_code" : loc_code}):
        return jsonify({
            "success" : False,
            "message" : "Location already there"
        })
    
    if parent_code is None:
        location_type = 'warehouse'
    
    else:
        parent = db.find_one(
            {
                "location_code" : parent_code
            }
        )
        location_type = 'store'
    

    new = {
        "location_code" : loc_code,
        "parent_location_code" : parent_code,
        "type" : location_type
    }

    db.insert_one(new)
    return {
        "success" : True,
        "message" : "Location Created Successfully",
        "data" : new
    }