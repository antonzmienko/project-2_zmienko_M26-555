def parse_where_clause(clause):
    return __parse_assignments(clause)


def parse_set_clause(clause):
    return __parse_assignments(clause)


def parse_values(values_clause):
    if not values_clause or not values_clause.strip():
        raise ValueError('Некорректное значение: пустой список значений.')

    return [__parse_value(part) for part in __split_assignments(values_clause)]


def __parse_assignments(clause):
    if not clause or not clause.strip():
        raise ValueError('Некорректное значение: пустое условие.')

    result = {}
    for part in __split_assignments(clause):
        column, value = __parse_assignment(part)
        result[column] = value
    return result


def __split_assignments(clause):
    parts = []
    current = []
    quote = None

    for char in clause:
        if quote is None and char in ('"', "'"):
            quote = char
            current.append(char)
        elif quote is not None and char == quote:
            quote = None
            current.append(char)
        elif char == ',' and quote is None:
            part = ''.join(current).strip()
            if part:
                parts.append(part)
            current = []
        else:
            current.append(char)

    if quote is not None:
        raise ValueError('Некорректное значение: незакрытые кавычки.')

    part = ''.join(current).strip()
    if part:
        parts.append(part)

    if not parts:
        raise ValueError('Некорректное значение: пустое условие.')

    return parts


def __parse_assignment(part):
    if '=' not in part:
        raise ValueError(f'Некорректное значение: {part}.')

    column, raw_value = part.split('=', 1)
    column = column.strip()
    raw_value = raw_value.strip()

    if not column or not raw_value:
        raise ValueError(f'Некорректное значение: {part}.')

    return column, __parse_value(raw_value)


def __parse_value(raw_value):
    if (
        len(raw_value) >= 2
        and raw_value[0] == raw_value[-1]
        and raw_value[0] in ('"', "'")
    ):
        return raw_value[1:-1]

    lowered = raw_value.lower()
    if lowered == 'true':
        return True
    if lowered == 'false':
        return False

    try:
        return int(raw_value)
    except ValueError:
        raise ValueError(
            f'Некорректное значение: {raw_value}. '
            'Строковые значения указывайте в кавычках.'
        )
