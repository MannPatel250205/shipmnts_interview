from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from config import Config
from src.utils.database import database
from src import logger

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = database()

@app.route('/')
def main():
    return render_template('index.html')

if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=5000)