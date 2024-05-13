from src.core.models.database import db
from src.core.models.usuario import Usuario
from src.web.formularios.editar_perfil import EditarPerfilForm
from flask import (session, Blueprint, flash, redirect, url_for, request, render_template)


bp = Blueprint("editarPerfil", __name__)

@bp.route("/editarPerfil/<int:usuario_id>", methods=['GET'])
def editarPerfilGo(usuario_id: int):
    """
    Muestra el formulario para editar el perfil de un usuario.
    """
    usuario = Usuario.query.get_or_404(usuario_id)
    
    if (usuario.id != session.get('user_id')):
        flash("No tienes permiso para editar este perfil.", "error"); 
        return redirect(url_for("root.perfil", usuario_id=usuario.id))
    
    form = EditarPerfilForm()
    form.password.data = usuario.password
    return render_template("editarPerfil.html", form=form, usuario_id=usuario.id, usuario=usuario)

@bp.route("/editarPerfil", methods=['POST'])
def editarPerfil():
    form = EditarPerfilForm()
    if form.validate_on_submit():
        password = form.password.data
        id = request.form['usuario_id']
        usuario = Usuario.query.get(id)
        
        if (usuario.id != session.get('user_id')):
            flash("No tienes permiso para editar este perfil.", "error")
            return redirect(url_for("root.perfil", usuario_id=usuario.id))
        
        usuario.password = password
        db.session.commit()
        flash("El perfil se ha actualizado correctamente.", "success")
        return redirect(url_for("root.perfil", usuario_id=usuario.id))
    return render_template("editarPerfil.html", form=form)

