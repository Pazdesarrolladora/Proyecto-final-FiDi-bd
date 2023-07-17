import cloudinary
import cloudinary.uploader
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token
from models import db
from models.usuario import Usuario
from models.imagen import Imagen
from models.habilidad import Habilidad
from models.registroHabilidad import RegistroHabilidad

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
    habilidades_raw = request.form['habilidades'] #Recibo el array habilidades mandados por el front, los id's de las habilidades seleccionadas por el usuario
    habilidades = [int(i) for i in habilidades_raw.split(',')] #La informacion viene como string desde el front, lo convierto en una lista para manipularlo
    intereses_raw = request.form['intereses']
    intereses = [int(i) for i in intereses_raw.split(',')]
    descripcion = request.form['descripcion']
    imagen = None

    print(habilidades) #Confirmado de que recibo id's
    print(intereses) #

    #Valido si los campos vienen con informacion, defino las advertencias que iran para el front y desplegarlas con el toast
    if not correo: return jsonify({"advertencia": "El correo es requerido!"}), 400
    if not nombre: return jsonify({"advertencia": "Nombre requerido!"}), 400
    if not password: return jsonify({"advertencia": "Password requerido!"}), 400
    if not habilidades: return jsonify({"advertencia": "Habilidades requeridas!"}), 400
    if not intereses: return jsonify({"advertencia": "Intereses requeridos!"}), 400
    if not descripcion: descripcion = ""
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
    new_user.descripcion = descripcion
    new_user.save()

    for id_habilidad in habilidades:
            new_register = RegistroHabilidad()
            new_register.id_usuario = new_user.id
            habilidad = Habilidad.query.get(id_habilidad)
            if habilidad:
                 new_register.id_habilidad = id_habilidad
                 new_register.tipo = 'Habilidad'
                 db.session.add(new_register)
                
    db.session.commit()

    #Recorro la lista intereses, la cual me trae el id de los intereses seleccionados por el usuario
    #Creo un nuevo RegistroHabilidad por cada vuelta de mi ciclo y le asigno 
    for id_interes in intereses:
            new_register = RegistroHabilidad()
            new_register.id_usuario = new_user.id
            interes = Habilidad.query.get(id_interes)
            if interes:
                 new_register.id_habilidad = id_interes
                 new_register.tipo = 'Interes'
                 db.session.add(new_register)

    db.session.commit()

    return jsonify({"success": "Usuario creado Satisfactoriamente", "Nuevo Usuario": new_user.serialize_with_registroHabilidades(), "status": 201})


@api.route('/settings/cambiarPassword/<int:id>', methods=['POST'])
@jwt_required()
def cambiarContraseña(id):

    actualPass = request.json.get('actualPass')
    newPass = request.json.get('newPass')
    verifyPass = request.json.get('verifyPass')

    if not actualPass: return jsonify({ "message": "La contraseña actual es requerida!"}), 400
    if not newPass: return jsonify({ "message": "La nueva contraseña es requerida!"}), 400
    if not verifyPass: return jsonify({ "message": "Debes repetir tu contraseña!"}), 400

    if newPass != verifyPass: return jsonify({ "message": "Las contraseñas no coinciden!"}), 400

    user = Usuario.query.get(id)

    if not check_password_hash(user.password, actualPass):
        return jsonify({ "message": "La constraseña es incorrecta!"}), 401
    
    newGeneratedHash = generate_password_hash(newPass)
    
    user.password = newGeneratedHash
    user.update()


    return jsonify({"success": "Contraseña Actualizada!", "usuario": user.serialize()}), 201

@api.route('/settings/cambiarImagen/<int:id>', methods=['POST'])
@jwt_required()
def cambiarImagen(id):

    #Busco al usuario por el id recibido por la ruta
    #Despues busco la imagen por el src_imagen que contiene el usuario encontrado
    user = Usuario.query.get(id)
    registroImagen = Imagen.query.filter_by(src_imagen=user.src_imagen).first()

    #Inicializo vacio para que no de error
    imagen = None

    #Pregunto si no viene vacia la peticion de imagen y la asigno a una variable imagen
    if not 'imagen' in request.files: 
        return jsonify({"message": "La imagen es requerida!"}), 400
    else: 
        imagen = request.files['imagen']

    #Destruyo la anterior imagen del usuario en cuestion
    cloudinary.uploader.destroy(registroImagen.id_publico)

    registroImagen.delete()

    response = cloudinary.uploader.upload(imagen, folder="imagenesFidi")

    if response:
        nuevaImagen = Imagen()
        nuevaImagen.src_imagen = response['secure_url']
        nuevaImagen.id_publico = response['public_id']
        nuevaImagen.activo = True
        nuevaImagen.save()

    user.src_imagen = response['secure_url']
    user.update()
    

    return jsonify({"success": "Imagen Actualizada!"}), 201
     