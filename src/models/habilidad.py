from models import db

class Habilidad(db.Model):
    __tablename__ = "habilidades"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()