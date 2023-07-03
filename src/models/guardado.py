from models import db

class Guardado(db.Model):
    __tablename__ = 'guardados'
    id_noticia = db.Column(db.Integer,db.ForeignKey("noticias.id"), primary_key=True) 
    id_usuario = db.Column(db.Integer,db.ForeignKey("usuarios.id") , primary_key=True)
    noticia = db.relationship("Noticia", back_populates="guardado")
    
    def serialize(self):
        return {
            "id_noticia": self.id_noticia,
            "id_usuario": self.id_usuario
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()