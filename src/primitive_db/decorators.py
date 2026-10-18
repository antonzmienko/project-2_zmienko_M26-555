import time

import prompt


def handle_db_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                'Ошибка: Файл данных не найден. '
                'Возможно, база данных не инициализирована.'
            )
        except KeyError as e:
            print(f'Ошибка: Таблица или столбец {e} не найден.')
        except UnicodeError as e:
            print(f'Ошибка кодировки: {e}')
        except ValueError as e:
            print(f'Ошибка валидации: {e}')
        except Exception as e:
            print(f'Произошла непредвиденная ошибка: {e}')
    return wrapper


def confirm_action(action_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            answer = prompt.string(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ',
                empty=True,
            )
            if answer.strip().lower() != 'y':
                print('Операция отменена.')
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_time(func):
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.monotonic() - start
            print(
                f'Функция {func.__name__} выполнилась за {elapsed:.3f} секунд.'
            )
    return wrapper
