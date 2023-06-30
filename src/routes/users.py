from flask import Blueprint, jsonify, request
from models.usuario import Usuario

api = Blueprint('api_users', __name__)

@api.route('/users', methods=['GET'])
def list_users():
    
    users = Usuario.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200