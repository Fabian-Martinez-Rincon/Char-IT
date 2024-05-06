from src.core.models.database import db
from datetime import datetime
from src.core.models.categoria import Categoria
from src.core.models.visibilidad import Visibilidad
from src.core.models.usuario import Usuario

class Publicacion(db.Model):
    __tablename__="publicaciones"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    foto_path = db.Column(db.String(255), nullable=False)  # Columna para almacenar la ruta de la imagen en el sistema de archivos
    fecha_publicacion = db.Column(db.DateTime, default=datetime.now)
    filiales_horarios_dias = db.Column(db.String(255), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    id_visibilidad = db.Column(db.Integer, db.ForeignKey("visibilidades.id"), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)