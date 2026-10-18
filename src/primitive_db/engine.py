import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import (
    DB_META_FILE_NAME,
    create_table,
    delete,
    drop_table,
    insert,
    list_tables,
    select,
    update,
)
from primitive_db.parser import parse_set_clause, parse_values, parse_where_clause
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

COMMAND_EXIT = 'exit'
COMMAND_HELP = 'help'
COMMAND_CREATE_TABLE = 'create_table'
COMMAND_DROP_TABLE = 'drop_table'
COMMAND_LIST_TABLES = 'list_tables'
COMMAND_INSERT = 'insert'
COMMAND_SELECT = 'select'
COMMAND_UPDATE = 'update'
COMMAND_DELETE = 'delete'
COMMAND_INFO = 'info'


def run():
    print_help()

    while True:
        metadata = load_metadata(DB_META_FILE_NAME)
        user_input = prompt.string('Введите команду: ')

        try:
            args = shlex.split(user_input)
        except ValueError:
            print('Некорректное значение: не удалось разобрать команду. '
                  'Попробуйте снова.')
            continue

        if not args:
            continue

        command, *command_args = args

        if command == COMMAND_EXIT:
            break
        elif command == COMMAND_HELP:
            print_help()
        elif command == COMMAND_CREATE_TABLE:
            __handle_create_table(metadata, command_args)
        elif command == COMMAND_DROP_TABLE:
            __handle_drop_table(metadata, command_args)
        elif command == COMMAND_LIST_TABLES:
            list_tables(metadata)
        elif command == COMMAND_INSERT:
            __handle_insert(metadata, user_input)
        elif command == COMMAND_SELECT:
            __handle_select(metadata, user_input)
        elif command == COMMAND_UPDATE:
            __handle_update(metadata, user_input)
        elif command == COMMAND_DELETE:
            __handle_delete(metadata, user_input)
        elif command == COMMAND_INFO:
            __handle_info(metadata, command_args)
        else:
            print(f'Функции {command} нет. Попробуйте снова.')


def print_help():
    print('\n***Процесс работы с таблицей***')
    print('Функции:')
    print('<command> create_table <имя_таблицы> <столбец1:тип> .. '
          '- создать таблицу')
    print('<command> list_tables - показать список всех таблиц')
    print('<command> drop_table <имя_таблицы> - удалить таблицу')

    print('\n***Операции с данными***')
    print('Функции:')
    print('<command> insert into <имя_таблицы> values '
          '(<значение1>, <значение2>, ...) - создать запись.')
    print('<command> select from <имя_таблицы> where '
          '<столбец> = <значение> - прочитать записи по условию.')
    print('<command> select from <имя_таблицы> - прочитать все записи.')
    print('<command> update <имя_таблицы> set '
          '<столбец1> = <новое_значение1> where '
          '<столбец_условия> = <значение_условия> - обновить запись.')
    print('<command> delete from <имя_таблицы> where '
          '<столбец> = <значение> - удалить запись.')
    print('<command> info <имя_таблицы> - вывести информацию о таблице.')

    print('\nОбщие команды:')
    print(f'<command> {COMMAND_EXIT} - выход из программы')
    print(f'<command> {COMMAND_HELP} - справочная информация\n')


def __handle_create_table(metadata, args):
    if len(args) < 2:
        print('Некорректное значение: укажите имя таблицы и столбцы. '
              'Попробуйте снова.')
        return

    table_name, *columns = args
    try:
        metadata = create_table(metadata, table_name, columns)
    except ValueError as error:
        __print_error(error)
        return

    save_metadata(DB_META_FILE_NAME, metadata)
    save_table_data(table_name, [])
    columns_info = ', '.join(metadata[table_name]['columns'])
    print(f'Таблица "{table_name}" успешно создана '
          f'со столбцами: {columns_info}')


def __handle_drop_table(metadata, args):
    if len(args) != 1:
        print('Некорректное значение: укажите имя таблицы. '
              'Попробуйте снова.')
        return

    table_name = args[0]
    try:
        metadata = drop_table(metadata, table_name)
    except ValueError as error:
        print(f'Ошибка: {error}')
        return

    save_metadata(DB_META_FILE_NAME, metadata)
    print(f'Таблица "{table_name}" успешно удалена.')


def __handle_insert(metadata, user_input):
    try:
        table_name, values = __parse_insert_command(user_input)
    except ValueError as error:
        __print_error(error)
        return

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    table_data = load_table_data(table_name)
    try:
        table_data = insert(metadata, table_name, table_data, values)
    except ValueError as error:
        __print_error(error)
        return

    save_table_data(table_name, table_data)
    save_metadata(DB_META_FILE_NAME, metadata)
    new_id = table_data[-1]['ID']
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')


def __handle_select(metadata, user_input):
    try:
        table_name, where_clause = __parse_select_command(user_input)
    except ValueError as error:
        __print_error(error)
        return

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    table_data = load_table_data(table_name)
    rows = select(table_data, where_clause)
    __print_rows(rows, metadata[table_name]['columns'])


def __handle_update(metadata, user_input):
    try:
        table_name, set_clause, where_clause = __parse_update_command(user_input)
    except ValueError as error:
        __print_error(error)
        return

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    table_data = load_table_data(table_name)
    matched = select(table_data, where_clause)
    if not matched:
        print('Ошибка: подходящие записи не найдены.')
        return

    table_data = update(table_data, set_clause, where_clause)
    save_table_data(table_name, table_data)
    for row in matched:
        print(
            f'Запись с ID={row["ID"]} в таблице "{table_name}" '
            'успешно обновлена.'
        )


def __handle_delete(metadata, user_input):
    try:
        table_name, where_clause = __parse_delete_command(user_input)
    except ValueError as error:
        __print_error(error)
        return

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    table_data = load_table_data(table_name)
    matched = select(table_data, where_clause)
    if not matched:
        print('Ошибка: подходящие записи не найдены.')
        return

    table_data = delete(table_data, where_clause)
    save_table_data(table_name, table_data)
    for row in matched:
        print(
            f'Запись с ID={row["ID"]} успешно удалена '
            f'из таблицы "{table_name}".'
        )


def __handle_info(metadata, args):
    if len(args) != 1:
        print('Некорректное значение: укажите имя таблицы. '
              'Попробуйте снова.')
        return

    table_name = args[0]
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    table_data = load_table_data(table_name)
    columns_info = ', '.join(metadata[table_name]['columns'])
    print(f'Таблица: {table_name}')
    print(f'Столбцы: {columns_info}')
    print(f'Количество записей: {len(table_data)}')


def __parse_insert_command(user_input):
    prefix = 'insert into '
    marker = ' values '
    lowered = user_input.lower()
    if not lowered.startswith(prefix):
        raise ValueError(
            'Некорректное значение: ожидался формат '
            'insert into <имя_таблицы> values (...).'
        )

    rest = user_input[len(prefix):]
    marker_index = rest.lower().find(marker)
    if marker_index == -1:
        raise ValueError(
            'Некорректное значение: ожидался формат '
            'insert into <имя_таблицы> values (...).'
        )

    table_name = rest[:marker_index].strip()
    values_part = rest[marker_index + len(marker):].strip()
    if not table_name:
        raise ValueError('Некорректное значение: не указано имя таблицы.')
    if not (values_part.startswith('(') and values_part.endswith(')')):
        raise ValueError(
            'Некорректное значение: значения должны быть в скобках.'
        )

    values = parse_values(values_part[1:-1])
    return table_name, values


def __parse_select_command(user_input):
    prefix = 'select from '
    where_marker = ' where '
    lowered = user_input.lower()
    if not lowered.startswith(prefix):
        raise ValueError(
            'Некорректное значение: ожидался формат '
            'select from <имя_таблицы> [where ...].'
        )

    rest = user_input[len(prefix):]
    where_index = rest.lower().find(where_marker)
    if where_index == -1:
        table_name = rest.strip()
        if not table_name:
            raise ValueError('Некорректное значение: не указано имя таблицы.')
        return table_name, None

    table_name = rest[:where_index].strip()
    where_part = rest[where_index + len(where_marker):].strip()
    if not table_name:
        raise ValueError('Некорректное значение: не указано имя таблицы.')
    if not where_part:
        raise ValueError('Некорректное значение: пустое условие where.')

    return table_name, parse_where_clause(where_part)


def __parse_update_command(user_input):
    prefix = 'update '
    set_marker = ' set '
    where_marker = ' where '
    lowered = user_input.lower()
    if not lowered.startswith(prefix):
        raise ValueError(
            'Некорректное значение: ожидался формат '
            'update <имя_таблицы> set ... where ...'
        )

    rest = user_input[len(prefix):]
    set_index = rest.lower().find(set_marker)
    if set_index == -1:
        raise ValueError(
            'Некорректное значение: ожидался формат '
            'update <имя_таблицы> set ... where ...'
        )

    table_name = rest[:set_index].strip()
    after_set = rest[set_index + len(set_marker):]
    where_index = after_set.lower().find(where_marker)
    if where_index == -1:
        raise ValueError(
            'Некорректное значение: ожидался формат '
            'update <имя_таблицы> set ... where ...'
        )

    set_part = after_set[:where_index].strip()
    where_part = after_set[where_index + len(where_marker):].strip()
    if not table_name:
        raise ValueError('Некорректное значение: не указано имя таблицы.')
    if not set_part:
        raise ValueError('Некорректное значение: пустое условие set.')
    if not where_part:
        raise ValueError('Некорректное значение: пустое условие where.')

    return (
        table_name,
        parse_set_clause(set_part),
        parse_where_clause(where_part),
    )


def __parse_delete_command(user_input):
    prefix = 'delete from '
    where_marker = ' where '
    lowered = user_input.lower()
    if not lowered.startswith(prefix):
        raise ValueError(
            'Некорректное значение: ожидался формат '
            'delete from <имя_таблицы> where ...'
        )

    rest = user_input[len(prefix):]
    where_index = rest.lower().find(where_marker)
    if where_index == -1:
        raise ValueError(
            'Некорректное значение: ожидался формат '
            'delete from <имя_таблицы> where ...'
        )

    table_name = rest[:where_index].strip()
    where_part = rest[where_index + len(where_marker):].strip()
    if not table_name:
        raise ValueError('Некорректное значение: не указано имя таблицы.')
    if not where_part:
        raise ValueError('Некорректное значение: пустое условие where.')

    return table_name, parse_where_clause(where_part)


def __print_rows(rows, columns):
    field_names = [column.split(':', 1)[0] for column in columns]
    table = PrettyTable(field_names)
    for row in rows:
        table.add_row([row.get(name) for name in field_names])
    print(table)


def __print_error(error):
    message = str(error)
    if message.startswith('Некорректное значение:'):
        print(f'{message} Попробуйте снова.')
    else:
        print(f'Ошибка: {message}')
