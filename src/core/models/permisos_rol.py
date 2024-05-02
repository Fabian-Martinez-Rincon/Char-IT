from src.core.models.database import db

class Permisos_Rol(db.Model):
    __tablename__="permisos_Roles"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    id_rol = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    id_permiso = db.Column(db.Integer, db.ForeignKey("permisos.id"), nullable=False)