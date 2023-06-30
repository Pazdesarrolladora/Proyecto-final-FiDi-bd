from flask import Blueprint, jsonify, request

api = Blueprint('api_roles', __name__)

@api.route('/roles', methods=['GET'])
def list_users():
    return jsonify([
        { "id": 1, "name": "Admin" },
        { "id": 2, "name": "Employee" },
    ]), 200