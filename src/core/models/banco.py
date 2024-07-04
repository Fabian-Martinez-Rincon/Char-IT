from src.core.models.database import db

class Banco(db.Model):
    __tablename__="bancos"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    tipo = db.Column(db.String(100), nullable=False)
    nro_tarjeta = db.Column(db.String(200), nullable=False)
    vencimiento = db.Column(db.String(6), nullable=False)
    cvv = db.Column(db.String(4), nullable=False)
    titular = db.Column(db.String(100), nullable=False)
    saldo = db.Column(db.Float, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, default=True)