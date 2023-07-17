from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import db
from models.usuario import Usuario
from models.habilidad import Habilidad
from models.registroHabilidad import RegistroHabilidad

api = Blueprint('api_settings', __name__)

@api.route('/settings/modificarHabilidad/<int:idFront>/agregar', methods=['POST'])
@jwt_required() # Definiendo una ruta privada
def modificarHabilidadesUsuario(idFront):
    point = 0
    def agregarHabilidad(agregado, tipo, point):
        #Validacion si vienen datos desde el front para Habilidades Agregadas
        if not agregado in request.form: 
            point += 1
        else: 
            habilidades_agregadas_raw = request.form[agregado]
            if habilidades_agregadas_raw != '':
                print(habilidades_agregadas_raw)
                habilidades_agregadas = [int(i) for i in habilidades_agregadas_raw.split(',')]
                for id_habilidad in habilidades_agregadas:
                    new_register = RegistroHabilidad()
                    new_register.id_usuario = idFront
                    new_register.id_habilidad = id_habilidad
                    new_register.tipo = tipo
                    new_register.save()

    agregarHabilidad('habilidades_agregadas', 'Habilidad', point)
    agregarHabilidad('intereses_agregados', 'Interes', point)

    #Validacion si vienen datos desde el front para Habilidades Eliminadas
    # if not 'habilidades_eliminadas' in request.form: 
    #     print('No hay habilidades Eliminadas')
    #     point += 1
    # else: 
    #     habilidades_eliminadas_raw = request.form['habilidades_eliminadas']
    #     if habilidades_eliminadas_raw != '':
    #         print(habilidades_eliminadas_raw)
    #         habilidades_eliminadas = [int(i) for i in habilidades_eliminadas_raw.split(',')]

    if point == 2: return jsonify({ "message": "No has modificado nada!"}), 400


    return jsonify({"success":"habilidades Modificadas"}), 200


@api.route('/settings/modificarHabilidad/<int:idFront>/eliminar', methods=['DELETE'])
@jwt_required()
def eliminarHabilidadesUsuario(idFront):
    point = 0
    def eliminarHabilidad(agregado, point):
        #Validacion si vienen datos desde el front para Habilidades Agregadas
        if not agregado in request.form: 
            point += 1
        else: 
            habilidades_agregadas_raw = request.form[agregado]
            if habilidades_agregadas_raw != '':
                print(habilidades_agregadas_raw)
                habilidades_agregadas = [int(i) for i in habilidades_agregadas_raw.split(',')]
                for id in habilidades_agregadas:
                    registro = RegistroHabilidad.query.filter_by(id_usuario=idFront, id_habilidad=id).first()
                    registro.delete()

    eliminarHabilidad('habilidades_eliminadas', point)
    eliminarHabilidad('intereses_eliminados', point)

    if point == 2: return jsonify({ "warning": "No has Eliminado ninguna Habilidad!"}), 400

    return jsonify({"success":"habilidades elimindas"}), 200