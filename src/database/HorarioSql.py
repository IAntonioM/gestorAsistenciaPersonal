import sqlite3
from src.models.HorarioModel import Horario
class HorarioSql:
    def __init__(self, nombre_archivo):
        self.conexion = sqlite3.connect(nombre_archivo)
        self.cursor = self.conexion.cursor()
        self.create_table_horarios()
        
    def create_table_horarios(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS horarios (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                hora_inicio TIME NOT NULL,
                                hora_salida TIME NOT NULL,
                                dias_trabajo TEXT NOT NULL,
                                id_user INTEGER,
                                FOREIGN KEY (id_user) REFERENCES users(id)
                            )''')
        self.conexion.commit()

    def insert_horario(self,inicio, salida, dias_trabajo_json, id_user):
        try:
            self.cursor.execute('''
                INSERT INTO horarios (hora_inicio, hora_salida, dias_trabajo, id_user)
                VALUES ( ?, ?, ?, ?)
            ''', (
                inicio.strftime('%H:%M'),
                salida.strftime('%H:%M'),
                dias_trabajo_json,
                id_user
            ))
            self.conexion.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al insertar horario: {e}")
            return False

    def get_horario_by_userId(self, id):
        self.cursor.execute("""
            SELECT h.id, h.hora_inicio, h.hora_salida, h.dias_trabajo, h.id_user
            FROM horarios h
            WHERE h.id_user= ?
        """, (id,))
        result = self.cursor.fetchone()
        if result:
            id, hora_inicio, hora_salida, dias_trabajo, user_id = result
            return Horario(id, hora_inicio, hora_salida, dias_trabajo, user_id)
        else:
            return None

    def get_horario_by_id(self, id):
        self.cursor.execute("""
            SELECT h.id, h.hora_inicio, h.hora_salida, h.dias_trabajo, h.id_user
            FROM horarios h
            WHERE h.id = ?
        """, (id,))
        result = self.cursor.fetchone()
        if result:
            id, hora_inicio, hora_salida, dias_trabajo = result
            return Horario(id, hora_inicio, hora_salida, dias_trabajo)
        else:
            return None
    
    def close(self):
        self.conexion.close()