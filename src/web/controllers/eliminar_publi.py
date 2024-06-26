from flask import redirect, url_for, flash, Blueprint, session
from src.core.models.usuario import Usuario
from src.core.models.publicacion import Publicacion
from src.core.models.database import db
from src.core.models.oferta import Oferta
from src.core.models.notificacion import Notificacion
from src.core.models.estado import Estado
bp = Blueprint("eliminar_publi", __name__)

@bp.route("/eliminar_publi/<int:publicacion_id>", methods=['GET'])
def eliminar_publi(publicacion_id):
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    # Verifica si el usuario actual es el propietario de la publicación
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol != 1 :  
                    flash('No tienes permiso para realizar esta operacion.', 'error')
                    return redirect(url_for('root.index_get'))
    Publi = Publicacion.query.get_or_404(publicacion_id)
    if Publi.id_usuario != session.get('user_id'):
        flash('No tienes permiso para editar esta publicación.', 'error')
        return redirect(url_for('root.publicaciones_get'))
    
    if (Oferta.query.join(Estado, Estado.id == Oferta.estado).filter(
        ((Oferta.ofrecido == publicacion_id) | (Oferta.solicitado == publicacion_id)) &
        ((Estado.nombre == "pendiente"))
    ).all()):
        flash('No Puedes Eliminar esta Publicacion ya que tenes ofertas pendientes.', 'error')
        return redirect(url_for('root.ofertas_recibidas_get'))
    
    if (Oferta.query.join(Estado, Estado.id == Oferta.estado).filter(
        ((Oferta.ofrecido == publicacion_id) | (Oferta.solicitado == publicacion_id)) &
        ((Estado.nombre == "aceptadas"))
    ).all()):
        flash('No Puedes Eliminar esta Publicacion se encuentra en una oferta aceptada.', 'error')
        return redirect(url_for('root.ofertas_recibidas_get'))
    
    Publi.id_visibilidad = 3 # Cambiar la visibilidad de la publicación a "eliminada"
    db.session.add(Publi)
    db.session.commit()
    flash('La publicación ha sido eliminada correctamente.', 'success')
    return redirect(url_for('root.mis_publicaciones_get'))

@bp.route("/eliminar_publi_own/<int:publicacion_id>", methods=['GET'])
def eliminar_publi_own(publicacion_id):
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    # Verifica si el usuario actual es Owner de la pagina
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol != 3 :  
                    flash('No tienes permiso para realizar esta operacion.', 'error')
                    return redirect(url_for('root.index_get'))
    Publi = Publicacion.query.get_or_404(publicacion_id)
    
    
    if (Oferta.query.join(Estado, Estado.id == Oferta.estado).filter(
        ((Oferta.ofrecido == publicacion_id) | (Oferta.solicitado == publicacion_id)) &
        ((Estado.nombre == "aceptadas"))
    ).all()):
        flash('No Puedes Eliminar esta Publicacion se encuentra en una oferta aceptada.', 'error')
        return redirect(url_for('root.historial_intercambios'))
    
    #Busca las ofertas con estado pendiente para notificar el cambio de estado
    ofertas_relacionadas = Oferta.query.join(Estado, Estado.id == Oferta.estado).filter(
        ((Oferta.ofrecido == publicacion_id) | (Oferta.solicitado == publicacion_id)) &
        ((Estado.nombre == "pendiente"))
    ).all()
    
    cancelada = Estado.query.filter_by(nombre="cancelada").first()
    # # Cambiar el estado de todas las ofertas pendientes que involucran esta publicación a "cancelada"
    for oferta in ofertas_relacionadas:
        oferta.estado = cancelada.id
    
    # Enviar notificación al usuario dueño de la otra publicación
    for oferta in ofertas_relacionadas:
        otra_publicacion_id = oferta.ofrecido if oferta.ofrecido != publicacion_id else oferta.solicitado
        otra_publicacion = Publicacion.query.get(otra_publicacion_id)
        if otra_publicacion.id_usuario != session.get('user_id'):
            # Crear notificación solo si el usuario dueño de la otra publicación no es el mismo que elimina la publicación
            oferta.descripcion = "La oferta fue cancelada por la eliminacion de " + Publi.titulo
            Notificacion.cancelarOferta(oferta.id, otra_publicacion.id_usuario)
            # Crear la notificación de eliminación de publicación
    Notificacion.eliminarPublicacion(publicacion_id)
    
    Publi.id_visibilidad = 3 # Cambiar la visibilidad de la publicación a "eliminada"
    db.session.add(Publi)
    db.session.commit()
    flash('La publicación ha sido eliminada correctamente.', 'success')
    return redirect(url_for('root.index_get'))