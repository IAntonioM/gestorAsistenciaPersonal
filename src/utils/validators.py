from datetime import datetime
import re
import json


def validate_date(date_string):
    """Valida que la fecha esté en formato DD/MM/YYYY."""
    try:
        return datetime.strptime(date_string, '%d/%m/%Y').date()
    except ValueError:
        return None

def validate_time(time_string):
    """Valida que la hora esté en formato HH:MM."""
    try:
        return datetime.strptime(time_string, '%H:%M').time()
    except ValueError:
        return None

def validate_dias_trabajo(dias):
    """Valida que los días de trabajo sean una lista de días válidos."""
    valid_dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    if not isinstance(dias, list):
        return None
    return [dia.lower() for dia in dias if dia.lower() in valid_dias]

def validate_id(id_value):
    """Valida que el ID sea un número entero positivo."""
    try:
        id_int = int(id_value)
        return id_int if id_int > 0 else None
    except ValueError:
        return None

def dias_trabajo_to_json(dias_trabajo):
    """Convierte la lista de días de trabajo a JSON."""
    if not isinstance(dias_trabajo, list):
        return None
    return json.dumps(dias_trabajo)

def dias_trabajo_from_json(dias_trabajo_json):
    """Convierte el JSON de días de trabajo a lista."""
    try:
        dias = json.loads(dias_trabajo_json)
        return dias if isinstance(dias, list) else None
    except json.JSONDecodeError:
        return None

def validate_id(id_value):
    """Valida que el ID sea un número entero positivo."""
    try:
        id_int = int(id_value)
        return id_int if id_int > 0 else None
    except ValueError:
        return None

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None

def validate_password_strength(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True

def validate_username(username):
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, username) is not None

def validate_name(name):
    pattern = r'^[a-zA-Z\s-]+$'
    return re.match(pattern, name) is not None

def validate_id(id_value):
    try:
        id_int = int(id_value)
        return id_int > 0
    except ValueError:
        return False