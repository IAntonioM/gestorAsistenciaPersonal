from src.models.HorarioModel import Horario
from src.database.HorarioSql import HorarioSql

from flask_jwt_extended import create_access_token,jwt_required
import bcrypt
import json
class HorarioService:
    def __init__(self):
        pass
    

    def register(hora_inicio, hora_salida, dias_trabajo,id_user):
        horario_db = HorarioSql("asistencia.db")
        try:
            horario= horario_db.get_horario_by_userId(id_user)
            if horario:
                return False, "Este usuario ya tiene un horario"
            success=horario_db.insert_horario(hora_inicio, hora_salida, json.dumps(dias_trabajo), id_user)
            if not success:
                return False, "No se completo el registro"
            
            return True, f"Horario Registrador para el user : {id_user}"
        finally:
            horario_db.close()
    