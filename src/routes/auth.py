from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.usuario import Usuario
from werkzeug.security import check_password_hash

api = Blueprint('api_auth', __name__)

@api.route('/loginform', methods=['POST'])
def login():
    
    correo = request.json.get('correo')
    password = request.json.get('password')
    
    if not correo: return jsonify({ "correo": "El correo es requerido!"}), 400
    if not password: return jsonify({ "password": "La contraseña es requerido!"}), 400
    
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
    return jsonify({ "message": "Private Route", "usuario": userFound.serialize() }), 200