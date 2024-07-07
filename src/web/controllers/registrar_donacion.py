from datetime import datetime
from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for, session
from src.core.models.database import db
from src.core.models.usuario import Usuario
from src.core.models.donacion import Donacion
from src.web.formularios.registrar_donacion import RegistrarDonacionForm
from src.core.models.notificacion import Notificacion

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
        nombre = form.nombre.data
        apellido = form.apellido.data
        telefono = form.telefono.data if 'telefono' in request.form else None
        usuario = Usuario.query.filter_by(email=email).first()
        monto = form.monto.data
        id_tipo = 2 # Tipo Efectivo

        if not nombre and not apellido:
            if usuario:
                if usuario.id_rol != 1:
                    flash('El donante no puede ser ni Dueño, ni Colaborador. Complete los campos como corresponde.', 'error')
                    return render_template('colaborador/registrar_donacion.html', form=form)
                nombre = usuario.nombre
                apellido = usuario.apellido
                telefono = usuario.telefono
            else:
                flash('El usuario no se encuentra registrado. Complete los campos como corresponde.', 'error')
                return render_template('colaborador/registrar_donacion.html', form=form)
        else:
             if usuario:
                flash('El Usuario ya se encuentra registrado. Complete los campos como corresponde.', 'error')
                form.nombre.data = ""
                form.apellido.data = ""
                form.telefono.data = ""
                return render_template('colaborador/registrar_donacion.html', form=form)

        donacion = Donacion(
            email=email, 
            nombre=nombre,
            apellido=apellido,
            telefono=telefono, 
            monto=monto, 
            id_tipo=id_tipo)
        db.session.add(donacion)
        db.session.commit()
        Notificacion.donacionEfectivo(donacion.id)
        flash('Donación registrada con éxito.', 'success')
        return redirect(url_for('registrar_donacion.registrar_donacion'))
    
    return render_template("/colaborador/registrar_donacion.html", form=form)