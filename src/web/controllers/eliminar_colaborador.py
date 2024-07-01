from flask import request, redirect, url_for, flash, Blueprint, session, jsonify
from src.core.models.usuario import Usuario
from src.core.models.database import db

bp = Blueprint("eliminar_colaborador", __name__)

@bp.route("/eliminar_colaborador/<int:user_id>", methods=['DELETE'])
def eliminar_colaborador(user_id):
    if not session.get('user_id'):
        return jsonify({"success": False, "error": "Debes iniciar sesión para realizar esta operación."}), 401
    if session.get('rol_id') != 3:  # No es owner
        return jsonify({"success": False, "error": "No tienes permisos para realizar esta operación."}), 403

    try:
        user = Usuario.query.get_or_404(user_id)
        user.penaltis = 3
        db.session.commit()
        flash(f'Usuario {user.email} eliminado correctamente', 'success')
        return jsonify({"success": True, "message": f'Usuario {user.email} eliminado correctamente.'})
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el usuario: {str(e)}', 'error')
        return jsonify({"success": False, "error": str(e)}), 500
