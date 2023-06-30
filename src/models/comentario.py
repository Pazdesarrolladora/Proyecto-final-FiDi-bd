from models import db
from datetime import datetime

class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(500))
    creacion_comentario = db.Column(db.DateTime(), default=datetime.now)
    id_noticia = db.Column(db.Integer, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    
    def serialize(self):
        return {
            "id": self.id,
            "mensaje": self.mensaje,
            "creacion_comentario": self.creacion_comentario
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()