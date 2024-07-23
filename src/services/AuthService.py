from src.models.UserModel import User
from src.database.UserSql import UserSql
from flask_jwt_extended import create_access_token,jwt_required
import bcrypt
class AuthService:
    def __init__(self):
        pass
    
    def login(username, password):
        user_db = UserSql("asistencia.db")
        user=user_db.get_user_by_username(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            claims={"rol":user.rol}
            jwt_token=create_access_token(identity=username,additional_claims=claims)
            return jwt_token, "Inicio de Sesion Exitoso"
        
        else:
            return False, "Credenciales Incorrectas"

    def register(username, fullNames, password, rol):
        user_db = UserSql("asistencia.db")
        try:
            if user_db.username_exists(username):
                return False, f"El username {username} ya esta registrado"
            
            hash_passwrod=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
            success=user_db.insert_user(username, fullNames, hash_passwrod, rol)
            if not success:
                return False, "No se completo el registro"
            
            return True, "Registro exitoso"
        finally:
            user_db.close()
    