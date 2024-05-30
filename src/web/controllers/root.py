from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from src.core.models.filial import Filial  # Importa el modelo Filial
from src.core.models.usuario import Usuario
from src.core.models.publicacion import Publicacion
from src.core.models.comentario import Comentario
from src.core.models.database import db
from src.web.formularios.inicio_sesion import LoginForm  # Asegúrate que esta es la ruta correcta
from src.web.formularios.comentar import ComentarForm
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
        if not usuarios_rol_2:
            mensaje = "No existen usuarios generales cargados en el sistema"
            return render_template("/owner/usuarios_generales.html", mensaje=mensaje)
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
        if not usuarios_rol_3:
            mensaje = "No existen usuarios colaboradores cargados en el sistema"
            return render_template("/owner/usuarios_colaboradores.html", mensaje=mensaje)
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
            return render_template("/comunes/publicaciones.html", mensaje=mensaje)
        return render_template("/comunes/publicaciones.html", publicaciones=todas_las_publicaciones)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@bp.get("/mis_publicaciones")
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
        mis_publicaciones = Publicacion.query.filter(
            Publicacion.id_usuario == session['user_id'],
            Publicacion.id_visibilidad != 3
        ).all()
        if not mis_publicaciones:
            mensaje = "No hay Publicaciones disponibles"
            return render_template("/general/mis_publicaciones.html", mensaje=mensaje)
        return render_template("/general/mis_publicaciones.html", publicaciones=mis_publicaciones)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@bp.route("/publicaciones/<int:publicacion_id>", methods=['GET', 'POST'])
def publicacion_detalle(publicacion_id):
    if not session.get('user_id'):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))

    # Obtener la publicación junto con sus comentarios y autores
    publicacion = Publicacion.query \
        .options(db.joinedload(Publicacion.comentarios_publicacion).joinedload(Comentario.autor)) \
        .get_or_404(publicacion_id)
    
    print(publicacion.comentarios_publicacion)

    comentarios_con_autores = []

    for comentario in publicacion.comentarios_publicacion:        
        respuesta = comentario.respuesta        
        respuesta_con_autor = {
            'contenido': respuesta.contenido,
            'fecha_creacion': respuesta.fecha_creacion,
            'autor_nombre': respuesta.autor.nombre,
            'autor_apellido': respuesta.autor.apellido
        } if respuesta else None

        comentarios_con_autores.append({
            'contenido': comentario.contenido,
            'fecha_creacion': comentario.fecha_creacion,
            'autor_nombre': comentario.autor.nombre,
            'autor_apellido': comentario.autor.apellido,
            'padre': comentario.comentario_padre_id,
            'id':comentario.id,
            'respuesta': respuesta_con_autor
        })

    form = None
    formAnswer = None
    if (session.get('user_id') != publicacion.id_usuario) and (Usuario.query.get(session.get('user_id')).id_rol == 1):                                
        form = ComentarForm()   
        if form.validate_on_submit():            
            contenido = form.contenido.data         
            nuevo_comentario = Comentario(contenido=contenido, publicacion_id=publicacion_id, autor_id=session.get('user_id'))                       
            try:
                db.session.add(nuevo_comentario)                
                db.session.commit()                
                flash('¡Comentario agregado con éxito!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Ocurrió un error al agregar el comentario. Inténtalo nuevamente.', 'error')                
                print(f"An error occurred: {str(e)}")
            return redirect(url_for('root.publicacion_detalle', publicacion_id=publicacion_id))            

    elif (session.get('user_id') == publicacion.id_usuario):           
        formAnswer = ComentarForm()     
        if formAnswer.validate_on_submit():            
            contenido = formAnswer.contenido.data                                        
            comentario_padre_id = formAnswer.comentario_padre_id.data
            print(formAnswer.comentario_padre_id.data)              
            respuesta = Comentario(contenido=contenido, publicacion_id=publicacion_id, autor_id=session.get('user_id'), comentario_padre_id=comentario_padre_id)                                               
            try:
                db.session.add(respuesta)                
                db.session.commit()                
                flash('¡Respuesta enviada con exito!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Ocurrió un error al responder el comentario. Inténtalo nuevamente.', 'error')
                print(f"An error occurred: {str(e)}")                
            return redirect(url_for('root.publicacion_detalle', publicacion_id=publicacion_id))            
    return render_template("/publicaciones/detalle.html", publicacion=publicacion, comentarios=comentarios_con_autores, form=form, formAnswer=formAnswer)


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
            # flash('You have successfully logged in!', 'success')
            flash('Inicio de sesión Exitoso', 'success')
            return redirect(url_for('root.index_get'))
        else:
            flash('El mail o contraseña son incorrectos.', 'error')
    return render_template('/comunes/login.html', form=form)


@bp.route('/logout')
def logout():
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    session.pop('user_id', None)
    session['logged_in'] = False
    flash('Se ha cerrado la sesión correctamente.', 'success')
    return redirect(url_for('root.index_get'))

@bp.route('/perfil')
def perfil():
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    if session.get('user_id'):
        user = Usuario.query.get(session.get('user_id'))
        return render_template('/comunes/perfil.html', user=user)
    else:
        flash('You must be logged in to view your profile.', 'error')
        return redirect(url_for('root.index_get'))

@bp.route("/eliminar_publicaciones")
def eliminar_publicaciones():
    try:
        # Eliminar todas las publicaciones
        Publicacion.query.delete()
        # Confirmar los cambios en la base de datos
        db.session.commit()
        # Redirigir a alguna página de confirmación o mostrar un mensaje de éxito
        #flash('Todas las publicaciones han sido eliminadas correctamente.', 'success')
        return redirect(url_for('root.publicaciones_get'))  # Cambia 'ruta_a_tu_pagina_de_confirmacion' por la ruta adecuada
    except Exception as e:
        # En caso de error, deshacer cualquier cambio en la base de datos y mostrar un mensaje de error
        db.session.rollback()
        # flash(f"No se pudieron eliminar las publicaciones. Error: {str(e)}", 'error')
        return redirect(url_for('root.publicaciones_get'))  # Cambia 'ruta_a_tu_pagina_de_error' por la ruta adecuada

@bp.route("/eliminar_colaboradores")
def eliminar_colaboradores():
    try: 
        # Eliminar todos los colaboradores
        Usuario.query.filter(Usuario.id_rol == 2).delete()
        # Confirmar los cambios en la base de datos
        db.session.commit()
        # Redirigir a alguna página de confirmación o mostrar un mensaje de éxito
        # flash('Todos los colaboradores han sido eliminados correctamente.', 'success')
        return redirect(url_for('root.usuarios_colaboradores_get'))  # Cambia 'ruta_a_tu_pagina_de_confirmacion' por la ruta adecuada
    except Exception as e:
        # En caso de error, deshacer cualquier cambio en la base de datos y mostrar un mensaje de error
        db.session.rollback()
        # flash(f"No se pudieron eliminar los colaboradores. Error: {str(e)}", 'error')
        return redirect(url_for('root.usuarios_colaboradores_get'))
    
@bp.route("/eliminar_generales")
def eliminar_generales():
    try: 
        # Eliminar todos los usuarios generales        
        Publicacion.query.delete()
        db.session.commit()
        Usuario.query.filter(Usuario.id_rol == 1).delete()
        # Confirmar los cambios en la base de datos
        db.session.commit()
        # Redirigir a alguna página de confirmación o mostrar un mensaje de éxito
        #flash('Todos los usuarios generales han sido eliminados correctamente.', 'success')
        return redirect(url_for('root.usuarios_generales_get'))  # Cambia 'ruta_a_tu_pagina_de_confirmacion' por la ruta adecuada
    except Exception as e:
        # En caso de error, deshacer cualquier cambio en la base de datos y mostrar un mensaje de error
        db.session.rollback()
        # flash(f"No se pudieron eliminar los usuarios generales. Error: {str(e)}", 'error')
        return redirect(url_for('root.usuarios_generales_get'))
    
@bp.route('/resetdb')
def reset_db():
    subprocess.call(["flask", "seeddb"])  # Llama al comando CLI desde la vista
    return redirect(url_for('root.index_get'))  # Redirige a alguna página después de ejecutar el comando

@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404