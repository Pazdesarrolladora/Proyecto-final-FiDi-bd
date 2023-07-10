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

    correo = request.form['correo']
    nombre = request.form['nombre']
    password = request.form['password']
    #habilidades = request.form['habilidades'] #Recibo el array habilidades mandados por el front, los id's de las habilidades seleccionadas por el usuario
    #intereses = request.form['intereses'] #Recibo el array intereses mandados por el front, los id's de las intereses seleccionadas por el usuario
    imagen = None

    #print(habilidades) #Confirmado de que recibo id's
    #print(intereses)

    #Valido si los campos vienen con informacion
    if not correo: return jsonify({"advertencia": "El correo es requerido!"}), 400
    if not nombre: return jsonify({"advertencia": "Nombre requerido!"}), 400
    if not password: return jsonify({"advertencia": "Password requerido!"}), 400
    #if not habilidades: return jsonify({"advertencia": "Habilidades requeridas!"}), 400
    #if not intereses: return jsonify({"advertencia": "Intereses requeridos!"}), 400
    if not 'imagen' in request.files: 
        return jsonify({"advertencia": "La imagen es requerida!"}), 400
    else: 
        imagen = request.files['imagen']

    #Creo una variable userFound, a la cual le asigno el primer usuario que encuentre con la funcion filter_by
    #buscando en la db, el correo provisto por el POST dentro de todos los User existentes
    userFound = Usuario.query.filter_by(correo=correo).first()
    #Si el usuario encontrado efectivamente existe, se devuelve un mensaje de que ya existe
    if userFound: return jsonify({"advertencia": "El correo ya esta registrado!"}), 400

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
    #     if habilidad and habilidad not in new_user.habilidades:
    #         new_user.habilidades.append(habilidad.id)

    # #Recorro este array intereses, y por cada iteracion asigno a 'interes' la busqueda de la habilidad por id de cada vuelta
    # for id in intereses:
    #     interes = Habilidad.query.get(id)
    #     #Si NO existe el interes buscado por id, se crea un nuevo elemento en la tabla que incluye el id del usuario y el id de la habilidad (clave compuesta) por cada iteracion
    #     if interes and interes not in new_user.habilidades:
    #         new_user.habilidades.append(interes.id)
    
    new_user.save()

    return jsonify({"success": "Usuario creado Satisfactoriamente", "status": 201})
