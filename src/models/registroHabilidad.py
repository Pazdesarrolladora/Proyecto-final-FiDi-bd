from models import db
from datetime import datetime

class RegistroHabilidad(db.Model):
    __tablename__= 'registroHabilidades'
    id_registro = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    creacion_registro = db.Column(db.DateTime, default=datetime.now)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_habilidad = db.Column(db.Integer, db.ForeignKey('habilidades.id'), nullable=False)
    usuario_relacion = db.relationship("Usuario", backref='registrosHabilidades')

    def serialize(self):
        return {
            "id_registro": self.id_registro,
            "tipo": self.tipo,
            "creacion_registro": self.creacion_registro,
            "id_usuario": self.id_usuario,
            "id_habilidad": self.id_habilidad
        }
    
    def serialize_with_user(self):
        return {
            "id_registro": self.id_registro,
            "tipo": self.tipo,
            "creacion_registro": self.creacion_registro,
            "id_usuario": self.id_usuario,
            "usuario_relacion": self.get_usuarios(),
            "id_habilidad": self.id_habilidad
        }
    
    def serialize_with_habilities(self):
        return {
            "id_registro": self.id_registro,
            "tipo": self.tipo,
            "creacion_registro": self.creacion_registro,
            "id_usuario": self.id_usuario,
            "id_habilidad": self.id_habilidad,
            "habilidad": self.get_habilidades()
        }
    
    def serialize_with_user_and_habilities(self):
        return {
            "id_registro": self.id_registro,
            "tipo": self.tipo,
            "creacion_registro": self.creacion_registro,
            "id_usuario": self.id_usuario,
            "usuario_relacion": self.get_usuarios(),
            "id_habilidad": self.id_habilidad,
            "habilidad": self.get_habilidades()
        }
    
    def get_habilidad(self):
        return list(map(lambda hability: hability.serialize(), self.habilidad))
    
    def get_usuario(self):
        return list(map(lambda user: user.serialize(), self.usuario_relacion))
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()