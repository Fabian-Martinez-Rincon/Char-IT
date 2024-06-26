from src.core.models.database import db
from datetime import datetime
from src.core.models.publicacion import Publicacion
from src.core.models.usuario import Usuario
from src.web.formularios.editar_publi import EditarPubliForm
from src.core.models.oferta import Oferta
from src.core.models.estado import Estado
from flask import request, flash, redirect, url_for, session, render_template, abort
from flask import (
    Blueprint,
    render_template
)

bp = Blueprint("editar_publi", __name__)

@bp.route("/editar_publi/<int:producto_id>", methods=['GET'])
def editar_publi_go(producto_id: int):
    """
    Muestra el formulario para editar una publicación si el usuario es el propietario.
    """
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol != 1 :  
                    flash('No tienes permiso para realizar esta operacion.', 'error')
                    return redirect(url_for('root.index_get'))
    producto = Publicacion.query.get_or_404(producto_id)
    
    # Verifica si el usuario actual es el propietario de la publicación
    if producto.id_usuario != session.get('user_id'):
        flash('No tienes permiso para editar esta publicación.', 'error')
        return redirect(url_for('root.publicacion_detalle', publicacion_id=producto.id))

    # Si el usuario es el propietario, muestra el formulario de edición
    form = EditarPubliForm()
    form.descripcion.data = producto.descripcion
    return render_template('/general/editar_publi.html', form=form, producto_id=producto_id, publicacion=producto)

@bp.route("/editar_publi", methods=['POST'])
def editar_publi():
    form = EditarPubliForm()
    if form.validate_on_submit():
        descripcion = form.descripcion.data
        id = request.form['producto_id']
        producto = Publicacion.query.get(id)
        
        # Verifica si el usuario actual es el propietario de la publicación
        if producto.id_usuario != session.get('user_id'):
            flash('No tienes permiso para editar esta publicación.', 'error')
            return redirect(url_for('root.publicacion_detalle', publicacion_id=producto.id))
        ofertas_involucradas = Oferta.query.join(Estado, Estado.id == Oferta.estado).filter(
            ((Oferta.ofrecido == id) | (Oferta.solicitado == id)) &
            ((Estado.nombre == "aceptada"))
        ).all()
        
        if (ofertas_involucradas):
            flash('No Puedes Editar esta Publicacion ya que tenes un intercambio pendiente.', 'error')
            return redirect(url_for('root.publicacion_detalle', publicacion_id=id))
        
        producto.descripcion = descripcion
        db.session.commit()
        flash('La publicación se ha actualizado correctamente.', 'success')
        return redirect(url_for('root.publicacion_detalle', publicacion_id=producto.id))
    return render_template("/general/editar_publi.html", form=form)
