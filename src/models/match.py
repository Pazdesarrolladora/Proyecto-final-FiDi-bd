from models import db

class Match(db.Model):
    __tablename__ = "matches" #Al hacer match debe haber una funcion que compruebe si existe el opuesto, ejemplo, (id propio = 1) (id match = 3) (estado = 1)| preguntar si existe (id propio=3) (id match = 1) (estado = 1) si es true habra match
    id =  db.Column(db.Integer, primary_key=True)
    id_propio = db.Column(db.Integer, db.ForeignKey("usuarios.id")) 
    estado = db.Column(db.Integer) # estado=1 Like, estado=2 Siguiente

    # def serialize(self):
    #     return {
    #         "id_match": self.id_match,
    #         "id_propio": self.id_propio,
    #         "estado": self.estado
    #     }
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()