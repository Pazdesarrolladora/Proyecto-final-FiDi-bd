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
    permission = db.Column(db.Integer, nullable=False)
    api_key = db.Column(db.String, nullable=False)
    foto_usuario = db.Column(db.String, nullable=False)
    id_usuario_favorito = db.Column(db.Integer, nullable=False)
    id_habilidades = db.Column(db.Integer, nullable=False)
    id_interes = db.Column(db.Integer, nullable=False)

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
            "permission": self.permission,
            "api_key": self.api_key,
            "foto_usuario": self.foto_usuario,
            "id_usuario_favorito": self.id_usuario_favorito,
            "id_habilidades": self.id_habilidades,
            "id_interes": self.id_interes
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
