from flask import Blueprint, jsonify, request
from models.habilidad import Habilidad

api = Blueprint('api_habilidad', __name__)

@api.route('/habilidades', methods=['GET'])
def listar_habilidades():
    
    habilidades = Habilidad.query.all()
    habilidades = list(map(lambda skill: skill.serialize(), habilidades))

    return jsonify(habilidades), 200



