from models import db


class MatchLog(db.Model):
    __tablename__ = "match_logs"
    id_match_log = db.Column(db.Integer, primary_key=True)
    id_match = db.Column(db.Integer)
    id_usr_emisor = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    id_usr_receptor = db.Column(db.Integer)
    creacion_match = db.Column(db.DateTime)
    estado = db.Column(db.Integer)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
   
   