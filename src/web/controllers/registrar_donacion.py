from datetime import datetime
from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for, session
from src.core.models.database import db
from src.core.models.usuario import Usuario
from src.core.models.donacion import Donacion
from src.web.formularios.registrar_donacion import RegistrarDonacionForm

from flask import (
    Blueprint,
    render_template
)

bp = Blueprint("registrar_donacion", __name__)

@bp.route("/registrar_donacion", methods=['GET'])
def registrar_donacion():
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol == 1:  
                flash('No tienes permiso para realizar esta operacion.', 'error')
                return redirect(url_for('root.index_get'))
    form = RegistrarDonacionForm()
    return render_template("/colaborador/registrar_donacion.html", form=form)

@bp.route("/registrar_donacion", methods=['POST'])
def registrar_donacion_post():
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol == 1:  
            flash('No tienes permiso para realizar esta operacion.', 'error')
            return redirect(url_for('root.index_get'))
        
    form = RegistrarDonacionForm()
    if form.validate_on_submit():
        email = form.email.data
        aux = Usuario.query.filter_by(email=email).first()
        telefono = form.telefono.data
        if (aux):
            telefono = Usuario.query.filter_by(email=email).first().telefono     
        elif not(aux) and not(telefono):
            flash('El usuario no se encuentra registrado. Complete los campos como corresponde.', 'error')
            return redirect(url_for('registrar_donacion.registrar_donacion', form=form))
        
        monto = form.monto.data
        id_categoria = 10 # Categoria Otros
        id_tipo = 2 # Tipo Efectivo
        donacion = Donacion(email=email, telefono=telefono, monto=monto, id_categoria=id_categoria, id_tipo=id_tipo)
        db.session.add(donacion)
        db.session.commit()
        flash('Donación registrada con éxito.', 'success')
        return redirect(url_for('root.index_get'))
    
    return render_template("/colaborador/registrar_donacion.html", form=form)