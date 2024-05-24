from src.core.models.database import db
from src.core.models.oferta import Oferta
from src.core.models.publicacion import Publicacion
from src.core.models.usuario import Usuario

class Notificacion(db.Model):
    __tablename__="notificaciones"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    oferta = db.Column(db.Integer, db.ForeignKey("ofertas.id"), nullable=True)
    publicacion = db.Column(db.Integer, db.ForeignKey("publicaciones.id"), nullable=True)
    descripcion = db.Column(db.String(255), nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    
    @classmethod
    def enviarOferta(cls, id_oferta: int)->None:
        """
        envia la notificacion cuando se envia una Oferta
        """
        oferta= Oferta.query.filter_by(id=id_oferta).first()
        nombrePubli  = Publicacion.query.filter_by(id=oferta.solicitado).first().titulo
        new_notificacion = Notificacion(oferta=id_oferta, descripcion="Tu Publicacion "+nombrePubli+" recibio una oferta")
        db.session.add(new_notificacion)
        db.session.commit()
        
    @classmethod
    def responderOferta(cls, id_oferta: int)->None:
        """
        envia la notificacion cuando se responde una Oferta
        """
        oferta= Oferta.query.filter_by(id=id_oferta).first()
        nombrePubli  = Publicacion.query.filter_by(id=oferta.solicitado).first().titulo
        new_notificacion = Notificacion(oferta=id_oferta, descripcion="Tu Oferta para la Publicacion "+nombrePubli+" fue respondida")
        db.session.add(new_notificacion)
        db.session.commit()
    
    @classmethod
    def cancelarOferta(self,id_oferta: int)->None:
        """
        envia la notificacion cuando se responde una Oferta
        """
        oferta= Oferta.query.filter_by(id=id_oferta).first()
        nombrePubli  = Publicacion.query.filter_by(id=oferta.solicitado).first().titulo
        nombrePubli2  = Publicacion.query.filter_by(id=oferta.ofrecido).first().titulo
        self.oferta = id_oferta
        self.descripcion = "La Oferta de "+nombrePubli+" para intercambiar por "+nombrePubli2+" fue cancelada"
        db.session.commit()
    
    @classmethod
    def eliminarPublicacion(cls, id_Publicacion: int)->None:
        """
        envia la notificacion cuando se elimina una publicacion
        """
        nombrePubli  = Publicacion.query.filter_by(id=id_Publicacion).first().titulo
        new_notificacion = Notificacion(publicacion=id_Publicacion, descripcion="Tu Publicacion "+nombrePubli+" fue eliminada por el administrador")
        db.session.add(new_notificacion)
        db.session.commit()
        
    @classmethod
    def nuevoComentario(cls, id_Publicacion: int)->None:
        """
        envia la notificacion cuando se realiza un nuevo comentario
        """
        nombrePubli  = Publicacion.query.filter_by(id=id_Publicacion).first().titulo
        new_notificacion = Notificacion(publicacion=id_Publicacion, descripcion="Tu Publicacion "+nombrePubli+" recibio un nuevo comentario")
        db.session.add(new_notificacion)
        db.session.commit()
        
    @classmethod
    def responderComentario(cls, id_Publicacion: int)->None:
        """
        envia la notificacion cuando le responden a un comentario
        """
        nombrePubli  = Publicacion.query.filter_by(id=id_Publicacion).first().titulo
        new_notificacion = Notificacion(publicacion=id_Publicacion, descripcion="Tu comentario en la Publicacion "+nombrePubli+" fue respondido")
        db.session.add(new_notificacion)
        db.session.commit()
    