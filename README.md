# primitive-db

Консольная база данных. Можно создавать, смотреть и удалять таблицы, а также выполнять CRUD-операции с данными. Структура таблиц сохраняется в файл `db_meta.json`, данные каждой таблицы — в отдельном JSON-файле в директории `data/`.

## Управление таблицами

Сборка и установка:

```bash
uv build
uv tool install --force dist/*.whl
```

Запуск:

```bash
database
```

Команды:

- `create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...` — создать таблицу. Столбец `ID:int` добавляется автоматически, если его не указали.
- `list_tables` — показать список всех таблиц.
- `drop_table <имя_таблицы>` — удалить таблицу.
- `help` — показать справку.
- `exit` — выйти из программы.

Типы столбцов: `int`, `str`, `bool`.

Пример:

```text
$ database

***Процесс работы с таблицей***
Функции:
<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу

Общие команды:
<command> exit - выход из программы
<command> help - справочная информация

Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

Введите команду: create_table users name:str
Ошибка: Таблица "users" уже существует.

Введите команду: list_tables
- users

Введите команду: drop_table users
Таблица "users" успешно удалена.

Введите команду: drop_table products
Ошибка: Таблица "products" не существует.

Введите команду: exit
```

## Демонстрация

[![asciicast](https://asciinema.org/a/4C2bjFQJRTlmsgs5.svg)](https://asciinema.org/a/4C2bjFQJRTlmsgs5)

## CRUD-операции

Команды для работы с данными таблиц:

- `insert into <имя_таблицы> values (<значение1>, <значение2>, ...)` — создать запись. Столбец `ID` заполняется автоматически.
- `select from <имя_таблицы>` — прочитать все записи.
- `select from <имя_таблицы> where <столбец> = <значение>` — прочитать записи по условию.
- `update <имя_таблицы> set <столбец> = <новое_значение> where <столбец> = <значение>` — обновить запись.
- `delete from <имя_таблицы> where <столбец> = <значение>` — удалить запись.
- `info <имя_таблицы>` — вывести информацию о таблице.

Строковые значения в условиях и в `values` указывайте в кавычках.

Пример:

```text
$ database

Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

Введите команду: insert into users values ("Sergei", 28, true)
Запись с ID=1 успешно добавлена в таблицу "users".

Введите команду: select from users where age = 28
+----+--------+-----+-----------+
| ID |  name  | age | is_active |
+----+--------+-----+-----------+
| 1  | Sergei |  28 |    True   |
+----+--------+-----+-----------+

Введите команду: update users set age = 29 where name = "Sergei"
Запись с ID=1 в таблице "users" успешно обновлена.

Введите команду: delete from users where ID = 1
Запись с ID=1 успешно удалена из таблицы "users".

Введите команду: info users
Таблица: users
Столбцы: ID:int, name:str, age:int, is_active:bool
Количество записей: 0

Введите команду: exit
```

## Демонстрация

[![asciicast](https://asciinema.org/a/JpQEwmqFLjU5lqgE.svg)](https://asciinema.org/a/JpQEwmqFLjU5lqgE)
