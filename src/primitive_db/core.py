DB_META_FILE_NAME = 'db_meta.json'

def create_table(metadata, table_name, columns):
    __check_unique_table_name(metadata, table_name)
    __validate_columns(columns)

    idColumnIndex = None
    if {id: int} in columns:
        idColumnIndex = columns.index({name: 'ID', type: 'int'})

    if idColumnIndex is None:
        columns.insert(0, {name: 'ID', type: 'int'})
    elif idColumnIndex != 0:
        columns.insert(0, columns.pop(idColumnIndex))

    table = {
        'name': table_name,
        'columns': columns
    }
    metadata[table_name] = table

    return metadata

def drop_table(metadata, table_name):
    __check_table_exists(metadata, table_name)
    del metadata[table_name]
    return metadata

def __validate_columns(columns: list):
    column_names = []
    for column in columns:
        if column.get('type') is None:
            raise ValueError('Column type is required')
        if column.get('type') not in ['int', 'float', 'str', 'bool']:
            raise ValueError('Invalid column type')
        if column.get('name') is None:
            raise ValueError('Column name is required')
        if column.get('name') in column_names:
            raise ValueError('Column name must be unique')

        column_names.append(column.get('name'))

def __check_unique_table_name(metadata, table_name):
    table = next(
        (t for t in metadata["tables"] if t["table_name"] == table_name),
        None
    )

    if table is not None:
        raise ValueError('Table name must be unique')

def __check_table_exists(metadata, table_name):
    if table_name not in metadata:
        raise ValueError('Table does not exist')