from flask import Flask, request, flash, redirect, url_for, Blueprint, session
from src.core.models.database import db
from src.core.models.oferta import Oferta
from src.core.models.estado import Estado
from src.core.models.usuario import Usuario
from src.core.models.notificacion import Notificacion

bp = Blueprint("rechazarOferta", __name__)

@bp.route('/rechazarOferta/<int:oferta_id>', methods=['GET', 'POST'])
def rechazarOferta(oferta_id):
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    # Verifica si el usuario actual es el propietario de la publicación
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol != 1 :  
                    flash('No tienes permiso para realizar esta operacion.', 'error')
                    return redirect(url_for('root.index_get'))

    try:
        # Buscar la oferta correspondiente en la base de datos
        oferta = Oferta.query.get(oferta_id)

        if not oferta:
            flash("Oferta no encontrada", "error")
            return redirect(url_for('/ofertas/detallar_oferta', id=oferta_id))

        if (oferta.publicacion_solicitado.id_usuario != session.get('user_id')):
            flash('No tienes permiso para rechazar esta oferta.', 'error')
            return redirect(url_for('/ofertas/detallar_oferta', id=oferta_id))
        
        descripcion_rechazo = request.form.get('descripcion')
        if not descripcion_rechazo:
            flash("Descripción de rechazo es requerida", "error")
            return redirect(url_for('/ofertas/detallar_oferta', id=oferta_id))
        estado_pendiente = Estado.query.filter_by(nombre="pendiente").first()
        if(oferta.estado != estado_pendiente.id):
            flash("La oferta no se puede rechazar", "error")
            return redirect(url_for('/ofertas/detallar_oferta', id=oferta_id))
        
        estado_rechazada = Estado.query.filter_by(nombre="rechazada").first()

        # Actualizar el estado y la descripción de la oferta
        oferta.estado = estado_rechazada.id
        oferta.descripcion = descripcion_rechazo
        db.session.commit()
        Notificacion.responderOferta(oferta.id)
        flash("Oferta rechazada con éxito", "success")
        return redirect(url_for('/ofertas/detallar_oferta', id=oferta_id))
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('/ofertas/detallar_oferta', id=oferta_id))