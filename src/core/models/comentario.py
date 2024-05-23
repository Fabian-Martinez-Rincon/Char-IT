from src.core.models.database import db
from datetime import datetime
from src.core.models.usuario import Usuario
from src.core.models.publicacion import Publicacion

class Comentario(db.Model):
    __tablename__="comentarios"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    descripcion = db.Column(db.String(255), nullable=False)
    fecha_comentario = db.Column(db.DateTime, default=datetime.now)
    autor = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    respuesta = db.Column(db.Integer, db.ForeignKey("comentarios.id"), nullable=True)
    publicacion = db.Column(db.Integer, db.ForeignKey("publicaciones.id"), nullable=False)