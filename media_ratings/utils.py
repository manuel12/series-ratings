import json

def get_data_from_json(file):
    with open(file) as f:
      data = json.load(f)
    return data