from models import db

class Imagen(db.Model):
    __tablename__ = "imagenes"
    id = db.Column(db.Integer, primary_key=True)
    src_imagen = db.Column(db.String(400))
    id_publico = db.Column(db.String(200))
    activo = db.Column(db.Boolean, default=True)

    def serialize(self):
        return {
            "id": self.id,
            "src_imagen": self.src_imagen,
            "id_publico": self.id_publico,
            "activo": self.activo
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()