import json
import os

from primitive_db.constants import DATA_DIR


def load_metadata(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    return True


def load_table_data(table_name):
    filepath = f'{DATA_DIR}/{table_name}.json'
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    filepath = f'{DATA_DIR}/{table_name}.json'
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    return True


def delete_table_data(table_name):
    filepath = f'{DATA_DIR}/{table_name}.json'
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass
    return True
