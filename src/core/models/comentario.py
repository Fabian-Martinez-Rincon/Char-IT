from src.core.models.database import db
from datetime import datetime
from src.core.models.usuario import Usuario

class Comentario(db.Model):
    __tablename__ = "comentarios"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    contenido = db.Column(db.Text, nullable=False)
    publicacion_id = db.Column(db.Integer, db.ForeignKey("publicaciones.id"), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    comentario_padre_id = db.Column(db.Integer, db.ForeignKey("comentarios.id"), nullable=True)    

    # Relación con el autor
    autor = db.relationship('Usuario', backref=db.backref('comentarios_autor', lazy=True))

    # Relación con la publicación
    publicacion = db.relationship('Publicacion', back_populates='comentarios_publicacion')

    # Relación con la respuesta
    respuesta = db.relationship('Comentario', 
                                backref=db.backref('comentario_padre', remote_side=[id]), 
                                remote_side=[comentario_padre_id], 
                                uselist=False)
