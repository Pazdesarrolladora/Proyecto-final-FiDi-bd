from models import db
from datetime import datetime

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'
    id_notificacion = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(500), nullable=False)
    creacion_notificacion = db.Column(db.DateTime(), default=datetime.now)
    id_emisor = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False) #El que emite el match por segunda vez, emite
    id_receptor = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    visto = db.Column(db.Boolean, default=False)
    
    def serialize(self):
        return {
            "id_notificacion": self.id_notificacion,
            "mensaje": self.mensaje,
            "creacion_notificacion": self.creacion_notificacion,
            "id_emisor": self.id_emisor,
            "id_receptor": self.id_receptor,
            "visto": self.visto
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()