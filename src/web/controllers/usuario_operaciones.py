from flask import redirect, url_for, flash, Blueprint, session, jsonify
from src.core.models.usuario import Usuario
from src.core.models.database import db

bp = Blueprint("usuario_operaciones", __name__)

@bp.route("/penalizar_usuario/<int:user_id>", methods=['GET'])
def penalizar_usuario(user_id):
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.usuarios_generales_get'))
    if session.get('rol_id') != 3:  # Asegúrate de que sólo el rol adecuado pueda penalizar
        flash('No tienes permisos para realizar esta operación.', 'error')
        return redirect(url_for('root.usuarios_generales_get'))

    # Incrementar penalizaciones del usuario
    try:
        user = Usuario.query.get_or_404(user_id)
        user.penaltis += 1
        db.session.commit()
        flash(f'Penalización añadida correctamente al usuario {user.email}.', 'success')
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        flash(f'Error al penalizar al usuario: {str(e)}', 'error')
        return jsonify({"success": False, "error": str(e)})

@bp.route("/get_penaltis/<int:user_id>", methods=['GET'])
def get_penaltis(user_id):
    if not(session.get('user_id')):
        return jsonify({"success": False, "error": "Debes iniciar sesión para realizar esta operación."}), 401

    try:
        user = Usuario.query.get_or_404(user_id)
        return jsonify({"success": True, "penaltis": user.penaltis})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})