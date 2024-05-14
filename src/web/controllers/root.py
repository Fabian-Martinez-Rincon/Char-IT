from flask import Blueprint, render_template, redirect, url_for, session, flash
from src.core.models.filial import Filial  # Importa el modelo Filial
from src.core.models.usuario import Usuario
from src.core.models.publicacion import Publicacion
from src.web.formularios.inicio_sesion import LoginForm  # Asegúrate que esta es la ruta correcta

from flask import (
    Blueprint,
    render_template
)

bp = Blueprint("root", __name__)

@bp.get("/")
def index_get():
    try:
        todas_las_filiales = Filial.query.all()
        return render_template("index.html", filiales=todas_las_filiales)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@bp.get("/generales")
def usuarios_generales_get():
    try:
        usuarios_rol_2 = Usuario.query.filter(Usuario.id_rol == 1).all()
        return render_template("/owner/usuarios_generales.html", usuarios=usuarios_rol_2)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
    
@bp.get("/colaboradores")
def usuarios_colaboradores_get():
    try:
        usuarios_rol_3 = Usuario.query.filter(Usuario.id_rol == 2).all()
        return render_template("/owner/usuarios_colaboradores.html", usuarios=usuarios_rol_3)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@bp.get("/publicaciones")
def publicaciones_get():
    try:
        todas_las_publicaciones = Publicacion.query.filter_by(id_visibilidad=1).all()
        return render_template("/owner/publicaciones.html", publicaciones=todas_las_publicaciones)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@bp.get("/mispublicaciones")
def mis_publicaciones_get():
    try:
        mis_publicaciones = Publicacion.query.filter_by(id_usuario=session['user_id']).all()
        return render_template("/owner/mis-publicaciones.html", publicaciones=mis_publicaciones)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@bp.get("/publicaciones/<int:publicacion_id>")
def publicacion_detalle(publicacion_id):
    publicacion = Publicacion.query.get_or_404(publicacion_id)
    return render_template("publicaciones/detalle.html", publicacion=publicacion)


from werkzeug.security import check_password_hash

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        # Usar check_password_hash para verificar la contraseña
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['logged_in'] = True
            session['rol_id'] = user.id_rol
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('root.index_get'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)


@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session['logged_in'] = False
    flash('You have been logged out.', 'success')
    return redirect(url_for('root.index_get'))

@bp.route('/perfil')
def perfil():
    if session.get('user_id'):
        user = Usuario.query.get(session.get('user_id'))
        return render_template('perfil.html', user=user)
    else:
        flash('You must be logged in to view your profile.', 'warning')
        return redirect(url_for('root.index_get'))


