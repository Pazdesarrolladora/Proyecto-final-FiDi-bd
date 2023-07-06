import cloudinary
import cloudinary.uploader
from flask import Blueprint, jsonify, request
from models.imagen import Imagen
from models.noticia import Noticia

api = Blueprint('api_noticias', __name__)


#Ruta para agregar una noticia
@api.route('/administrar/agregarNoticia', methods=['POST'])
def upload_image():

    # Asignamos a una variable los valores rescatados del form, 
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    image = None
    
    if not titulo: return jsonify({"message": "Titulo is required!"}), 400
    if not descripcion: return jsonify({"message": "Descripcion is required!"}), 400
    if not 'image' in request.files: 
        return jsonify({"message": "Image is required!"}), 400
    else: 
        image = request.files['image']
        
    response = cloudinary.uploader.upload(image, folder="imagenesFidi")
    
    if response:
        nuevaImagen = Imagen()
        nuevaImagen.src_imagen = response['secure_url']
        nuevaImagen.id_publico = response['public_id']
        nuevaImagen.activo = True
        nuevaImagen.save()

        nuevaNoticia = Noticia()
        nuevaNoticia.titulo = titulo
        nuevaNoticia.descripcion = descripcion
        nuevaNoticia.src_imagen = response['secure_url']
        nuevaNoticia.save()
    
    return jsonify({ "image": nuevaImagen.serialize(), "message": "Noticia creada satisfactoriamente"}), 201

@api.route('/administrar/modificarNoticia')
def modify_notice():
    noticias = Noticia.query.all() # [<User 1>, <User 2>]
    noticias = list(map(lambda noticia: noticia.serialize(), noticias)) # [{"id": 1}, {"id": 2}]
    
    return jsonify(noticias), 200