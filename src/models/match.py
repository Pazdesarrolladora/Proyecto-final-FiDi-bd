from models import db

class Match(db.Model):
    __tablename__ = "matches"
    estado = db.Column(db.Integer)
    id_usuario_remitente = db.Column(db.Integer, primary_key=True) #Union a tabla Usuarios por id
    id_usuario_reportado = db.Column(db.Integer, primary_key=True) #Union a tabla Usuarios por id

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