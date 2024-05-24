from src.core.models.database import db

class Estado(db.Model):
    __tablename__="estados"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    nombre = db.Column(db.String(50), nullable=False)
    
    
#EN LAS SEED PONER LOS ESTADOS CON EL NOMBRE ASI TAL CUAL: "pendiente", "aceptada", "cancelada", "rechazada"