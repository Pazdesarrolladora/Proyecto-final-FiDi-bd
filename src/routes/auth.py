from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.usuario import Usuario
from models.habilidad import Habilidad
from models.registroHabilidad import RegistroHabilidad
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
    arrayNombresHab = []
    arrayNombresInt = []
    userFound = Usuario.query.get(id)
    habilidades = RegistroHabilidad.query.filter_by(id_usuario=id, tipo='Habilidad').all()
    habilidades = list(map(lambda habilidad: habilidad.id_habilidad, habilidades))

    for idHab in habilidades:
        nombreHabilidad = Habilidad.query.get(idHab)
        if nombreHabilidad:
            arrayNombresHab.append(nombreHabilidad)

    arrayNombresHab = list(map(lambda habNom: habNom.descripcion, arrayNombresHab))
    print(habilidades)
    print(arrayNombresHab)

    intereses = RegistroHabilidad.query.filter_by(id_usuario=id, tipo='Interes').all()
    intereses = list(map(lambda interes: interes.id_habilidad, intereses))

    for idInt in intereses:
        nombreHabilidad = Habilidad.query.get(idInt)
        if nombreHabilidad:
            arrayNombresInt.append(nombreHabilidad)

    arrayNombresInt = list(map(lambda habInt: habInt.descripcion, arrayNombresInt))
    print(intereses)
    print(arrayNombresInt)

    return jsonify({ "message": "Perfil Privado", "usuario": userFound.serialize(), "habilidades": arrayNombresHab, "intereses": arrayNombresInt }), 200


@api.route('/listarUsuarios', methods=['GET'])
@jwt_required() # Definiendo una ruta privada
def listarUsuarios():
    id = get_jwt_identity()
    print(id)
    userFound = Usuario.query.all()
    userFound = list(map(lambda user: user.serialize(), userFound))
    print(userFound)
    return jsonify({ "message": "Private Route", "usuario": userFound }), 200