from src.core.models.database import db
from src.core.models.oferta import Oferta
from src.core.models.publicacion import Publicacion
from src.core.models.comentario import Comentario
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
    def enviarOferta(self, oferta: Oferta)->None:
        """
        envia la notificacion cuando se envia una Oferta
        """
        Publi  = Publicacion.query.filter_by(id=oferta.solicitado).first()
        new_notificacion = Notificacion(id_usuario= Publi.id_usuario ,oferta=oferta.id, descripcion="Tu Publicacion "+Publi.titulo+" recibio una oferta")
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
        new_notificacion = Notificacion(id_usuario=Publi.id_usuario, publicacion=id_Publicacion, descripcion="Tu Publicación "+Publi.titulo+" fue eliminada por el administrador")
        self.send_mail(Publi.id_usuario, new_notificacion.descripcion)
        db.session.add(new_notificacion)
        db.session.commit()
        
    @classmethod
    def nuevoComentario(self, id_Publicacion: int, comentario:Comentario)->None:
        """
        envia la notificacion cuando se realiza un nuevo comentario
        """
        Publi  = Publicacion.query.filter_by(id=id_Publicacion).first()
        duenio_comentario = Usuario.query.filter_by(id=comentario.autor_id).first()
        new_notificacion = Notificacion(id_usuario=Publi.id_usuario,publicacion=id_Publicacion, descripcion="Tu Publicacion "+Publi.titulo+" recibio un nuevo comentario" + "\n\n" + duenio_comentario.nombre + " " + duenio_comentario.apellido + ": " + comentario.contenido)
        self.send_mail(Publi.id_usuario, new_notificacion.descripcion)
        db.session.add(new_notificacion)
        db.session.commit()
        
    @classmethod
    def responderComentario(self, id_Publicacion: int, comentario_padre:Comentario, respuesta:Comentario)->None:
        """
        envia la notificacion cuando le responden a un comentario 
        recordar que el id_usuario es el que realizo el comentario
        """
        Publi  = Publicacion.query.filter_by(id=id_Publicacion).first()
        duenio = Usuario.query.filter_by(id=Publi.id_usuario).first()
        new_notificacion = Notificacion(id_usuario=comentario_padre.autor_id, publicacion=id_Publicacion, descripcion="Tu comentario en la Publicacion "+Publi.titulo+" fue respondido" + "\n\n" + "Tú: " + comentario_padre.contenido + "\n" + duenio.nombre + " " + duenio.apellido+ ": " + respuesta.contenido)
        self.send_mail(comentario_padre.autor_id, new_notificacion.descripcion)
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
        message = f'¡Atencion! Se le notifica que:\n{descripcion}\n\n Para Conocer mas detalles ingrese a la plataforma.'
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = message
        mail.send(msg)
        
    @classmethod
    def aceptarOferta(self, id_oferta: int)->None:
        """
        envia la notificacion cuando se acepta una Oferta
        """
        oferta= Oferta.query.filter_by(id=id_oferta).first()
        Ofrecido  = Publicacion.query.filter_by(id=oferta.ofrecido).first()
        Solicitado = Publicacion.query.filter_by(id=oferta.solicitado).first()
        
        new_notificacion = Notificacion(
            id_usuario= Ofrecido.id_usuario ,
            oferta=id_oferta, 
            descripcion="Tu Oferta de "+ Ofrecido.titulo+"  por la Publicacion "+Solicitado.titulo+" fue aceptada"
        )
        
        self.send_mail(Ofrecido.id_usuario, new_notificacion.descripcion) 
        db.session.add(new_notificacion)
        db.session.commit()
    
    
    @classmethod
    def rechazarOferta(self, id_oferta: int)->None:
        """
        envia la notificacion cuando se rechaza una Oferta
        """
        oferta= Oferta.query.filter_by(id=id_oferta).first()
        Ofrecido  = Publicacion.query.filter_by(id=oferta.ofrecido).first()
        Solicitado = Publicacion.query.filter_by(id=oferta.solicitado).first()
        
        new_notificacion = Notificacion(
            id_usuario= Ofrecido.id_usuario ,
            oferta=id_oferta, 
            descripcion="Tu Oferta de "+ Ofrecido.titulo+"  por la Publicacion "+Solicitado.titulo+" fue rechazada"
        )
        
        self.send_mail(Ofrecido.id_usuario, new_notificacion.descripcion) 
        db.session.add(new_notificacion)
        db.session.commit()

    @classmethod
    def confirmarIntercambio(self, id_oferta: int)->None:
        """
        envia la notificacion cuando se confirma el intercambio
        """
        oferta= Oferta.query.filter_by(id=id_oferta).first()
        Ofrecido  = Publicacion.query.filter_by(id=oferta.ofrecido).first()
        Solicitado = Publicacion.query.filter_by(id=oferta.solicitado).first()
        
        new_notificacion = Notificacion(
            id_usuario= Ofrecido.id_usuario ,
            oferta=id_oferta, 
            descripcion="El intercambio de "+ Ofrecido.titulo+"  por "+Solicitado.titulo+" fue realizado con exito"
        )

        new_notificacion2 = Notificacion(
            id_usuario= Solicitado.id_usuario ,
            oferta=id_oferta, 
            descripcion="El intercambio de "+ Ofrecido.titulo+"  por "+Solicitado.titulo+" fue realizado con exito"
        )
        
        self.send_mail(Ofrecido.id_usuario, new_notificacion.descripcion) 
        self.send_mail(Solicitado.id_usuario, new_notificacion2.descripcion)
        db.session.add(new_notificacion)
        db.session.commit()        

    @classmethod
    def cancelarIntercambio(self, id_oferta: int)->None:
        """
        envia la notificacion cuando se cancela el intercambio
        """
        oferta= Oferta.query.filter_by(id=id_oferta).first()
        Ofrecido  = Publicacion.query.filter_by(id=oferta.ofrecido).first()
        Solicitado = Publicacion.query.filter_by(id=oferta.solicitado).first()
        
        new_notificacion = Notificacion(
            id_usuario= Ofrecido.id_usuario ,
            oferta=id_oferta, 
            descripcion="El intercambio de "+ Ofrecido.titulo+" por "+Solicitado.titulo+" fue cancelado \nMotivo: "+oferta.descripcion
        )

        new_notificacion2 = Notificacion(
            id_usuario= Solicitado.id_usuario ,
            oferta=id_oferta, 
            descripcion="El intercambio de "+ Ofrecido.titulo+" por "+Solicitado.titulo+" fue cancelado \nMotivo: "+oferta.descripcion
        )
        
        self.send_mail(Ofrecido.id_usuario, new_notificacion.descripcion) 
        self.send_mail(Solicitado.id_usuario, new_notificacion2.descripcion)
        db.session.add(new_notificacion)
        db.session.commit()        