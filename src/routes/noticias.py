import cloudinary
import cloudinary.uploader
from flask import Blueprint, jsonify, request
from models.imagen import Imagen

api = Blueprint('api_noticias', __name__)

@api.route('/api/noticias/agregar', methods=['POST'])
def upload_image():
    
    title = request.form['title']
    image = None
    
    if not title: return jsonify({"message": "Title is required!"}), 400
    if not 'image' in request.files: 
        return jsonify({"message": "Image is required!"}), 400
    else: 
        image = request.files['image']
        
    response = cloudinary.uploader.upload(image, folder="imagenesFidi")
    
    if response:
        
        imagenNoticia = Imagen()
        imagenNoticia.title = title
        imagenNoticia.image_file = response['secure_url']
        imagenNoticia.public_id = response['public_id']
        imagenNoticia.active = True
        imagenNoticia.save()
    
    return jsonify({ "image": imagenNoticia.serialize(), "message": "Image uploaded successfully"}), 201