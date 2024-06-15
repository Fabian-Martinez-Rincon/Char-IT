from flask import redirect, url_for, flash, Blueprint, session
from src.core.models.usuario import Usuario
from src.core.models.database import db

bp = Blueprint("eliminar_colaborador", __name__)

@bp.route("/eliminar_colaborador/<int:user_id>", methods=['GET'])
def eliminar_colaborador(user_id):
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
    if (session.get('rol_id') != 3): #No es owner
        flash('No tienes permisos para realizar esta operación.', 'error')
        return redirect(url_for('root.usuarios_colaboradores_get'))
    #Eliminar usuario colaborador
    try:
        user = Usuario.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash(f'Usuario {user.email} eliminado correctamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el usuario colaborador.', 'error')
    return redirect(url_for('root.usuarios_colaboradores_get'))