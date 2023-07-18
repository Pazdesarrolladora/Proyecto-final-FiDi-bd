from models import db


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer)
    oficio = db.Column(db.String(200))
    descripcion = db.Column(db.String(500))
    valoracion = db.Column(db.Float)
    tipo_registro = db.Column(db.Integer)
    api_key = db.Column(db.String)
    src_imagen = db.Column(db.String(1000))
    id_usuario_favorito = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    id_roles = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False, default=2)
    registros_habilidades = db.relationship("RegistroHabilidad", backref="usuario")
    comentario = db.relationship("Comentario")
    notificacion_emisor = db.relationship("Notificacion", foreign_keys='Notificacion.id_emisor')
    notificacion_receptor = db.relationship("Notificacion", foreign_keys='Notificacion.id_receptor')
    guardado = db.relationship("Guardado", back_populates="usuarioGuardado", uselist=False)
    mensajes = db.relationship("Mensaje", backref="mensajesUsuario")


    def serialize(self):
        return {
            "id": self.id,
            "correo": self.correo,
            "password": self.password,
            "nombre": self.nombre,
            "edad": self.edad,
            "oficio": self.oficio,
            "descripcion": self.descripcion,
            "valoracion": self.valoracion,
            "tipo_registro": self.tipo_registro,
            "api_key": self.api_key,
            "src_imagen": self.src_imagen,
            "id_usuario_favorito": self.id_usuario_favorito,
            "id_roles": self.id_roles
        }
    
    def serialize_with_registroHabilidades(self):
        return {
            "id": self.id,
            "correo": self.correo,
            "password": self.password,
            "nombre": self.nombre,
            "edad": self.edad,
            "oficio": self.oficio,
            "descripcion": self.descripcion,
            "valoracion": self.valoracion,
            "tipo_registro": self.tipo_registro,
            "api_key": self.api_key,
            "src_imagen": self.src_imagen,
            "id_usuario_favorito": self.id_usuario_favorito,
            "id_roles": self.id_roles,
            "registrosHabilidades": self.get_registrosHabilidades()
        }

    def get_registrosHabilidades(self):
        return list(map(lambda registro: registro.serialize(), self.registrosHabilidades))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
