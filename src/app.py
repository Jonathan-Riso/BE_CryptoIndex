from sre_constants import SUCCESS
from flask import Flask, Response, abort, url_for
from pymongo import MongoClient
from helpers.json_helper import convert_to_json
from calculations.index import calc_index
from dotenv import load_dotenv
from datetime import datetime
import json
import os
import logging

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

@app.route("/", methods=['GET'])
def get_homepage():
    try:
        
        result = list(scores.find())
        logging.info(result)
        return Response(f"{convert_to_json(result)}", status=200, mimetype='application/json')
    except Exception as e:
        logging.error(f"GET / || ERROR: {e}")
        abort(Response(e, 500))

@app.route("/results/<index>", methods=['GET'])
def get_index_results(index):
    try:
        result = scores.find_one({"index": index.lower()})
        if not result:
            scores.insert_one(calc_index(index))
            result = scores.find_one({"index": index.lower()})
            # abort(404)
        
        if recalculate(result) is True:
            scores.insert_one(calc_index(index))
            result = scores.find_one({"index": index.lower()})            
        
        return Response(f"{convert_to_json([result])}", status=200, mimetype='application/json')

    except Exception as e:
        logging.error(f"GET /results/{index} || ERROR: {e}")
        abort(Response(e, 500))



@app.route('/tweets/<index>', methods=['GET'])
def get_index_tweets(index):
    try:
        result = scores.find_one({"index": index.lower()})
        if not result:
            abort(404)
        
        if recalculate(result) is True:
            scores.insert_one(calc_index(index))
            result = scores.find_one({"index": index.lower()})            
        
        tweets = result.get('twitter')

        return Response(f"{json.dumps(tweets)}", status=200, mimetype='application/json')
    except Exception as e:
        logging.error(f"GET /tweets/{index} || ERROR: {e}")
        abort(Response(e, 500))

@app.route('/news/<index>', methods=['GET'])
def get_index_news(index):
    try:
        result = scores.find_one({"index": index.lower()})
        if not result:
            abort(404)
        
        if recalculate(result) is True:
            scores.insert_one(calc_index(index))
            result = scores.find_one({"index": index.lower()})            
        
        news = result.get('news')

        return Response(f"{json.dumps(news)}", status=200, mimetype='application/json')
    except Exception as e:
        logging.error(f"GET /news/{index} || ERROR: {e}")
        abort(Response(e, 500))

@app.route('/reddit/<index>', methods=['GET'])
def get_index_reddit(index):
    try:
        result = scores.find_one({"index": index.lower()})
        if not result:
            abort(404)
        
        if recalculate(result) is True:
            scores.insert_one(calc_index(index))
            result = scores.find_one({"index": index.lower()})            
        
        posts = result.get('reddit')

        return Response(f"{json.dumps(posts)}", status=200, mimetype='application/json')
    except Exception as e:
        logging.error(f"GET /reddit/{index} || ERROR: {e}")
        abort(Response(e, 500))

def recalculate(result):
    hours = divmod((datetime.utcnow() - result["last_updated"]).total_seconds(), 3600)[0]
    if (hours > 1):
        return True
    else:
        return False

if __name__=="__main":
	app.run()
