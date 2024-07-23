from flask import Blueprint, request, jsonify
from src.models.UserModel import User
from src.services.HorarioService import HorarioService
from src.utils.validators import validate_date,validate_time,validate_dias_trabajo
horario_bp = Blueprint('horario_bp', __name__)

@horario_bp.route('/horario', methods=['POST'])
def register():
    data = request.get_json()
    inicio = validate_time(data.get("hora_inicio"))
    salida = validate_time(data.get("hora_salida"))
    dias_trabajo = data.get("dias_trabajo")
    print(f"{dias_trabajo}")
    dias_trabajo = validate_dias_trabajo(data.get("dias_trabajo"))
    print(f"{dias_trabajo}")
    id_user = data.get("id_user") # Usa la función validate_id

    if not all([inicio, salida, dias_trabajo, id_user]):
        return jsonify({'msg': 'Los datos de Horario están incompletos o son inválidos'}), 400
    
    success, msg = HorarioService.register(inicio, salida, dias_trabajo, id_user)
    if success:
        return jsonify({'msg': msg}), 200
    else:
        return jsonify({'msg': msg}), 400