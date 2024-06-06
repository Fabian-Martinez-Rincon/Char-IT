from flask import redirect, url_for, flash, Blueprint, session
from src.core.models.publicacion import Publicacion
from src.core.models.database import db
from src.core.models.usuario import Usuario
from src.core.models.oferta import Oferta
from src.core.models.estado import Estado
from src.core.models.notificacion import Notificacion

bp = Blueprint("cambiar_visibilidad", __name__)

@bp.route("/cambiar_visibilidad/<int:publicacion_id>", methods=['GET'])
def cambiar_visibilidad(publicacion_id):
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol != 1 :  
                    flash('No tienes permiso para realizar esta operacion.', 'error')
                    return redirect(url_for('root.index_get'))
    Publi = Publicacion.query.get_or_404(publicacion_id)
    if Publi.id_usuario != session.get('user_id'):
        flash('No tienes permiso para editar esta publicación.', 'error')
        return redirect(url_for('root.publicaciones_get'))
    
    ofertas_involucradas = Oferta.query.join(Estado, Estado.id == Oferta.estado).filter(
        ((Oferta.ofrecido == publicacion_id) | (Oferta.solicitado == publicacion_id)) &
        ((Estado.nombre == "aceptada"))
    ).all()
    
    if (ofertas_involucradas):
        flash('No Puedes Cambiar la visibilidad de esta Publicacion ya que tenes un intercambio pendiente.', 'error')
        return redirect(url_for('root.publicacion_detalle', publicacion_id=publicacion_id))
    
    
    #RECORDAR AGREGAR DOBLE CONFIRMACION AL ARCHIVAR YA QUE SE CANCELAN LAS OFERTAS PENDIENTES A RESPONDER
    if Publi.id_visibilidad == 1:
        #Busca las ofertas con estado pendiente para notificar el cambio de estado
        ofertas_relacionadas = Oferta.query.join(Estado, Estado.id == Oferta.estado).filter(
            ( (Oferta.solicitado == publicacion_id)) &
            ((Estado.nombre == "pendiente"))
        ).all()
        
        cancelada = Estado.query.filter_by(nombre="cancelada").first()
        # Cambiar el estado de todas las ofertas pendientes que involucran esta publicación a "cancelada"
        for oferta in ofertas_relacionadas:
            oferta.estado = cancelada.id  
            oferta.descripcion = "La publicación ya no se encuentra disponible."
            Notificacion.responderOferta(oferta.id)
        Publi.id_visibilidad = 2
    else:
        Publi.id_visibilidad = 1
    db.session.commit()
    flash('La publicación se ha actualizado correctamente.', 'success')
    return redirect(url_for('root.publicacion_detalle', publicacion_id=publicacion_id))
