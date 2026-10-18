import json
import os

from primitive_db.constants import DATA_DIR


def load_metadata(filepath):
    """Загружает метаданные БД из JSON-файла."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохраняет метаданные БД в JSON-файл."""
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    return True


def load_table_data(table_name):
    """Загружает данные таблицы из JSON-файла."""
    filepath = f'{DATA_DIR}/{table_name}.json'
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохраняет данные таблицы в JSON-файл."""
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
