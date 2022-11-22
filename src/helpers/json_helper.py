import json

def convert_to_json(data):
    for d in data:
        id = d.get("_id", None)
        last_updated = d.get("last_updated", None)
        if id is None:
            raise Exception("Missing ID")
        if last_updated is None:
            raise Exception("Missing timestamp")

        d.update({"_id": str(id), "last_updated": str(last_updated)})
    return json.dumps(data)
