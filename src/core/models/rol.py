from src.core.models.database import db

class Rol(db.Model):
    __tablename__="roles"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    nombre = db.Column(db.String(50), nullable=False, unique= True)
    permisos_rol = db.relationship('Permisos_Rol', backref='permisos_rol', cascade='all, delete-orphan')