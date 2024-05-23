from flask import redirect, url_for, flash, Blueprint, session
from src.core.models.usuario import Usuario
from src.core.models.publicacion import Publicacion
from src.core.models.database import db
bp = Blueprint("eliminar_publi", __name__)

@bp.route("/eliminar_publi/<int:publicacion_id>", methods=['GET'])
def eliminar_publi(publicacion_id):
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    # Verifica si el usuario actual es el propietario de la publicación
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol != 1 :  
                    flash('No tienes permiso para realizar esta operacion.', 'error')
                    return redirect(url_for('root.index_get'))
    Publi = Publicacion.query.get_or_404(publicacion_id)
    if Publi.id_usuario != session.get('user_id'):
        flash('No tienes permiso para editar esta publicación.', 'error')
        return redirect(url_for('root.publicaciones_get'))
    
    db.session.delete(Publi)
    db.session.commit()
    flash('La publicación ha sido eliminada correctamente.', 'success')
    return redirect(url_for('root.mis_publicaciones_get'))
