from sre_constants import SUCCESS
from flask import Flask
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from src.helpers.json_helper import convert_to_json
import json

app = Flask(__name__)

# Connects to default localhost
client = MongoClient()
heartbeat_collection = client.cryptoIndex.heartbeat

# https://flask.palletsprojects.com/en/2.2.x/quickstart/
# for basics

@app.route("/heartbeat")
def heartbeat():
    result = heartbeat_collection.insert_one({"status": "Alive"})
    document = heartbeat_collection.find_one({"_id": ObjectId(result.inserted_id)})
    return convert_to_json(document)