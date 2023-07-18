from models import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.usuario import Usuario
from models.notificacion import Notificacion

api = Blueprint('api_notificaciones', __name__)

@api.route('/notificaciones/recibir/notificacion', methods=['GET'])
@jwt_required()
def obtener_notificacion():
    id = get_jwt_identity()

    comprobar = Notificacion.query.filter(Notificacion.id_emisor == id).all()
    if comprobar: 
        comprobar = list(map(lambda aux1: aux1.serialize(), comprobar))
        print(comprobar)
        

    return jsonify({"success": "Hay Notificaciones", "notificaciones": comprobar}), 201