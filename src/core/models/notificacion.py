from src.core.models.database import db
from src.core.models.oferta import Oferta
from src.core.models.publicacion import Publicacion
from src.core.models.usuario import Usuario
from flask_mail import Mail, Message
from flask import current_app

class Notificacion(db.Model):
    __tablename__="notificaciones"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    oferta = db.Column(db.Integer, db.ForeignKey("ofertas.id"), nullable=True)
    publicacion = db.Column(db.Integer, db.ForeignKey("publicaciones.id"), nullable=True)
    descripcion = db.Column(db.String(255), nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    
    @classmethod
    def enviarOferta(self, id_oferta: int)->None:
        """
        envia la notificacion cuando se envia una Oferta
        """
        oferta= Oferta.query.filter_by(id=id_oferta).first()
        Publi  = Publicacion.query.filter_by(id=oferta.solicitado).first()
        new_notificacion = Notificacion(id_usuario= Publi.id_usuario ,oferta=id_oferta, descripcion="Tu Publicacion "+Publi.titulo+" recibio una oferta")
        self.send_mail(Publi.id_usuario, new_notificacion.descripcion)
        db.session.add(new_notificacion)
        db.session.commit()
        
    @classmethod
    def responderOferta(self, id_oferta: int)->None:
        """
        envia la notificacion cuando se responde una Oferta
        """
        oferta= Oferta.query.filter_by(id=id_oferta).first()
        Publi  = Publicacion.query.filter_by(id=oferta.ofrecido).first()
        new_notificacion = Notificacion(id_usuario= Publi.id_usuario ,oferta=id_oferta, descripcion="Tu Oferta para la Publicacion "+Publi.titulo+" fue respondida")
        self.send_mail(Publi.id_usuario, new_notificacion.descripcion) 
        db.session.add(new_notificacion)
        db.session.commit()
    
    @classmethod
    def cancelarOferta(self,id_oferta: int, id_usuario:int )->None:
        """
        envia la notificacion cuando se cancela una Oferta
        """
        oferta= Oferta.query.filter_by(id=id_oferta).first()
        nombrePubli  = Publicacion.query.filter_by(id=oferta.solicitado).first().titulo
        nombrePubli2  = Publicacion.query.filter_by(id=oferta.ofrecido).first().titulo
        new_notificacion = Notificacion(id_usuario= id_usuario ,oferta=id_oferta, descripcion="La Oferta de "+nombrePubli+" para intercambiar por "+nombrePubli2+" fue cancelada")
        self.send_mail(id_usuario, new_notificacion.descripcion)
        db.session.add(new_notificacion)
        db.session.commit()
    
    @classmethod
    def cancelarOfertaAceptada(self,id_oferta: int)->None:
        """
        envia la notificacion cuando se cancela una Oferta que fue aceptada y ninguno de los dos usuarios asistio
        """
        oferta = Oferta.query.filter_by(id=id_oferta).first()
        PubliO = Publicacion.query.filter_by(id=oferta.ofrecido).first()
        PubliS = Publicacion.query.filter_by(id=oferta.solicitado).first()
        new_notificacion = Notificacion(id_usuario= PubliO.id_usuario ,oferta=id_oferta, descripcion="La Oferta de "+PubliS.titulo+" para intercambiar por "+PubliO.titulo+" fue cancelada por no asistir a la reunion")
        self.send_mail(PubliO.id_usuario, new_notificacion.descripcion) 
        new_notificacion2 = Notificacion(id_usuario= PubliS.id_usuario ,oferta=id_oferta, descripcion="La Oferta de "+PubliS.titulo+" para intercambiar por "+PubliO.titulo+" fue cancelada por no asistir a la reunion")
        self.send_mail(PubliS.id_usuario, new_notificacion.descripcion)
        db.session.add(new_notificacion, new_notificacion2)
        db.session.commit()
    
    @classmethod
    def eliminarPublicacion(self, id_Publicacion: int)->None:
        """
        envia la notificacion cuando se elimina una publicacion al usuario que se le elimino 
        recordar cancelar las ofertas pendientes que tenia y enviar la notificacion con "cancelarOferta" (lo mismo que cuando se elimina mi publicacion)
        """
        Publi  = Publicacion.query.filter_by(id=id_Publicacion).first()
        new_notificacion = Notificacion(id_usuario=Publi.id_usuario, publicacion=id_Publicacion, descripcion="Tu Publicacion "+Publi.titulo+" fue eliminada por el administrador")
        self.send_mail(Publi.id_usuario, new_notificacion.descripcion)
        db.session.add(new_notificacion)
        db.session.commit()
        
    @classmethod
    def nuevoComentario(self, id_Publicacion: int)->None:
        """
        envia la notificacion cuando se realiza un nuevo comentario
        """
        Publi  = Publicacion.query.filter_by(id=id_Publicacion).first()
        new_notificacion = Notificacion(id_usuario=Publi.id_usuario,publicacion=id_Publicacion, descripcion="Tu Publicacion "+Publi.titulo+" recibio un nuevo comentario")
        self.send_mail(Publi.id_usuario, new_notificacion.descripcion)
        db.session.add(new_notificacion)
        db.session.commit()
        
    @classmethod
    def responderComentario(self, id_usuario:int, id_Publicacion: int)->None:
        """
        envia la notificacion cuando le responden a un comentario 
        recordar que el id_usuario es el que realizo el comentario
        """
        nombrePubli  = Publicacion.query.filter_by(id=id_Publicacion).first()
        new_notificacion = Notificacion(id_usuario=id_usuario, publicacion=id_Publicacion, descripcion="Tu comentario en la Publicacion "+nombrePubli+" fue respondido")
        self.send_mail(id_usuario, new_notificacion.descripcion)
        db.session.add(new_notificacion)
        db.session.commit()
    
    @staticmethod
    def send_mail(userId: int, descripcion: str)->None:
        """
        Send the confirmation email to the user.
        """
        app = current_app._get_current_object()
        usuario = Usuario.query.filter_by(id=userId).first()
        mail = Mail(app)
        subject = 'Nueva Notificacion'
        sender = app.config['MAIL_DEFAULT_SENDER']
        recipients = [usuario.email]
        message = f'¡Atencion! Se le notifica que:\n\n {descripcion} \n\n Para Conocer mas detalles ingrese a la plataforma.'
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = message
        mail.send(msg)