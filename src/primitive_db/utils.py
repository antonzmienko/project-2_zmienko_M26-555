def load_metadata(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    return {}

def save_metadata(filepath, data):
    json.dump(data, open(filepath, 'w'))
    return True