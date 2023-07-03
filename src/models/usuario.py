from models import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    oficio = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(500))
    valoracion = db.Column(db.Float, nullable=False)
    tipo_registro = db.Column(db.Integer, nullable=False)
    api_key = db.Column(db.String, nullable=False)
    id_usuario_favorito = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    id_habilidades = db.Column(db.Integer, db.ForeignKey("habilidades.id"), nullable=False)
    id_interes = db.Column(db.Integer, db.ForeignKey("habilidades.id"), nullable=False)
    id_roles = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    id_imagen = db.Column(db.Integer, db.ForeignKey("imagenes.id"))
    imagenUsuario = db.relationship("Imagen", back_populates="usuarioImagen")
    comentario = db.relationship("Comentario")
    guardado = db.relationship("Guardado", back_populates="usuarioGuardado", uselist=False)
    habilidades = db.relationship("Habilidad", backref="habilidadesUsuario")
    intereses = db.relationship("Habilidad", backref="interesesUsuario")
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
            "foto_usuario": self.foto_usuario,
            "id_usuario_favorito": self.id_usuario_favorito,
            "id_habilidades": self.id_habilidades,
            "id_interes": self.id_interes,
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
            "id_habilidades": self.id_habilidades,
            "id_interes": self.id_interes,
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
