from src.models.UserModel import User
from src.database.UserSql import UserSql

from flask_jwt_extended import create_access_token,jwt_required
import bcrypt
import json
class UsuarioService:
    def __init__(self):
        pass
    

    def get_users_asistencia():
            user_db = UserSql("asistencia.db")
            try:
                usuarios = user_db.get_user_actividad()
                if not usuarios:
                    return False, "No se encontraron usuarios"
                usuarios_serializados = [
                    {
                        "id": usuario['id'],
                        "username": usuario['username'],
                        "fullNames": usuario['fullNames'],
                        "rol": usuario['rol'],
                        "hora_entrada": usuario['hora_entrada'],
                        "hora_salida": usuario['hora_salida'],
                        "fecha": usuario['fecha'],
                        "horario_id": usuario['horario_id'],
                        "ultima_hora_entrada": usuario['ultima_hora_entrada'],
                        "ultima_hora_salida": usuario['ultima_hora_salida'],
                        "ultima_fecha": usuario['ultima_fecha']
                    }
                    for usuario in usuarios
                ]
                
                return usuarios_serializados, "Usuarios obtenidos exitosamente"
            except Exception as e:
                return False, f"Error al obtener la lista de usuarios: {str(e)}"
            finally:
                user_db.close()