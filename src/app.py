import os
import cloudinary
import cloudinary.uploader
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db


# Import de las tablas
from models.chat import Chat
from models.comentario import Comentario
from models.guardado import Guardado
from models.habilidad import Habilidad
from models.imagen import Imagen
from models.match import Match
from models.mensaje import Mensaje
from models.noticia import Noticia
from models.registroHabilidad import RegistroHabilidad
from models.role import Role
from models.usuario import Usuario
from models.notificacion import Notificacion

from dotenv import load_dotenv
from rutas import api

from routes.auth import api as api_auth
from routes.users import api as api_users
from routes.roles import api as api_roles
from routes.noticias import api as api_noticias
from routes.chats import api as api_chats
from routes.habilidades import api as api_habilidades
from routes.registrosHabilidades import api as api_registrosHabilidades
from routes.matches import api as api_matches
from routes.settings import api as api_settings
from routes.notificaciones import api as api_notificaciones


load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)
Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

cloudinary.config( 
  cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
  api_key = os.getenv('CLOUDINARY_API_KEY'),
  api_secret = os.getenv('CLOUDINARY_API_SECRET'), 
)

app.register_blueprint(api_matches, url_prefix="/api")
app.register_blueprint(api_auth, url_prefix="/api")
app.register_blueprint(api_roles, url_prefix="/api")
app.register_blueprint(api_users, url_prefix="/api")
app.register_blueprint(api_noticias, url_prefix="/api")
app.register_blueprint(api_chats, url_prefix="/api")
app.register_blueprint(api_habilidades, url_prefix="/api")
app.register_blueprint(api_registrosHabilidades, url_prefix="/api")
app.register_blueprint(api_settings, url_prefix="/api")
app.register_blueprint(api_notificaciones, url_prefix="/api")

@app.route('/')
def main():
    return jsonify({ "message": "API REST With Flask"}), 200

#Socket io no funciona aun


if __name__ == '__main__':
    app.run()