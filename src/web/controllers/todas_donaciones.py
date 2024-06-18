from flask import Blueprint, render_template, session, flash, redirect, url_for
from src.core.models.donacion import Donacion
from src.core.models.database import db

bp = Blueprint('todas_donaciones', __name__)

@bp.route('/todas_donaciones')
def todas_donaciones():
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
    if (session.get('rol_id') != 3): #No es owner
        flash('No tienes permisos para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    donaciones = Donacion.query.order_by(Donacion.fecha_donacion.asc()).all()
    if not donaciones:
        mensaje = "No hay donaciones disponibles."
        return render_template('owner/todas_donaciones.html', mensaje=mensaje)
    
    return render_template('owner/todas_donaciones.html', donaciones=donaciones)
