from flask import Blueprint, request, jsonify
from src.models.UserModel import User
from src.services.UsuarioService import UsuarioService
from src.utils.validators import validate_date,validate_time,validate_dias_trabajo
usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuario/all', methods=['GET'])
def getAll():
    usuarios, msg = UsuarioService.get_users_asistencia()
    if usuarios:
        return jsonify({'usuarios': usuarios}), 200
    else:
        return jsonify({'msg': msg}), 400