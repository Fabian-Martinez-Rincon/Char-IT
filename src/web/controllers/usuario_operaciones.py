from flask import request, redirect, url_for, flash, Blueprint, session, jsonify, render_template
from src.core.models.publicacion import Publicacion
from src.core.models.oferta import Oferta
from src.core.models.estado import Estado
from src.core.models.usuario import Usuario
from src.core.models.database import db
from src.core.models.notificacion import Notificacion

bp = Blueprint("usuario_operaciones", __name__)

@bp.route("/penalizar_usuario/<int:user_id>", methods=['POST'])
def penalizar_usuario(user_id):
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.usuarios_generales_get'))
    if session.get('rol_id') != 3:
        flash('No tienes permisos para realizar esta operación.', 'error')
        return redirect(url_for('root.usuarios_generales_get'))

    motivo = request.json.get('motivo')
    if not motivo:
        return jsonify({"success": False, "error": "El motivo es obligatorio."}), 400
    try:
        user = Usuario.query.get_or_404(user_id)
        user.penaltis += 1
        if user.penaltis > 2:
            Notificacion.informarEliminacionUsuario(user.id, motivo)
            # db.session.delete(user)
            eliminar_publicaciones_usuario(user.id)
            db.session.commit()
            flash(f'El usuario fue penalizado y eliminado con éxito', 'success')
            return jsonify({"success": True, "action": "deleted"})
        db.session.commit()
        Notificacion.informarPenalizacion(user.id, motivo)
        flash(f'El usuario fue penalizado con éxito', 'success')
        return jsonify({"success": True, "action": "penalized"})
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

@bp.route("/eliminar_usuario/<int:user_id>", methods=['DELETE'])
def eliminar_usuario(user_id):
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.usuarios_generales_get'))
    if session.get('rol_id') != 3:
        flash('No tienes permisos para realizar esta operación.', 'error')
        return redirect(url_for('root.usuarios_generales_get'))

    motivo = request.json.get('motivo')
    if not motivo:
        return jsonify({"success": False, "error": "El motivo es obligatorio."}), 400

    try:
        user = Usuario.query.get_or_404(user_id)
        eliminar_publicaciones_usuario(user.id)
        user.penaltis = 3  # Establecer penalizaciones en 3 antes de eliminar
        Notificacion.informarEliminacionUsuario(user.id, motivo)
        # db.session.delete(user)
        db.session.commit()
        flash(f'Usuario General eliminado correctamente', 'success')
        return jsonify({"success": True, "error": f'Usuario {user.email} eliminado correctamente. Motivo: {motivo}'})
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el usuario: {str(e)}', 'error')
        return jsonify({"success": False, "error": str(e)})
    


def eliminar_publicaciones_usuario(user_id):
    publicaciones = Publicacion.query.filter_by(id_usuario=user_id).all()
    cancelada = Estado.query.filter_by(nombre="cancelada").first()

    for publicacion in publicaciones:
        # Busca las ofertas con estado pendiente para notificar el cambio de estado
        ofertas_relacionadas = Oferta.query.join(Estado, Estado.id == Oferta.estado).filter(
            ((Oferta.ofrecido == publicacion.id) | (Oferta.solicitado == publicacion.id)) &
            ((Estado.nombre == "pendiente") | (Estado.nombre == "aceptada"))
        ).all()

        # Cambiar el estado de todas las ofertas pendientes que involucran esta publicación a "cancelada"
        for oferta in ofertas_relacionadas:
            oferta.estado = cancelada.id
            oferta.descripcion = f"La oferta fue cancelada por la eliminación de la publicación {publicacion.titulo}"
            otra_publicacion_id = oferta.ofrecido if oferta.ofrecido != publicacion.id else oferta.solicitado
            otra_publicacion = Publicacion.query.get(otra_publicacion_id)
            if otra_publicacion.id_usuario != user_id:
                Notificacion.cancelarOferta(oferta.id, otra_publicacion.id_usuario)

        Notificacion.eliminarPublicacion(publicacion.id)
        publicacion.id_visibilidad = 3  # Cambiar la visibilidad de la publicación a "eliminada"
        db.session.add(publicacion)

    db.session.commit()