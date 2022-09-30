from flask import Flask

app = Flask(__name__)

# https://flask.palletsprojects.com/en/2.2.x/quickstart/
# for basics

@app.route("/heartbeat")
def heartbeat():
    return {"status": "Alive"}