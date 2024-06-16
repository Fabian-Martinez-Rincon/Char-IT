from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for, session
from src.core.models.database import db
from src.core.models.usuario import Usuario
from flask import (
    Blueprint,
    render_template
)

bp = Blueprint("registrar_donacion", __name__)

@bp.route("/registrar_donacion", methods=['GET','POST'])
def registrar_donacion():
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol != 2:  
                flash('No tienes permiso para realizar esta operacion.', 'error')
                return redirect(url_for('root.index_get'))
    return render_template("/colaborador/registrar_donacion.html")