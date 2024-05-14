from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from src.core.models.filial import Filial  # Importa el modelo Filial
from src.core.models.usuario import Usuario
from src.core.models.publicacion import Publicacion
from src.core.models.database import db
from src.web.formularios.inicio_sesion import LoginForm  # Asegúrate que esta es la ruta correcta
import subprocess
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
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol == 1 :  
                    flash('No tienes permiso para realizar esta operacion.', 'error')
                    return redirect(url_for('root.index_get'))
    try:
        usuarios_rol_2 = Usuario.query.filter(Usuario.id_rol == 1).all()
        return render_template("/owner/usuarios_generales.html", usuarios=usuarios_rol_2)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
    
@bp.get("/colaboradores")
def usuarios_colaboradores_get():
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol != 3:  
                flash('No tienes permiso para realizar esta operacion.', 'error')
                return redirect(url_for('root.index_get'))
    try:
        usuarios_rol_3 = Usuario.query.filter(Usuario.id_rol == 2).all()
        return render_template("/owner/usuarios_colaboradores.html", usuarios=usuarios_rol_3)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@bp.get("/publicaciones")
def publicaciones_get():
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    try:
        todas_las_publicaciones = Publicacion.query.filter_by(id_visibilidad=1).filter(Publicacion.id_usuario != session.get('user_id')).all()
        if not todas_las_publicaciones:
            mensaje = "No hay Publicaciones disponibles"
            return render_template("/owner/publicaciones.html", mensaje=mensaje)
        return render_template("/owner/publicaciones.html", publicaciones=todas_las_publicaciones)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@bp.get("/mispublicaciones")
def mis_publicaciones_get():
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol != 1 :  
                    flash('No tienes permiso para realizar esta operacion.', 'error')
                    return redirect(url_for('root.index_get'))
    try:
        mis_publicaciones = Publicacion.query.filter_by(id_usuario=session['user_id']).all()
        if not mis_publicaciones:
            mensaje = "No hay Publicaciones disponibles"
            return render_template("/owner/mis-publicaciones.html", mensaje=mensaje)
        return render_template("/owner/mis-publicaciones.html", publicaciones=mis_publicaciones)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@bp.get("/publicaciones/<int:publicacion_id>")
def publicacion_detalle(publicacion_id):
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    publicacion = Publicacion.query.get_or_404(publicacion_id)
    return render_template("publicaciones/detalle.html", publicacion=publicacion)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Simulación de búsqueda de usuario y verificación de contraseña
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:  # Esto debería usar hashing en un caso real
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
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    session.pop('user_id', None)
    session['logged_in'] = False
    flash('You have been logged out.', 'success')
    return redirect(url_for('root.index_get'))

@bp.route('/perfil')
def perfil():
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    if session.get('user_id'):
        user = Usuario.query.get(session.get('user_id'))
        return render_template('perfil.html', user=user)
    else:
        flash('You must be logged in to view your profile.', 'warning')
        return redirect(url_for('root.index_get'))

@bp.route("/eliminar_publicaciones")
def eliminar_publicaciones():
    try:
        # Eliminar todas las publicaciones
        Publicacion.query.delete()
        # Confirmar los cambios en la base de datos
        db.session.commit()
        # Redirigir a alguna página de confirmación o mostrar un mensaje de éxito
        flash('Todas las publicaciones han sido eliminadas correctamente.', 'success')
        return redirect(url_for('root.publicaciones_get'))  # Cambia 'ruta_a_tu_pagina_de_confirmacion' por la ruta adecuada
    except Exception as e:
        # En caso de error, deshacer cualquier cambio en la base de datos y mostrar un mensaje de error
        db.session.rollback()
        flash(f"No se pudieron eliminar las publicaciones. Error: {str(e)}", 'error')
        return redirect(url_for('root.publicaciones_get'))  # Cambia 'ruta_a_tu_pagina_de_error' por la ruta adecuada

@bp.route('/resetdb')
def reset_db():
    subprocess.call(["flask", "seeddb"])  # Llama al comando CLI desde la vista
    return redirect(url_for('root.index_get'))  # Redirige a alguna página después de ejecutar el comando
