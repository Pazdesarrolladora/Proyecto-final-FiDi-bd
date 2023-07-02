from models import db
from datetime import datetime

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    creacion_chat = db.Column(db.DateTime, default=datetime.utcnow)
    id_usuario_send = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    id_usuario_recibe = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    id_mensajes = db.Column(db.Integer, db.ForeignKey('mensajes.id'))
    
    def serialize(self):
        return {
            "id": self.id,
            "creacion_chat": self.creacion_chat.isoformat(),
            "id_usuario_send": self.id_usuario_send,
            "id_usuario_recibe": self.id_usuario_recibe,
            "id_mensajes": self.id_mensajes
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
