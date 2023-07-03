from models import db
from datetime import datetime

class Habilidades(db.Model):
    __tablename__ = 'habilidades'
    id = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(500))
        
    def serialize(self):
        return {
            "id": self.id,
            "mensaje": self.mensaje,
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()