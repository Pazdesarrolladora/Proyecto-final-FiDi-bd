from models import db
from datetime import datetime

class Noticia(db.Model):
    __tablename__ = 'noticias'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    creacion_noticia = db.Column(db.DateTime, default=datetime.now)
    foto = db.Column(db.String(500))
    descripcion = db.Column(db.String(3000))
    comentario = db.relationship("Comentario", backref="noticia")
    guardado = db.relationship("Guardado", back_populates="noticia", uselist=False)

    
    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "creacion_noticia": self.creacion_noticia,
            "foto": self.foto,
            "descripcion": self.descripcion
        }
        
    #Crear funcion para serializar junto con los comentarios
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()