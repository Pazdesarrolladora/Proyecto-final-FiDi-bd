import cloudinary
import cloudinary.uploader
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from models.usuario import Usuario
from models.imagen import Imagen
from models.habilidad import Habilidad
from models.usuario import habilidad_usuario

api = Blueprint('api_users', __name__)

@api.route('/users', methods=['GET'])
def list_users():
    
    users = Usuario.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200

@api.route('/formulario', methods=['POST'])
def registrar_usuario():
    print("estoy aqui")
    correo = request.form['correo']
    nombre = request.form['nombre']
    password = request.form['password']
    imagen = None

    #Valido si los campos vienen con informacion
    if not correo: return jsonify({"message": "El correo es requerido!"}), 400
    if not nombre: return jsonify({"message": "Nombre requerido!"}), 400
    if not password: return jsonify({"message": "Password requerido!"}), 400
    if not 'imagen' in request.files: 
        return jsonify({"message": "Image is required!"}), 400
    else: 
        imagen = request.files['imagen']

    #Creo una variable userFound, a la cual le asigno el primer usuario que encuentre con la funcion filter_by
    #buscando en la db, el username provisto por el POST dentro de todos los User existentes
    userFound = Usuario.query.filter_by(correo=correo).first()
    #Si el usuario encontrado efectivamente existe, se devuelve un mensaje
    if userFound: return jsonify({"message": "El correo ya esta registrado!"}), 400

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
    new_user.password = generate_password_hash(password)
    new_user.src_imagen = response['secure_url']

    # for id in habilidades:
    #     habilidad = Habilidad.query.get(id)
    #     if habilidad: new_user.habilidades.append(habilidad)

    # for id in intereses:
    #     interes = Habilidad.query.get(id)
    #     if interes: new_user.habilidades.append(interes)

    new_user.save()

    return jsonify({"success": "User created successfully", "status": 201}), 201
