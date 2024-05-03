from src.core.models.database import db

# class Permiso(db.Model):
#     __tablename__="permisos"
#     id = db.Column(db.Integer, primary_key=True, unique= True)
#     nombre = db.Column(db.String(50), nullable=False, unique= True)
#     permisos_rol = db.relationship('Permisos_Rol', backref='permisos_rol', cascade='all, delete-orphan')

#el valor de backref debería ser un nombre que se usará para referirse a la relación desde el modelo relacionado. Aquí parece que estás usando el mismo nombre para el backref que para la relación en sí, lo que podría estar causando confusión o un conflicto.

class Permiso(db.Model):
    __tablename__ = "permisos"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    permisos_roles = db.relationship('Permisos_Rol', backref='permiso', cascade='all, delete-orphan')
