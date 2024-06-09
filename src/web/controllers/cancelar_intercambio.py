from flask import Flask, request, flash, redirect, url_for, Blueprint, session, render_template
from src.core.models.database import db
from src.core.models.oferta import Oferta
from src.core.models.estado import Estado
from src.core.models.usuario import Usuario
from src.core.models.notificacion import Notificacion
from src.core.models.publicacion import Publicacion
from src.core.models.filial import Filial

bp = Blueprint("cancelarIntercambio", __name__)

@bp.route('/cancelarIntercambio/<int:oferta_id>', methods=['GET', 'POST'])
def cancelarIntercambio(oferta_id):
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    # Verifica si el usuario actual es el propietario de la publicación
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol == 1 :  
            flash('No tienes permiso para realizar esta operacion.', 'error')
            return redirect(url_for('root.index_get'))
    try:
        # Buscar la oferta correspondiente en la base de datos
        intercambio = Oferta.query.get(oferta_id)

        if not intercambio:
            flash("Intercambio  no encontrada", "error")
            return redirect(url_for('pedientes.pendientes'))      
        
        # descripcion_rechazo = request.form.get('descripcion')

        # if not descripcion_rechazo:
        #     flash("Descripción de rechazo es requerida", "error")
        #     return redirect(url_for('/ofertas/detallar_oferta', id=oferta_id))                   
        if (intercambio.estado == Estado.query.filter_by(nombre="rechazada").first().id):
            flash("No puedes cancelar el intercambio, ya que es una oferta rechazada", "error")
            return redirect(url_for('pendientes.pendientes'))
        
        if (intercambio.estado == Estado.query.filter_by(nombre="pendiente").first().id):
            flash("No puedes cancelar el intercambio, ya que es una oferta pendiente", "error")
            return redirect(url_for('pendientes.pendientes'))

        if (intercambio.estado == Estado.query.filter_by(nombre="cancelada").first().id):
            flash("No puedes cancelar el intercambio, ya que es una oferta cancelada", "error")
            return redirect(url_for('pendientes.pendientes'))
        
        if (intercambio.estado == Estado.query.filter_by(nombre="finalizada").first().id):
            flash("No puedes cancelar el intercambio, su estado es finalizado", "error")
            return redirect(url_for('pendientes.pendientes'))
        
        # Actualizar el estado y la descripción de la oferta
        
        
        intercambio.estado = Estado.query.filter_by(nombre="finalizada").first().id        
        intercambio.descripcion = request.form.get('descripcion') # LA DESCRIPCION LA DEBE PONER EL USUARIO
        db.session.commit()
        Notificacion.responderOferta(intercambio.id) # CREAR LA NOTIFICACION DE CONFIRMACION DE INTERCAMBIO
        flash("Intercambio cancelado con éxito", "success")
        intercambio = Oferta.query.get(oferta_id)        
        # Obtén los valores de los atributos de la oferta        
        return redirect(url_for('root.detallar_oferta', intercambio_id=intercambio.id))
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "error")       
        return redirect(url_for('pendientes.pendientes'))