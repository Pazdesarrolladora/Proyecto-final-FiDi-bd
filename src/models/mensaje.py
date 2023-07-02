from models import db
from datetime import datetime

class Mensaje(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(500))
    creacion_mensaje = db.Column(db.DateTime(), default=datetime.now)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    
    def serialize(self):
        return {
            "id": self.id,
            "mensaje": self.mensaje,
            "creacion_mensaje": self.creacion_comentario
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()