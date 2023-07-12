from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from models.registroHabilidad import RegistroHabilidad
from models.habilidad import Habilidad

api = Blueprint('api_registrosHabilidades', __name__)

# @api.route('/profile', methods=['GET'])
# def obtenerHabilidadesUsuario():
   