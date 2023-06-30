from models import db

class Guardado(db.Model):
    __tablename__ = 'guardados'
    id = db.Column(db.Integer, primary_key=True)
    id_noticia = db.Column(db.Integer) #Falta relacion a tabla Noticia
    id_usuario = db.Column(db.Integer) #Falta relacion a tabla Usuario
    
    def serialize(self):
        return {
            "id": self.id
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()