from datetime import datetime

def format_value(value):
    if value is None:
        return 'NULL'
    elif isinstance(value, datetime):
        return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"
    elif isinstance(value, str):
        return f"'{value}'"
    else:
        return str(value)