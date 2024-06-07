import os
from src.core.models.notificacion import Notificacion
from src.core.models.usuario import Usuario
from flask import render_template, request, flash, redirect, url_for, session, current_app
from src.web.formularios.ofertar_publi import OfertarPubli
from src.core.models.oferta import Oferta
from src.core.models.publicacion import Publicacion
from src.core.models.database import db
from datetime import time
from flask import (
    Blueprint,
    render_template
)


bp = Blueprint("ofertar_publi", __name__)

@bp.route("/ofertar_publi/<int:publicacion_id>", methods=['GET'])
def ofertar_publi_go(publicacion_id):
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol != 1 :  
                    flash('No tienes permiso para realizar esta operacion.', 'error')
                    return redirect(url_for('root.index_get'))

    # Obtén todas las publicaciones del usuario
    mis_publicaciones = Publicacion.query.filter_by(id_usuario=session['user_id']).filter(Publicacion.id_visibilidad.in_([1, 2])).all()
    lista_publi=[(i.id, i.titulo) for i in mis_publicaciones]

    if(len(lista_publi)==0):
        flash('No tienes publicaciones para ofertar.', 'error')
        return redirect(url_for('root.publicaciones_get'))
    
    form = OfertarPubli()
    # Llena el campo de selección de publicaciones
    form.publicacion.choices = lista_publi
    return render_template('/general/ofertar.html', form=form)

@bp.route("/ofertar_publi/<int:publicacion_id>", methods=['POST'])
def subir_oferta(publicacion_id):
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol != 1 :  
                    return redirect(url_for('root.index_get'))
    form = OfertarPubli() 
    mis_publicaciones = Publicacion.query.filter_by(id_usuario=session['user_id']).all()
    lista_publi=[(i.id, i.titulo) for i in mis_publicaciones]
    form.publicacion.choices = lista_publi
    if form.validate_on_submit():
        # Obtiene los datos del formulario
        ofrecido_id = form.publicacion.data
        solicitado_id = publicacion_id
        horarios = form.horarios.data
        fecha = form.fecha.data
        filial = form.filial.data
        estado = 1

        oferta_aux = Oferta.query.filter_by(ofrecido=ofrecido_id, solicitado=solicitado_id, estado = 1).first()
        if oferta_aux:
            flash('Ya has ofertado por esta publicación.', 'error')
            return redirect(url_for('root.publicaciones_get'))
        oferta_aux2 = Oferta.query.filter_by(ofrecido=solicitado_id, solicitado=ofrecido_id, estado = 1).first()
        if oferta_aux2:
            flash('Ya existe una oferta similar.', 'error')
            return redirect(url_for('root.publicaciones_get'))

        # Crea la nueva oferta
        nueva_oferta = Oferta(ofrecido=ofrecido_id, solicitado=solicitado_id, horaIntercambio=horarios, fechaIntercambio=fecha, filial=filial, estado=estado)
        db.session.add(nueva_oferta)
        db.session.commit()
        
        # Enviar notificación al usuario dueño de la otra publicación
        Notificacion.enviarOferta(nueva_oferta)
        flash('Oferta realizada con éxito.', 'success')
        return redirect(url_for('root.publicaciones_get'))
    return render_template('/general/ofertar.html', form=form)