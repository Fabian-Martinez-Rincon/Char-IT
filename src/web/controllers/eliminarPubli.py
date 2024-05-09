from flask import redirect, url_for, flash, Blueprint, session
from src.core.models.publicacion import Publicacion
from src.core.models.database import db
bp = Blueprint("eliminarPubli", __name__)

@bp.route("/eliminarPubli/<int:publicacion_id>", methods=['GET'])
def eliminarPubli(publicacion_id):
    # Verifica si el usuario actual es el propietario de la publicación
    
    Publi = Publicacion.query.get_or_404(publicacion_id)
    if Publi.id_usuario != session.get('user_id'):
        flash('No tienes permiso para editar esta publicación.', 'error')
        return redirect(url_for('root.publicaciones_get'))
    
    db.session.delete(Publi)
    db.session.commit()
    flash('La publicación ha sido eliminada correctamente.', 'success')
    return redirect(url_for('root.mis_publicaciones_get'))

