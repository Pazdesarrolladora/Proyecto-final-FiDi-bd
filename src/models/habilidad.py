from models import db

class Habilidad(db.Model):
    __tablename__ = "habilidades"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100))
    registros_habilidades = db.relationship("RegistroHabilidad", backref="habilidad")

    def serialize(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "categoria": self.categoria
        }
    
    def serialize_with_registroHabilidades(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "categoria": self.categoria
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()