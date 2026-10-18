import shlex

import prompt

from primitive_db.core import (
    DB_META_FILE_NAME,
    create_table,
    drop_table,
    list_tables,
)
from primitive_db.utils import load_metadata, save_metadata

COMMAND_EXIT = 'exit'
COMMAND_HELP = 'help'
COMMAND_CREATE_TABLE = 'create_table'
COMMAND_DROP_TABLE = 'drop_table'
COMMAND_LIST_TABLES = 'list_tables'


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
        else:
            print(f'Функции {command} нет. Попробуйте снова.')


def print_help():
    print('\n***Процесс работы с таблицей***')
    print('Функции:')
    print('<command> create_table <имя_таблицы> <столбец1:тип> .. '
          '- создать таблицу')
    print('<command> list_tables - показать список всех таблиц')
    print('<command> drop_table <имя_таблицы> - удалить таблицу')

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
        message = str(error)
        if message.startswith('Некорректное значение:'):
            print(f'{message} Попробуйте снова.')
        else:
            print(f'Ошибка: {message}')
        return

    save_metadata(DB_META_FILE_NAME, metadata)
    columns_info = ', '.join(metadata[table_name])
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
