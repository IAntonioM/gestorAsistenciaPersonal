from src.models.AsistenciaModel import Asistencia
from src.database.AsistenciaSql import AsistenciaSql
from src.database.HorarioSql import HorarioSql
from datetime import datetime
from flask_jwt_extended import create_access_token,jwt_required
import bcrypt
import json
class AsistenciaService:
    def __init__(self):
        pass
    

    def register_in(id_user):
        asistencia_db = AsistenciaSql("asistencia.db")
        horario_db = HorarioSql("asistencia.db")
        try:
            now = datetime.now()
            fecha_str = now.strftime('%Y-%m-%d')
            asistencia= asistencia_db.get_asistencia_by_fecha(fecha_str,id_user)
            if asistencia :
                return False, "Ya se Registro la Hora de Ingreso"

            hora_entrada_str = now.strftime('%H:%M:%S')
            horario= horario_db.get_horario_by_userId(id_user)

            if not horario:
                return False, "No existe el usuario o horario registrado"
            
            asistencia= asistencia_db.insert_asistencia(hora_entrada_str,None,fecha_str,horario.id)
            if not asistencia:
                return False, "No se completo el registro de ingreso"
            
            return True, f"Se registro la Hora de Ingreso exitosamente, por el user : {id_user}"
        finally:
            asistencia_db.close()
    

    def register_out(id_user):
        asistencia_db = AsistenciaSql("asistencia.db")
        try:
            now = datetime.now()
            fecha_str = now.strftime('%Y-%m-%d')
            asistencia= asistencia_db.get_asistencia_by_fecha(fecha_str,id_user)
            if not asistencia:
                return False, "No se encontro un registro con esta Fecha ni ingresada"
            hora_salida_str = now.strftime('%H:%M:%S')
            asistencia= asistencia_db.update_hora_salida(asistencia.id, hora_salida_str)
            if not asistencia:
                return False, "No se completo el registro de salida"
            
            return True, f"Se registro la Hora de Salida exitosamente, por el user : {id_user}"
        finally:
            asistencia_db.close()
    