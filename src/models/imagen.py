from models import db

class Imagen(db.Model):
    __tablename__ = "imagenes"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.Integer)
    archivo_imagen = db.Column(db.String(120))
    id_publico = db.Column(db.Integer)
    activo = db.Column(db.Boolean, default=True)
    usuarioImagen = db.relationship("Usuario", back_populates="imagenUsuario", uselist=False)
    noticiaImagen = db.relationship("Usuario", back_populates="imagenNoticia", uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "archivo_imagen": self.archivo_imagen,
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