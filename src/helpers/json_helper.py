
def convert_to_json(data):
    id = data.get("id", None)
    if id is None:
        raise Exception("Missing ID")
    data.update({"_id": str(id)})
    return data
