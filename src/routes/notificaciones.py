from models import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.usuario import Usuario
from models.notificacion import Notificacion

api = Blueprint('api_notificaciones', __name__)

# @api.route('/notificaciones/crear/usuario/<int:idFront>', methods=['POST'])
# @jwt_required()
# def crear_notificacion(idFront):
#     id = get_jwt_identity()
    
#     notificacion_emisor = Notificacion() #notificacion para usuario 1 emisor
#     notificacion_emisor.mensaje = 'Match'
#     notificacion_emisor.id_emisor = id
#     notificacion_emisor.id_receptor = idFront 
#     notificacion_emisor.save()

#     notificacion_receptor = Notificacion() #notificacion para usuario 1 receptor
#     notificacion_receptor.mensaje = 'Match'
#     notificacion_receptor.id_emisor = idFront
#     notificacion_receptor.id_receptor = id
#     notificacion_receptor.save()
    
#     return jsonify({"success": "Usuario creado Satisfactoriamente"})

@api.route('/notificaciones/recibir/notificacion', methods=['GET'])
@jwt_required()
def obtener_notificacion():
    id = get_jwt_identity()

    comprobar = Notificacion.query.filter(Notificacion.id_emisor == id).all()
    if comprobar: 
        comprobar = list(map(lambda aux1: aux1.serialize(), comprobar))
        print(comprobar)
        

    return jsonify({"success": "Hay Notificaciones", "notificaciones": comprobar}), 201