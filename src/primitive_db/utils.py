import json

DATA_DIR = 'data'


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


def load_table_data(table_name):
    filepath = f'{DATA_DIR}/{table_name}.json'
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    filepath = f'{DATA_DIR}/{table_name}.json'
    with open(filepath, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    return True
