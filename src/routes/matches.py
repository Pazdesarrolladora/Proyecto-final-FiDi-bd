from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models.match import Match
from models.matchLog import MatchLog
from models.registroHabilidad import RegistroHabilidad
from models.habilidad import Habilidad
from models.matchLog import MatchLog
from models.notificacion import Notificacion
from models import db
from datetime import date


api = Blueprint('api_matches', __name__)

# Ruta para manejar el like del usuario emisor al receptor
@api.route("/match/like", methods=["POST"])
@jwt_required()
def like_user():

    emisor_id = request.form["emisor_id"]
    receptor_id = request.form["receptor_id"]

    existe_match = MatchLog.query.filter_by(id_usr_emisor=receptor_id).first()

    like= Match()
    like.id_propio= emisor_id
    like.estado = 1
    like.save()

    id_match = like.id

    nuevoLike = MatchLog() #Se crea el nuevo like y se pasan los datos a matchLog
    nuevoLike.id_match = id_match
    nuevoLike.id_usr_emisor = emisor_id
    nuevoLike.id_usr_receptor = receptor_id
    nuevoLike.creacion_match = date.today()
    nuevoLike.estado = 1
    nuevoLike.save()

    print(existe_match)
    if not existe_match: print('No HAY MATCH')

    if existe_match:
        notificacion_emisor = Notificacion() #notificacion para usuario 1 emisor
        notificacion_emisor.mensaje = 'Match'
        notificacion_emisor.id_emisor = emisor_id
        notificacion_emisor.id_receptor = receptor_id 
        notificacion_emisor.save()

        notificacion_receptor = Notificacion() #notificacion para usuario 1 receptor
        notificacion_receptor.mensaje = 'Match'
        notificacion_receptor.id_emisor = receptor_id
        notificacion_receptor.id_receptor = emisor_id
        notificacion_receptor.save()

        nuevoLike.estado = 2
        nuevoLike.update()

    return jsonify({"success": "Like Creado Satisfactoriamente", "status": 200})

 

# Ruta para manejar el unlike del usuario emisor al receptor
@api.route("/match/unlike", methods=["POST"])
@jwt_required()
def unlike_user():
    emisor_id = request.json["emisor_id"]
    receptor_id = request.json["receptor_id"]

    # Verificar si existe un match entre el emisor y el receptor
    existing_match = Match.query.filter(
        (Match.id_usr_emisor == emisor_id) & (Match.id_usr_receptor == receptor_id)
    ).first()

    if existing_match:
        # Actualizar el estado del match a 1
        existing_match.estado = 1
        db.session.commit()

    return jsonify({"message": "Has eliminado el like"})


@api.route('/match/habilidades/usuario/<int:idFront>', methods=['GET'])
@jwt_required()
def obtenerHabilidadesUsuarioMatch(idFront):
    
    #Inicializo variables para guardar las habilidades y los intereses
    arrayHabilidad = []
    arrayInteres = []
    
    #Filtro en el registro de habilidades por id de usuario (id_usuario) y tipo habilidad (Habilidad), me trae todos los encontrados
    #Las habilidades las convierto a listas y por cada habilidad encontrada, guarda el id de la habilidad.
    habilidades = RegistroHabilidad.query.filter_by(id_usuario=idFront, tipo='Habilidad').all()
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

    intereses = RegistroHabilidad.query.filter_by(id_usuario=idFront, tipo='Interes').all()
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