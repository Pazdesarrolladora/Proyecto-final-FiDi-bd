from flask import Blueprint, jsonify, request
from models.habilidad import Habilidad
from models.chat import Chat

api = Blueprint('api_chats', __name__)

@api.route('/chat', methods=['GET'])
def listarMensajes():
    chat = Chat.query.all()
    return jsonify(chat)
