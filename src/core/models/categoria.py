from src.core.models.database import db

class Categoria(db.Model):
    __tablename__="categorias"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    nombre = db.Column(db.String(50), nullable=False, unique= True)
    publicaciones = db.relationship('Publicacion', backref='publicaciones', cascade='all, delete-orphan')