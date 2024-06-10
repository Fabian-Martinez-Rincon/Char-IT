from flask import Flask, request, flash, redirect, url_for, Blueprint, session, render_template
from src.core.models.database import db
from src.core.models.oferta import Oferta
from src.core.models.estado import Estado
from src.core.models.usuario import Usuario
from src.core.models.notificacion import Notificacion
from src.core.models.publicacion import Publicacion
from src.core.models.filial import Filial
from src.core.models.visibilidad import Visibilidad
bp = Blueprint("confirmarIntercambio", __name__)

@bp.route('/confirmarIntercambio/<int:oferta_id>', methods=['GET', 'POST'])
def confirmarIntercambio(oferta_id):
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
            flash("No puedes confirmar el intercambio, ya que es una ofertarechazada", "error")
            return redirect(url_for('pendientes.pendientes'))
        
        if (intercambio.estado == Estado.query.filter_by(nombre="pendiente").first().id):
            flash("No puedes confirmar el intercambio, ya que es una oferta pendiente", "error")
            return redirect(url_for('pendientes.pendientes'))

        if (intercambio.estado == Estado.query.filter_by(nombre="cancelada").first().id):
            flash("No puedes confirmar el intercambio, ya que es una oferta cancelada", "error")
            return redirect(url_for('pendientes.pendientes'))
        
        if (intercambio.estado == Estado.query.filter_by(nombre="finalizada").first().id):
            flash("No puedes confirmar el intercambio, su estado es finalizado", "error")
            return redirect(url_for('pendientes.pendientes'))
        
        # Actualizar el estado y la descripción de la oferta
        
        
        intercambio.estado = Estado.query.filter_by(nombre="finalizada").first().id
        intercambio.descripcion = "Intercambio confirmado con éxito"
        visibilidad_eliminada = Visibilidad.query.filter_by(estado="Eliminada").first().id
        solicitado = Publicacion.query.filter_by(id=intercambio.solicitado).first()
        ofrecido  = Publicacion.query.filter_by(id=intercambio.ofrecido).first()
        solicitado.id_visibilidad = visibilidad_eliminada
        ofrecido.id_visibilidad = visibilidad_eliminada        

        db.session.commit()
        Notificacion.confirmarIntercambio(intercambio.id) # CREAR LA NOTIFICACION DE CONFIRMACION DE INTERCAMBIO
        flash("Intercambio confirmado con éxito", "success")
        intercambio = Oferta.query.get(oferta_id)        
        # Obtén los valores de los atributos de la oferta        
        return redirect(url_for('pendientes.pendientes'))
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "error")       
        return redirect(url_for('pendientes.pendientes'))