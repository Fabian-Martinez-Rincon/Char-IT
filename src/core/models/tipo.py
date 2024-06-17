from src.core.models.database import db

class Tipo(db.Model):
    __tablename__="tipos"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    nombre = db.Column(db.String(50), nullable=False)