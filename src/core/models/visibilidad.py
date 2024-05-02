from src.core.models.database import db

class Visibilidad(db.Model):
    __tablename__="visibilidades"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    estado = db.Column(db.String(50), nullable=False, unique= True)
    publicaciones = db.relationship('Publicacion', backref='publicaciones', cascade='all, delete-orphan')