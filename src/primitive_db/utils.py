import json


def load_metadata(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    with open(filepath, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    return True
