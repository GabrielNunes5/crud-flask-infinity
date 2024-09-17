from ..database import db


class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email
        }