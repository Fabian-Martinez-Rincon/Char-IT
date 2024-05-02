from src.core.models.database import db

class Permiso(db.Model):
    __tablename__="permisos"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    nombre = db.Column(db.String(50), nullable=False, unique= True)
    permisos_rol = db.relationship('Permisos_Rol', backref='permisos_rol', cascade='all, delete-orphan')