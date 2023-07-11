from flask import Flask, request, jsonify
from models import db, Match, MatchLog

app = Flask(__name__)

# Ruta para manejar el like del usuario emisor al receptor
@app.route("/api/match/like", methods=["POST"])
def like_user():
    emisor_id = request.json["emisor_id"]
    receptor_id = request.json["receptor_id"]

    # Verificar si ya existe un match entre el emisor y el receptor
    existing_match = Match.query.filter(
        (Match.id_usr_emisor == emisor_id) & (Match.id_usr_receptor == receptor_id)
    ).first()

    if existing_match:
        # Si ya existe un match, actualizar el estado a 2
        existing_match.estado = 2
        db.session.commit()
    else:
        # Si no existe un match, crear uno nuevo con estado 1
        new_match = Match(id_usr_emisor=emisor_id, id_usr_receptor=receptor_id, estado=1)
        db.session.add(new_match)
        db.session.commit()

    # Crear un registro en MatchLog
    match_log = MatchLog(id_match=existing_match.id_match if existing_match else new_match.id_match, id_usr_emisor=emisor_id, id_usr_receptor=receptor_id, estado=new_match.estado)
    db.session.add(match_log)
    db.session.commit()

    return jsonify({"message": "Haz dado un like"})

# Ruta para manejar el unlike del usuario emisor al receptor
@app.route("/api/match/unlike", methods=["POST"])
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

    return jsonify({"message": "eliminaste el like"})

if __name__ == '__main__':
    app.run()
