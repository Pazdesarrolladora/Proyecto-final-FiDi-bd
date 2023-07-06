import cloudinary
import cloudinary.uploader
from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from models.imagen import Imagen

api = Blueprint('api_users', __name__)

@api.route('/users', methods=['GET'])
def list_users():
    
    users = Usuario.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200

@api.route('/formulario', methods=['POST'])
def registrar_usuario():

    correo = request.form['correo']
    nombre = request.form['nombre']
    password = request.form['password']
    habilidades = request.form['habilidades']
    imagen = None

    if not correo: return jsonify({"message": "El correo es requerido!"}), 400
    if not nombre: return jsonify({"message": "Nombre requerido!"}), 400
    if not password: return jsonify({"message": "Password requerido!"}), 400
    if not habilidades: return jsonify({"message": "Habilidades requeridas!"}), 400
    if not 'imagen' in request.files: 
        return jsonify({"message": "Image is required!"}), 400
    else: 
        imagen = request.files['imagen']

    response = cloudinary.uploader.upload(imagen, folder="imagenesFidi")
    
    if response:
        nuevaImagen = Imagen()
        nuevaImagen.src_imagen = response['secure_url']
        nuevaImagen.id_publico = response['public_id']
        nuevaImagen.activo = True
        nuevaImagen.save()

    new_user = Usuario()
    new_user.correo = correo
    new_user.nombre = nombre
    new_user.password = password
    new_user.src_imagen = response['secure_url']
    new_user.save()


    return jsonify(message='Ya puedes disfrutar de FiDi'), 201
