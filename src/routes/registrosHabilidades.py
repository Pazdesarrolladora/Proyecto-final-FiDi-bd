from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.usuario import Usuario
from models.registroHabilidad import RegistroHabilidad
from models.habilidad import Habilidad

api = Blueprint('api_registrosHabilidades', __name__)

@api.route('/usuario/habilidades', methods=['GET'])
@jwt_required()
def obtenerHabilidadesUsuario():
    id = get_jwt_identity()

    #Inicializo variables para guardar las habilidades y los intereses
    arrayHabilidad = []
    arrayInteres = []
    
    #Filtro en el registro de habilidades por id de usuario (id_usuario) y tipo habilidad (Habilidad), me trae todos los encontrados
    #Las habilidades las convierto a listas y por cada habilidad encontrada, guarda el id de la habilidad.
    habilidades = RegistroHabilidad.query.filter_by(id_usuario=id, tipo='Habilidad').all()
    habilidades = list(map(lambda habilidad: habilidad.id_habilidad, habilidades))

    #print('habilidades', habilidades)

    #Este loop, por cada id en la lista de habilidades, busca dentro de los registros de Habilidad, ese id
    #Si este existe, se agrega al arrayHabilidad inicializado mas arriba
    for idHab in habilidades:
        nombreHabilidad = Habilidad.query.get(idHab)
        if nombreHabilidad:
            arrayHabilidad.append(nombreHabilidad)

    #A este arrayHabilidad lo ordenare como una lista, y por cada uno le pasare el serialize() para ordenarlos como diccionarios
    #Asi los envio mas tarde en 'data' para mandarlos como .json
    arrayHabilidad = list(map(lambda habNom: habNom.serialize(), arrayHabilidad))

    #-------------------------------------------------------------------------------------------------------------------
    #Lo mismo que arriba pero para los intereses

    intereses = RegistroHabilidad.query.filter_by(id_usuario=id, tipo='Interes').all()
    intereses = list(map(lambda interes: interes.id_habilidad, intereses))


    for idInt in intereses:
        nombreHabilidad = Habilidad.query.get(idInt)
        if nombreHabilidad:
            arrayInteres.append(nombreHabilidad)

    arrayInteres = list(map(lambda habInt: habInt.serialize(), arrayInteres))

    #Ordeno la informacion para mandarla como json
    data = {
        "habilidades": arrayHabilidad,
        "intereses": arrayInteres
    }
   
    return jsonify({ "message": "Habilidades Cargadas", "data": data }), 200