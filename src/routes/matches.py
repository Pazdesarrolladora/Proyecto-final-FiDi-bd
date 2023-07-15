from flask import Blueprint, jsonify, request
from models.match import Match
from models.matchLog import MatchLog
from models import db
from datetime import date





api = Blueprint('api_matches', __name__)


# Ruta para manejar el like del usuario emisor al receptor
@api.route("/like", methods=["POST"])
def like_user():

    emisor_id = request.form["emisor_id"]
    receptor_id = request.form["receptor_id"]

    like= Match()
    like.id_propio= emisor_id
    like.estado = 1

    print("id_propio ",like.id_propio)
    print("estado ",like.estado)
    like.save()

    id_match = like.id

    print("id_match ",id_match)

    nuevoLike = MatchLog()
    nuevoLike.id_match = id_match
    nuevoLike.id_usr_emisor = emisor_id
    nuevoLike.id_usr_receptor = receptor_id
    nuevoLike.creacion_match = date.today()
    nuevoLike.estado = 1
    nuevoLike.save()
    db.session.commit()

    return jsonify({"success": "Like Creado Satisfactoriamente", "status": 200})

# Ruta para manejar el unlike del usuario emisor al receptor
@api.route("/match/unlike", methods=["POST"])
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

# if __name__ == '__main__':
#     #  app.run()


    # Verificar si ya existe un match entre el emisor y el receptor
    # existing_match = MatchLog.query.filter(
    #     (MatchLog.id_usr_emisor == emisor_id) & (Match.id_usr_receptor == receptor_id)
    # ).first()
    # print("existe match "+ existing_match)   
    # print("emisor "+Match.emisor_id) 
    
    # if existing_match:
    #     # Si ya existe un match, actualizar el estado a 2
    #     existing_match.estado = 2
    #     db.session.commit()
    # else:
    #     # Si no existe un match, crear uno nuevo con estado 1
    #     new_match = Match(emisor_id=emisor_id, id_usr_receptor=receptor_id, estado=1)
    #     db.session.add(new_match)
    #     db.session.commit()

    # # Crear un registro en MatchLog
    # match_log = MatchLog(id_match=existing_match.id_match if existing_match else new_match.id_match, id_usr_emisor=emisor_id, id_usr_receptor=receptor_id, estado=new_match.estado)
    # db.session.add(match_log)
    # db.session.commit()