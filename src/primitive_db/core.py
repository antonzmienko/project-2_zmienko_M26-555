from primitive_db.decorators import handle_db_errors

ALLOWED_TYPES = ('int', 'str', 'bool')
DB_META_FILE_NAME = 'db_meta.json'


@handle_db_errors
def create_table(metadata, table_name, columns):
    if table_name in metadata:
        raise ValueError(f'Таблица "{table_name}" уже существует.')

    validated = __validate_columns(columns)
    validated = [
        col for col in validated
        if col.split(':', 1)[0].lower() != 'id'
    ]
    validated.insert(0, 'ID:int')

    metadata[table_name] = {
        'columns': validated,
        'last_id': 0,
    }
    return metadata


@handle_db_errors
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


@handle_db_errors
def insert(metadata, table_name, table_data, values):
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')

    table_meta = metadata[table_name]
    columns = table_meta['columns']
    data_columns = [
        column for column in columns
        if column.split(':', 1)[0].lower() != 'id'
    ]
    if len(values) != len(data_columns):
        raise ValueError(
            f'Некорректное значение: ожидалось {len(data_columns)} '
            f'значений (без ID), получено {len(values)}.'
        )

    new_id = table_meta['last_id'] + 1
    table_meta['last_id'] = new_id

    record = {'ID': new_id}
    for value, column in zip(values, data_columns):
        name, col_type = column.split(':', 1)
        record[name] = __cast_value(value, col_type)

    table_data.append(record)
    return table_data


@handle_db_errors
def select(table_data, where_clause=None):
    if where_clause is None:
        return list(table_data)

    return [
        row for row in table_data
        if __matches_where(row, where_clause)
    ]


@handle_db_errors
def update(table_data, set_clause, where_clause):
    for row in table_data:
        if __matches_where(row, where_clause):
            row.update(set_clause)
    return table_data


@handle_db_errors
def delete(table_data, where_clause):
    return [
        row for row in table_data
        if not __matches_where(row, where_clause)
    ]


def __matches_where(row, where_clause):
    return all(row.get(key) == value for key, value in where_clause.items())


def __cast_value(value, col_type):
    if col_type == 'int':
        if isinstance(value, bool):
            raise ValueError(f'Некорректное значение: {value}.')
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                raise ValueError(f'Некорректное значение: {value}.')
        raise ValueError(f'Некорректное значение: {value}.')

    if col_type == 'str':
        if isinstance(value, str):
            return value
        raise ValueError(f'Некорректное значение: {value}.')

    if col_type == 'bool':
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            lowered = value.lower()
            if lowered == 'true':
                return True
            if lowered == 'false':
                return False
        raise ValueError(f'Некорректное значение: {value}.')

    raise ValueError(f'Некорректное значение: {value}.')


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
