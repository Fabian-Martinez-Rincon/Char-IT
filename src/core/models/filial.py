from src.core.models.database import db

class Filial(db.Model):
    __tablename__ = "filiales"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    horarios = db.Column(db.String(255), nullable=False)
    dias = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(255), nullable=False)