from models import db
from datetime import datetime

class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, primary_key=True)
    creacion_chat = db.Column(db.DateTime, default=datetime.now)
    id_usuario_send = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    id_usuario_recibe = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    id_mensajes = db.Column(db.Integer, db.ForeignKey("mensajes.id"))
    mensajes = db.relationship("Mensaje")

    def serialize(self):
        return {
            "id": self.id,
            "creacion_chat": self.creacion_chat,
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