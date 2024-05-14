import os
from werkzeug.utils import secure_filename
from flask import render_template, request, flash, redirect, url_for, session, current_app
from src.web.formularios.subir_publi import SubirPubliForm
from src.core.models.publicacion import Publicacion
from src.core.models.categoria import Categoria
from src.core.models.database import db
from flask import (
    Blueprint,
    render_template
)

bp = Blueprint("subirPubli", __name__)
@bp.route("/subirPubli", methods=['GET'])
def subirPubliGo():
    form = SubirPubliForm()
    categorias = Categoria.query.all()  # Obtén todas las categorías disponibles
    form.categoria.choices = [(categoria.id, categoria.nombre) for categoria in Categoria.query.all()]  # Llena el campo de selección de categorías
    return render_template('subirPubli.html', form=form ,categorias=categorias)


@bp.route("/subirPubli", methods=['POST'])
def subirPubli():
    form = SubirPubliForm() 
    form.categoria.choices = [(categoria.id, categoria.nombre) for categoria in Categoria.query.all()]  # Llena el campo de selección de categorías
    categorias = Categoria.query.all()  # Obtén todas las categorías disponibles
    if form.validate_on_submit():
        titulo = form.titulo.data
        # Verifica si entre sus publicaciones hay otra con el mismo titulo
        mis_publicaciones = Publicacion.query.filter_by(id_usuario=session['user_id'])
        existing_public = mis_publicaciones.filter(Publicacion.titulo == titulo).first()
        if existing_public:
            flash('Ya tienes una publicación con el mismo título.', 'warning')
            return redirect(url_for('subirPubli.subirPubli'))
        descripcion = form.descripcion.data
        horarios = form.horarios.data
        categoria_id = form.categoria.data  # Obtiene el ID de la categoría seleccionada
        categoria_nombre = Categoria.query.get(categoria_id).nombre
        # Obtén la foto cargada en el formulario
        foto = request.files['foto']
        if foto:
            # Guarda la foto en el sistema de archivos
            nombre_archivo = secure_filename(foto.filename)
            ruta_foto = os.path.join(categoria_nombre, nombre_archivo)
            ruta_completa = os.path.join(current_app.config['UPLOAD_FOLDER'],"img", ruta_foto).replace(os.sep, "/")
            ruta_foto2 = os.path.join("img",categoria_nombre, nombre_archivo).replace(os.sep, "/")
            # Crea la carpeta si no existe
            os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
            foto.save(ruta_completa)
        #Verifica si se presionó el botón de publicar o archivar
        if 'submit' in request.form:
            id_visibilidad = 1  # Publicar
        elif 'submit_archivar' in request.form:
            id_visibilidad = 2  # Archivar

        # Crea una nueva instancia de Publicacion con los datos del formulario
        nueva_publicacion = Publicacion(
            titulo=titulo,
            descripcion=descripcion,
            filiales_horarios_dias=horarios,
            foto_path=ruta_foto2,
            id_usuario=session['user_id'],
            id_categoria=categoria_id,  # Asigna el ID de la categoría a la publicación
            id_visibilidad=id_visibilidad   )

        # Guarda la nueva publicación en la base de datos
        db.session.add(nueva_publicacion)
        db.session.commit()
        flash('La publicación se ha subido correctamente.', 'success')
        return redirect(url_for('root.mis_publicaciones_get'))
    return render_template('subirPubli.html', form=form,categorias=categorias)