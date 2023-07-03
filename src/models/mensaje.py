from models import db
from datetime import datetime

class Mensaje(db.Model):
    __tablename__ = "mensajes"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    mensaje = db.Column(db.String(1000), nullable=False)
    creacion_mensaje = db.Column(db.DateTime, default=datetime.now)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    id_chat = db.Column(db.Integer, db.ForeignKey("noticias.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "mensaje": self.mensaje,
            "creacion_mensaje": self.creacion_mensaje,
            "id_usuario": self.id_usuario,
            "id_chat": self.id_chat
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()