ALLOWED_TYPES = ('int', 'str', 'bool')
DB_META_FILE_NAME = 'db_meta.json'


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        raise ValueError(f'Таблица "{table_name}" уже существует.')

    validated = __validate_columns(columns)
    validated = [
        col for col in validated
        if col.split(':', 1)[0].lower() != 'id'
    ]
    validated.insert(0, 'ID:int')

    metadata[table_name] = validated
    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')

    del metadata[table_name]
    return metadata


def list_tables(metadata):
    if not metadata:
        print('Таблицы отсутствуют.')
        return

    for table_name in metadata:
        print(f'- {table_name}')


def __validate_columns(columns: list):
    column_names = []
    validated = []

    for column in columns:
        if ':' not in column:
            raise ValueError(f'Некорректное значение: {column}.')

        name, col_type = column.rsplit(':', 1)
        if not name or col_type not in ALLOWED_TYPES:
            raise ValueError(f'Некорректное значение: {column}.')
        if name in column_names:
            raise ValueError(f'Некорректное значение: {column}.')

        column_names.append(name)
        validated.append(f'{name}:{col_type}')

    return validated
