from flask import Blueprint, request, jsonify
from src.models.AsistenciaModel import Asistencia
from src.services.AsistenciaService import AsistenciaService
from src.utils.validators import validate_date,validate_time,validate_dias_trabajo
asistencia_bp = Blueprint('asistencia_bp', __name__)

@asistencia_bp.route('/asistencia/ingreso', methods=['POST'])
def ingreso():
    data = request.get_json()
    id_user = data.get("id_user")
    if not all([id_user]):
        return jsonify({'msg': 'Los datos para registrar Ingreso, estan incompletos'}), 400
    
    success, msg = AsistenciaService.register_in(id_user)
    if success:
        return jsonify({'msg': msg}), 200
    else:
        return jsonify({'msg': msg}), 400
    

@asistencia_bp.route('/asistencia/salida', methods=['POST'])
def salida():
    data = request.get_json()
    id_user = data.get("id_user")
    if not all([id_user]):
        return jsonify({'msg': 'Los datos para registrar Salida, estan incompletos'}), 400
    
    success, msg = AsistenciaService.register_out(id_user)
    if success:
        return jsonify({'msg': msg}), 200
    else:
        return jsonify({'msg': msg}), 400