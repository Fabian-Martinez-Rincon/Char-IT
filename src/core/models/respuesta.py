from src.core.models.database import db
from datetime import datetime
from src.core.models.publicacion import Publicacion
from src.core.models.usuario import Usuario

class Respuesta(db.Model):
    __tablename__="respuestas"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    estado = db.Column(db.String(50), nullable=False)
    id_PublicacionS = db.Column(db.Integer, db.ForeignKey("publicaciones.id"), nullable=False)
    id_PublicacionO = db.Column(db.Integer, db.ForeignKey("publicaciones.id"), nullable=False)
    descripcionRechazo = db.Column(db.String(255), nullable=True)
    fechaRespuesta = db.Column(db.DateTime, default=datetime.now)
    id_usuarioRespondio = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)