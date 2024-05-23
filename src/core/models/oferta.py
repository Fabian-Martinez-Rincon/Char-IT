from src.core.models.database import db
from datetime import datetime
from src.core.models.oferta import Oferta
from src.core.models.publicacion import Publicacion
from src.core.models.filial import Filial
from src.core.models.estado import Estado

class Oferta(db.Model):
    __tablename__="ofertas"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    ofrecido = db.Column(db.Integer, db.ForeignKey("publicaciones.id"), nullable=False)
    solicitado = db.Column(db.Integer, db.ForeignKey("publicaciones.id"), nullable=False)
    fechaIntercambio = db.Column(db.Date, nullable=False)
    horaIntercambio = db.Column(db.Time, nullable=False)
    filial = db.Column(db.Integer, db.ForeignKey("filiales.id"), nullable=False)
    estado = db.Column(db.Integer, db.ForeignKey("estados.id"), nullable=False)
    