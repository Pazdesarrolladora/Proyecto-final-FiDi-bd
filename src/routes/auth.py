from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from models.usuario import Usuario
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api_auth', __name__)

@api.route('/login', methods=['POST'])
def login():
    
    correo = request.json.get('correo')
    password = request.json.get('password')
    
    if not correo: return jsonify({ "correo": "El correo es requerido!"}), 400
    if not password: return jsonify({ "password": "Password is required!"}), 400
    
    userFound = Usuario.query.filter_by(correo=correo).first()
    
    if not userFound: return jsonify({ "message": "correo/password is incorrect"}), 401
    
    if not check_password_hash(userFound.password, password):
        return jsonify({ "message": "El correo o password es incorrecto"}), 401
    
    acces_token = create_access_token(identity=userFound["id"])
    
    data = {
        "access_token": acces_token,
        "user": userFound.serialize()
    }
    
    return jsonify(data), 200
    
    
@api.route('/register', methods=['POST'])
def register():
    # code to register users
    pass