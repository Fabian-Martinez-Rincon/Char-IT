from flask import Blueprint, render_template, session, flash, redirect, url_for
from src.core.models.donacion import Donacion
from src.core.models.database import db
from src.core.models.usuario import Usuario

bp = Blueprint('mis_donaciones', __name__)

@bp.route('/mis_donaciones')
def todas_donaciones():
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
    if (session.get('rol_id') != 1): #No es general
        flash('No tienes permisos para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    email = Usuario.query.filter_by(id=session.get('user_id')).first().email
    mis_donaciones = Donacion.query.filter_by(email=email).order_by(Donacion.fecha_donacion.asc()).all()
    mis_donaciones.reverse()
    if not mis_donaciones:
        mensaje = "No hay donaciones disponibles."
        return render_template('general/mis_donaciones.html', mensaje=mensaje)
    
    return render_template('general/mis_donaciones.html', donaciones=mis_donaciones)