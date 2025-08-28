from flask import Flask, render_template, request, jsonify, Blueprint
from flask_cors import CORS
from config import Config
from src.utils.database import database
from src import logger
from src.api.create_location import create_location
from src.api.tree import generate_tree
from src.api.transaction import transaction

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = database()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/api/create_location', methods=['POST'])
def create_loc():
    data = request.get_json()
    location_code = data.get("location_code", "")
    parent_location_code = data.get("parent_location_code", "")

    final_json = create_location(location_code, parent_location_code)

    if final_json["success"]:

        return jsonify({
            "success" : True,
            "message" : final_json["message"],
            "data" : {
                "location_code" : final_json["data"]["location_code"],
                "parent_location_code" : final_json["data"]["parent_location_code"],
                "type" : final_json["data"]["type"]
            }
        }), 200
    
    else:
        return jsonify({
            "success" : False,
            "message" : final_json["message"],
        }) , 400


@app.route('/api/warehouse/tree', methods=['GET'])
def tree():
    data = request.args.get('warehouse_code')

    final_json = generate_tree(data)


    if final_json["success"]:
        return jsonify(final_json), 200
    
    else:
        return jsonify(final_json), 400


@app.route('/api/transaction/receipt', methods=['POST'])
def receipt():
    data = request.get_json()
    is_success = transaction(data)
    if is_success:
        return jsonify({
            "success" : True,
            "message" : "Products added successfully"
        })
    
    else:
        return jsonify({
            "success" : False,
            "message" : "Location dosen't belong to specific ware house"
        })

if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=5000)