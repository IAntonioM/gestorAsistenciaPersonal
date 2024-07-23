import sqlite3
from src.models.UserModel import User
from datetime import datetime

class UserSql:
    def __init__(self, nombre_archivo):
        self.conexion = sqlite3.connect(nombre_archivo)
        self.cursor = self.conexion.cursor()
        self.create_table_users()
        
    def create_table_users(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                fullNames TEXT NOT NULL,
                                password TEXT NOT NULL,
                                rol INTEGER NOT NULL
                            )''')
        self.conexion.commit()

    def insert_user(self, username, fullNames, password, rol):
        try:
            self.cursor.execute("INSERT INTO users (username, fullNames, password, rol) VALUES (?, ?, ?, ?)", (username, fullNames, password, rol))
            self.conexion.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al Registrar usuario: {e}")
            self.conexion.rollback()
            return False
    

    def get_user_by_username(self, username):
        self.cursor.execute("""
            SELECT u.id, u.username, u.fullNames, u.password, u.rol
            FROM users u
            WHERE u.username = ?
        """, (username,))
        result = self.cursor.fetchone()
        if result:
            id, username, fullNames, password, rol= result
            return User(id, username, fullNames, password, rol)
        else:
            return None
        
    def get_all(self):
        try:
            self.cursor.execute("""
                SELECT id, username, fullNames, password, rol
                FROM users
            """)
            results = self.cursor.fetchall()
            users = []
            for row in results:
                id, username, fullNames, password, rol = row
                users.append(User(id, username, fullNames, password, rol))
            return users
        except sqlite3.Error as e:
            print(f"Error al obtener todos los usuarios: {e}")
            return None
    
    def get_all_users(self):
            self.cursor.execute("SELECT * FROM users")
            return self.cursor.fetchall()
        
    def get_today_assistances(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("""
            SELECT * FROM asistencias
            WHERE fecha = ?
        """, (today,))
        return self.cursor.fetchall()
        
    def get_last_activity(self):
        self.cursor.execute("""
            SELECT a.* FROM asistencias a
            JOIN (
                SELECT id_horario, MAX(fecha) as last_date
                FROM asistencias
                GROUP BY id_horario
            ) last_ass ON a.id_horario = last_ass.id_horario AND a.fecha = last_ass.last_date
        """)
        return self.cursor.fetchall()
    
    def get_user_actividad(self):
        try:
            users = self.get_all_users()
            today_assistances = self.get_today_assistances()
            last_activities = self.get_last_activity()
            
            user_dict = {user[0]: user for user in users}
            today_assist_dict = {assist[4]: assist for assist in today_assistances}
            last_activity_dict = {activity[4]: activity for activity in last_activities}
            
            usuarios = []
            for user_id, user_data in user_dict.items():
                usuario = {
                    'id': user_data[0],
                    'username': user_data[1],
                    'fullNames': user_data[2],
                    'password': user_data[3],
                    'rol': user_data[4],
                    'hora_entrada': today_assist_dict.get(user_id, [None]*6)[1],
                    'hora_salida': today_assist_dict.get(user_id, [None]*6)[2],
                    'fecha': today_assist_dict.get(user_id, [None]*6)[3],
                    'horario_id': today_assist_dict.get(user_id, [None]*6)[4],
                    'ultima_hora_entrada': last_activity_dict.get(user_id, [None]*6)[1],
                    'ultima_hora_salida': last_activity_dict.get(user_id, [None]*6)[2],
                    'ultima_fecha': last_activity_dict.get(user_id, [None]*6)[3]
                }
                # Convertir datetime y time a string para JSON
                for key in ['hora_entrada', 'hora_salida', 'fecha', 'ultima_hora_entrada', 'ultima_hora_salida', 'ultima_fecha']:
                    if usuario[key] is not None and isinstance(usuario[key], (datetime, bytes)):
                        usuario[key] = usuario[key].strftime("%Y-%m-%d %H:%M:%S") if usuario[key] else None
                usuarios.append(usuario)
                
            return usuarios
        except sqlite3.Error as e:
            print(f"Error al obtener todos los usuarios y asistencias: {e}")
            return None
    
    def close(self):
        self.conexion.close()
    def username_exists(self, username):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
            count = self.cursor.fetchone()[0]
            return count > 0
        except sqlite3.Error as e:
            print(f"Error al verificar username: {e}")
            return False

    def close(self):
        self.conexion.close()

    