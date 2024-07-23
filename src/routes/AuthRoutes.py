from flask import Blueprint, request, jsonify
from src.models.UserModel import User
from src.services.AuthService import AuthService

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data=request.get_json()
    username=data.get("username")
    password=data.get("password")
    if not (username and password):
        return jsonify({'msg': 'Las credenciales del usuario estan incompletas'}), 400
    token,msg=AuthService.login(username,password)
    if token:
        return jsonify({'token':token}), 200
    else:
        return jsonify({'msg':msg}), 401



@auth_bp.route('/register', methods=['POST'])
def register():
    data=request.get_json()
    username=data.get("username")
    fullNames=data.get("fullNames")
    password=data.get("password")
    rol=data.get("rol")
    if not (username and password and fullNames and rol):
        return jsonify({'error': 'Datos de registro incompleto'}), 400
    sucess,msg = AuthService.register(username, fullNames, password, rol)
    if not sucess:
        return jsonify({'error': msg}), 500
    return jsonify({'success': msg}), 200

