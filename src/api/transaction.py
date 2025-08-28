from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config import Config
from src import logger
from src.utils.database import database
from flask import jsonify

db = database()
transactions = db.db.transaction
db = db.db.location

# def insert_product(product_data, warehouse_code, transaction_date):
#     if not product_data.get("product_code"):
#         return {
#             "success" : False
#         }
    
#     loc_code = product_data.get("location_code", "")
#     location = db.find_one({
#         "location_code" : loc_code
#     })

#     parent = location.get("parent_location_code", "")

#     # while parent is not None:
#     #     if parent == warehouse_code:
#     #         break

#     #     parent_doc = db.find_one({
#     #         "location_code" : parent
#     #     })

#     #     parent = parent_doc.get("parent_location_code", "") if parent else None

    

def transaction(data):
    warehouse_code = data.get("warehouse_code", "")
    transaction_date = data.get("transaction_date", "")
    
    if not warehouse_code or not transaction_date:
        return False
    
    for product_data in data.get("products", []):
        loc_code = product_data.get("location_code", "")
        location = db.find_one({
            "location_code" : loc_code
        })

        parent = location.get("parent_location_code", "")

        while parent is not None:
            if parent == warehouse_code:
                break

            parent_doc = db.find_one({
                "location_code" : parent
            })

            parent = parent_doc.get("parent_location_code", "") if parent else None
        
        if parent is None:
            return False
    
    transaction_new = {
        "transaction_date" : transaction_date,
        "warehouse_code" : warehouse_code,
        "products" : data.get("products", [])
    }
    transactions.insert_one(transaction_new)
    return True