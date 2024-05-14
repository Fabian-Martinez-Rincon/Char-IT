from flask import redirect, url_for, flash, Blueprint, session
from src.core.models.publicacion import Publicacion
from src.core.models.database import db
from src.core.models.usuario import Usuario

bp = Blueprint("cambiarVisibilidad", __name__)

@bp.route("/cambiarVisibilidad/<int:publicacion_id>", methods=['GET'])
def cambiarVisibilidad(publicacion_id):
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol != 1 :  
                    flash('No tienes permiso para realizar esta operacion.', 'error')
                    return redirect(url_for('root.index_get'))
    Publi = Publicacion.query.get_or_404(publicacion_id)
    if Publi.id_usuario != session.get('user_id'):
        flash('No tienes permiso para editar esta publicación.', 'error')
        return redirect(url_for('root.publicaciones_get'))
    
    if Publi.id_visibilidad == 1:
        Publi.id_visibilidad = 2
    else:
        Publi.id_visibilidad = 1
    db.session.commit()
    flash('La publicación se ha actualizado correctamente.', 'success')
    return redirect(url_for('root.publicacion_detalle', publicacion_id=publicacion_id))