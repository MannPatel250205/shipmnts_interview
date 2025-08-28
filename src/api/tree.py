from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config import Config
from src import logger
from src.utils.database import database
from flask import jsonify

db = database()
db = db.db.location

def build(warehouse_code):
    loc = db.find_one({
        "location_code" : warehouse_code
    })

    if not loc:
        return None
    
    childs = db.find_many({
        "parent_location_code" : warehouse_code
    })

    loc["childs"] : [build(child["location_code"]) for child in childs]

    return loc

def generate_tree(warehouse_code):

    warehouse = db.find_one({
        "location_code" : warehouse_code,
        "type" : "warehouse"
    })
    
    if not warehouse:
        return jsonify({
            "success" : False,
            "message" : "warehouse not found"
        })
    
    overall_tree = build(warehouse_code)
    
    return overall_tree