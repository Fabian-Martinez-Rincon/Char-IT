import os
from src.core.models.usuario import Usuario
from flask import render_template, request, flash, redirect, url_for, session, current_app
from src.web.formularios.ofertar_publi import OfertarPubli
from src.core.models.publicacion import Publicacion
from src.core.models.database import db
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
    mis_publicaciones = Publicacion.query.filter_by(id_usuario=session['user_id']).all()
    lista_publi=[(i.id, i.titulo) for i in mis_publicaciones]
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
        id_publicacion = form.publicacion.data
        horarios = form.horarios.data
        filial = form.filial.data
        # Crea la nueva oferta
        #nueva_oferta = Oferta(id_publicacion=id_publicacion, id_usuario=session['user_id'], precio=precio, descripcion=descripcion)
        #db.session.add(nueva_oferta)
        #db.session.commit()
        flash('Oferta realizada con éxito.', 'success')
        return redirect(url_for('root.publicaciones_get'))
    return render_template('/general/ofertar.html', form=form)