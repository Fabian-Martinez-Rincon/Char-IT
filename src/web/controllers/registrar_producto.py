from flask import render_template, request, redirect, url_for, flash, Blueprint, session
from src.core.models.database import db
from src.core.models.donacion import Donacion
from src.core.models.categoria import Categoria
from src.core.models.usuario import Usuario
from src.core.models.notificacion import Notificacion
from src.web.formularios.registrar_producto import DonacionForm  # Asegúrate de tener un formulario definido en forms.py

bp = Blueprint("registrar_producto", __name__)

@bp.route('/registrar_producto', methods=['GET', 'POST'])
def registrar_donacion():
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    # Verifica si el usuario actual es el propietario de la publicación
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol == 1 :  
                    flash('No tienes permiso para realizar esta operacion.', 'error')
                    return redirect(url_for('root.index_get'))
    form = DonacionForm()
    categorias = Categoria.query.all()
    form.categoria.choices = [(categoria.id, categoria.nombre) for categoria in categorias]

    if form.validate_on_submit():
        email = form.email.data
        descripcion = form.descripcion.data
        id_categoria = form.categoria.data
        nombre = form.nombre.data
        apellido = form.apellido.data
        telefono = form.telefono.data if 'telefono' in request.form else None
        usuario = Usuario.query.filter_by(email=email).first()
        
        if not nombre and not apellido:
            if usuario:
                if usuario.id_rol != 1:
                    flash('El donante no puede ser ni Dueño, ni Colaborador. Complete los campos como corresponde.', 'error')
                    return render_template('owner/registrar_producto.html', form=form)
                nombre = usuario.nombre
                apellido = usuario.apellido
                telefono = usuario.telefono
            else:
                flash('Usuario no registrado. Por favor, complete los datos requeridos.', 'error')
                return render_template('owner/registrar_producto.html', form=form)
        else:
             if usuario:
                flash('El Usuario ya se encuentra registrado. Complete los campos como corresponde.', 'error')
                formAux = DonacionForm()
                formAux.email.data = email
                formAux.descripcion.data = descripcion
                id_categoria = form.categoria.data
                return render_template('owner/registrar_producto.html', form=form)

        nueva_donacion = Donacion(
            email=email,
            descripcion=descripcion,
            id_categoria=id_categoria,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            id_tipo=1  
        )
        
        db.session.add(nueva_donacion)
        db.session.commit()
        Notificacion.donacionProducto(nueva_donacion.id)
        flash('Donación registrada con éxito', 'success')
        return redirect(url_for('registrar_producto.registrar_donacion'))

    return render_template('owner/registrar_producto.html', form=form)

