from flask import Blueprint, jsonify, request
# from models import db, Match, MatchLog
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.usuario import Usuario
from models.habilidad import Habilidad
from models.registroHabilidad import RegistroHabilidad
from werkzeug.security import check_password_hash

api = Blueprint('api_auth', __name__)

@api.route('/loginform', methods=['POST'])
def login():
    
    correo = request.json.get('correoLogin')
    password = request.json.get('passwordLogin')
    
    if not correo: return jsonify({ "message": "El correo es requerido!"}), 400
    if not password: return jsonify({ "message": "La contraseña es requerido!"}), 400
    
    userFound = Usuario.query.filter_by(correo=correo).first()
    
    if not userFound: return jsonify({ "message": "correo/password is incorrect"}), 401
    
    if not check_password_hash(userFound.password, password):
        return jsonify({ "message": "El correo o password es incorrecto"}), 401
    
    access_token = create_access_token(identity=userFound.id)
    
    data = {
        "access_token": access_token,
        "user": userFound.serialize()
    }
    
    return jsonify({ "success": "Login successfully", "status": 200, "data": data}), 200
    
    
@api.route('/profile', methods=['GET'])
@jwt_required() # Definiendo una ruta privada
def profiles():

    id = get_jwt_identity()
    userFound = Usuario.query.get(id)

    return jsonify({ "message": "Perfil Privado", "usuario": userFound.serialize()}), 200

@api.route('/listarUsuarios', methods=['GET'])
@jwt_required() # Definiendo una ruta privada
def listarUsuarios():
    id = get_jwt_identity()
    userFound = Usuario.query.all()
    userFound = list(map(lambda user: user.serialize(), userFound))
    return jsonify({ "message": "Perfil Privado", "usuario": userFound }), 200

@api.route('/GuardarMatch', methods=['POST'])
@jwt_required() # Definiendo una ruta privada
def guardarMatch():
    print("Quiero entrar, eso es lo mejor")
    data = request.json
    print("¡Qué genial! Espero que esta función funcione correctamente")
    return jsonify({ "success": "Login successfully", "status": 200, "data": data}), 200