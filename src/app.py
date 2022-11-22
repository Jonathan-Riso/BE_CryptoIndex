from sre_constants import SUCCESS
from flask import Flask, Response, abort
from pymongo import MongoClient
from helpers.json_helper import convert_to_json
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# Connects to default localhost
uri = os.environ.get("mongo_uri")
client = MongoClient(uri)
scores = client.cryptoIndex.scores

# https://flask.palletsprojects.com/en/2.2.x/quickstart/
# for basics

# @app.route("/heartbeat")
# def heartbeat():
#     result = heartbeat_collection.insert_one({"status": "Alive"})
#     document = heartbeat_collection.find_one({"_id": ObjectId(result.inserted_id)})
#     return convert_to_json(document)

@app.route("/results/<index>")
def results(index):
    print(index)
    result = scores.find_one({"index": index.lower()})
    if not result:
        abort(404)
    print(result)
    # if result.time < 2 hours current
    # Post new results
    return Response(f"{convert_to_json(result)}", status=200, mimetype='application/json')

# GET Tweets
# GET News_Reports
# POST results