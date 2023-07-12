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

@api.route('/GuardarMatch', methods=['POST'])
# @jwt_required() # Definiendo una ruta privada
def guardarMatch():
    print("Quiero entrar, eso es lo mejor")
    data = request.json
    print(data)
    print("¡Qué genial! Espero que esta función funcione correctamente")
    return jsonify({ "success": "Login successfully", "status": 200, "data": data}), 200

# @app.route("/api/match/like", methods=["POST"])
# def like_user():
#     emisor_id = request.json["emisor_id"]
#     receptor_id = request.json["receptor_id"]

#     # Verificar si ya existe un match entre el emisor y el receptor
#     existing_match = Match.query.filter(
#         (Match.id_usr_emisor == emisor_id) & (Match.id_usr_receptor == receptor_id)
#     ).first()

#     if existing_match:
#         # Si ya existe un match, actualizar el estado a 2
#         existing_match.estado = 2
#         db.session.commit()
#     else:
#         # Si no existe un match, crear uno nuevo con estado 1
#         new_match = Match(id_usr_emisor=emisor_id, id_usr_receptor=receptor_id, estado=1)
#         db.session.add(new_match)
#         db.session.commit()

#     # Crear un registro en MatchLog
#     match_log = MatchLog(id_match=existing_match.id_match if existing_match else new_match.id_match, id_usr_emisor=emisor_id, id_usr_receptor=receptor_id, estado=new_match.estado)
#     db.session.add(match_log)
#     db.session.commit()

#     return jsonify({"message": "Has dado un like"})

# @app.route("/api/match/unlike", methods=["POST"])
# def unlike_user():
#     emisor_id = request.json["emisor_id"]
#     receptor_id = request.json["receptor_id"]

#     # Verificar si existe un match entre el emisor y el receptor
#     existing_match = Match.query.filter(
#         (Match.id_usr_emisor == emisor_id) & (Match.id_usr_receptor == receptor_id)
#     ).first()

#     if existing_match:
#         # Actualizar el estado del match a 1
#         existing_match.estado = 1
#         db.session.commit()

#     return jsonify({"message": "Has eliminado el like"})



