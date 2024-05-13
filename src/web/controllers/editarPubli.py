from src.core.models.database import db
from datetime import datetime
from src.core.models.publicacion import Publicacion
from src.core.models.usuario import Usuario
from src.web.formularios.editar_publi import EditarPubliForm
from flask import request, flash, redirect, url_for, session, render_template, abort
from flask import (
    Blueprint,
    render_template
)

bp = Blueprint("editarPubli", __name__)

@bp.route("/editarPubli/<int:producto_id>", methods=['GET'])
def editarPubliGo(producto_id: int):
    """
    Muestra el formulario para editar una publicación si el usuario es el propietario.
    """
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol != 1 :  
                    return redirect(url_for('root.index_get'))
    producto = Publicacion.query.get_or_404(producto_id)
    
    # Verifica si el usuario actual es el propietario de la publicación
    if producto.id_usuario != session.get('user_id'):
        flash('No tienes permiso para editar esta publicación.', 'error')
        return redirect(url_for('root.publicacion_detalle', publicacion_id=producto.id))

    # Si el usuario es el propietario, muestra el formulario de edición
    form = EditarPubliForm()
    form.descripcion.data = producto.descripcion
    return render_template('editarPubli.html', form=form, producto_id=producto_id, publicacion=producto)

@bp.route("/editarPubli", methods=['POST'])
def editarPubli():
    form = EditarPubliForm()
    if form.validate_on_submit():
        descripcion = form.descripcion.data
        id = request.form['producto_id']
        producto = Publicacion.query.get(id)
        
        # Verifica si el usuario actual es el propietario de la publicación
        if producto.id_usuario != session.get('user_id'):
            flash('No tienes permiso para editar esta publicación.', 'error')
            return redirect(url_for('root.publicacion_detalle', publicacion_id=producto.id))
        
        producto.descripcion = descripcion
        db.session.commit()
        flash('La publicación se ha actualizado correctamente.', 'success')
        return redirect(url_for('root.publicacion_detalle', publicacion_id=producto.id))
    return render_template("editarPubli.html", form=form)

