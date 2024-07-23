import sqlite3
from src.models.AsistenciaModel import Asistencia
class AsistenciaSql:
    def __init__(self, nombre_archivo):
        self.conexion = sqlite3.connect(nombre_archivo)
        self.cursor = self.conexion.cursor()
        self.create_table_asistencia()
        
    def create_table_asistencia(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS asistencias (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                hora_entrada TIME NOT NULL,
                                hora_salida TIME,
                                fecha DATE NOT NULL,
                                id_horario INTEGER,
                                FOREIGN KEY (id_horario) REFERENCES horarios(id)
                            )''')
        self.conexion.commit()

    def insert_asistencia(self,hora_entrada, hora_salida,fecha, id_horario):
        try:
            self.cursor.execute('''
                INSERT INTO asistencias (hora_entrada, hora_salida,fecha, id_horario)
                VALUES ( ?, ?, ?, ?)
            ''', (
                hora_entrada,
                hora_salida,
                fecha,
                id_horario,
            ))
            self.conexion.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al insertar asistencia: {e}")
            return False
        
    def update_hora_salida(self, id_asistencia, hora_salida):
        try:
            self.cursor.execute('''
                UPDATE asistencias
                SET hora_salida = ?
                WHERE id = ?
            ''', (hora_salida, id_asistencia))
            self.conexion.commit()
            
            # Verificar si se actualizó algún registro
            if self.cursor.rowcount > 0:
                return True
            else:
                print(f"No se encontró asistencia con ID {id_asistencia}")
                return False
        except sqlite3.Error as e:
            print(f"Error al actualizar hora de salida: {e}")
            return False

    def get_asistencia_by_fecha(self, fecha, id_user):
        self.cursor.execute("""
            SELECT a.id, a.hora_entrada, a.hora_salida, a.fecha, a.id_horario
            FROM asistencias a
            INNER JOIN horarios h ON a.id_horario=h.id
            INNER JOIN users u ON h.id_user=u.id
            WHERE a.fecha= ? AND h.id_user= ?
        """, (fecha, id_user,))
        result = self.cursor.fetchone()
        if result:
            id, hora_entrada, hora_salida, fecha, id_horario = result
            return Asistencia(id, id_horario, hora_entrada, hora_salida, fecha)
        else:
            return None


    # def get_horario_by_userId(self, id):
    #     self.cursor.execute("""
    #         SELECT h.id, h.hora_inicio, h.hora_salida, h.dias_trabajo, h.id_user
    #         FROM horarios h
    #         WHERE h.id_user= ?
    #     """, (id,))
    #     result = self.cursor.fetchone()
    #     if result:
    #         id, hora_inicio, hora_salida, dias_trabajo, user_id = result
    #         return Horario(id, hora_inicio, hora_salida, dias_trabajo, user_id)
    #     else:
    #         return None

    # def get_horario_by_id(self, id):
    #     self.cursor.execute("""
    #         SELECT h.id, h.hora_inicio, h.hora_salida, h.dias_trabajo, h.id_user
    #         FROM horarios h
    #         WHERE h.id = ?
    #     """, (id,))
    #     result = self.cursor.fetchone()
    #     if result:
    #         id, hora_inicio, hora_salida, dias_trabajo = result
    #         return Horario(id, hora_inicio, hora_salida, dias_trabajo)
    #     else:
    #         return None
    
    def close(self):
        self.conexion.close()