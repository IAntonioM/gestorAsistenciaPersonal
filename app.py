from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from src.routes.AuthRoutes import auth_bp
from src.routes.HorarioRoute import horario_bp
from src.routes.UsuarioRoute import usuario_bp
from src.routes.AsistenciaRoute import asistencia_bp

from src.database.UserSql import UserSql
from src.database.HorarioSql import HorarioSql


app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'clave_12323_1'
jwt = JWTManager(app)

db_user= UserSql("asistencia.db")
db_horario = HorarioSql("asistencia.db")

@app.route('/')
def index():
    return 'hello world'

app.register_blueprint(auth_bp)
app.register_blueprint(horario_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(asistencia_bp)

if __name__ == '__main__':
    app.run(debug=True)

