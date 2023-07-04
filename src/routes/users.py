from flask import Blueprint, jsonify, request
from models.usuario import Usuario

api = Blueprint('api_users', __name__)

@api.route('/users', methods=['GET'])
def list_users():
    
    users = Usuario.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200

@api.route('/formulario', methods=['POST'])
def formulario_user():
    data=request.get_json()
    new_user = Usuario() 
    new_user.username = data['nombre']
    new_user.email=data['correo']
    new_user.password=data['contraseña']
    new_user.id_habilidades =data ["habilidades.id"]
    new_user.id_interes = data["habilidades.id"]
    new_user.id_roles =data ["roles.id"]
    new_user.save()


    return jsonify(message='Ya puedes disfrutar de FiDi'), 201
