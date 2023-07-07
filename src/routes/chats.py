from flask import Blueprint, jsonify, request
from models.habilidad import Habilidad
from models.usuario import Usuario
from models.mensaje import Mensaje
from models.chat import Chat

api = Blueprint('api_chats', __name__)

@api.route('/chat/<int:id>', methods=['GET'])
def listarMensajes():
    chat = Chat.query.get(id)
    return jsonify(chat)

@api.route('/chat/<int:id1>/<int:id2>', methods=['GET'])
def show_role(id1, id2):
    
    # mensajes1 = Mensaje.query.get(id1)
    # mensajes2 = Mensaje.query.get(id2)

    # mensaje = list(map(lambda user: user.username, mensaje.users))
    # info = {
    #     "role": role.serialize()
    # }
    # info["users"] = users
   
    return jsonify(info), 200