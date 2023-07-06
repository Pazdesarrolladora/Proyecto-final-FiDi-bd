from models import db

habilidad_usuario = db.Table("habilidad_usuario",
    db.Column("id_usuario", db.ForeignKey("usuarios.id"), primary_key=True),
    db.Column("id_habilidad", db.ForeignKey("habilidades.id"), primary_key=True),
    db.Column("habilidadInteres", db.String),  # Puedes usar este campo para distinguir habilidades e intereses
)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
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
    habilidades = db.relationship("Habilidad", secondary=habilidad_usuario, backref="usuarios")
    comentario = db.relationship("Comentario")
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
    
    def serialize_with_roles(self):
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
            "foto_usuario": self.foto_usuario,
            "id_usuario_favorito": self.id_usuario_favorito,
            "id_roles": self.id_roles,
            "role": self.role.seralize()
        }


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
