import json

def convert_to_json(data):
    for d in data:
        id = d.get("_id", None)
        if id is None:
            raise Exception("Missing ID")
        d.update({"_id": str(id)})
    return json.dumps(data)
