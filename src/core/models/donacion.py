from src.core.models.database import db
from src.core.models.categoria import Categoria
from src.core.models.tipo import Tipo
from datetime import datetime

class Donacion(db.Model):
    __tablename__="donaciones"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    id_tipo = db.Column(db.Integer, db.ForeignKey("tipos.id"), nullable=False) # PUEDE SER PRODUCTO - EFECTIVO - TARJETA
    email = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(50), nullable=True) # OPCIONAL SI NO ESTA REGISTRADO
    descripcion = db.Column(db.String(255), nullable=True) # SI ES UN PRODUCTO VA EL NOMBRE DEL PRODUCTO, SI ES POR LA WEB VA EL NRO DE COMPROBANTE
    monto = db.Column(db.Float, nullable=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=True)
    fecha_donacion = db.Column(db.DateTime, default=datetime.now)