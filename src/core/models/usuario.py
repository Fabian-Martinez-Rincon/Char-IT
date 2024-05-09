from src.core.models.database import db
from datetime import datetime
from src.core.models.rol import Rol

class Usuario(db.Model):
    __tablename__="usuarios"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False) 
    email = db.Column(db.String(255), nullable=False, unique=True)
    dni = db.Column(db.String(12), nullable=True, unique=True) 
    fecha_nacimiento = db.Column(db.DateTime,nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    id_rol = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    publicaciones = db.relationship('Publicacion', backref='publicaciones', cascade='all, delete-orphan')