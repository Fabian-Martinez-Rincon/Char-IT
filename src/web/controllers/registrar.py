from flask import render_template, redirect, url_for, flash, session , request
from werkzeug.security import generate_password_hash
from src.core.models.database import db
from src.web.formularios.registrar import RegisterForm
from src.core.models.usuario import Usuario
from flask import Blueprint
from datetime import date

bp = Blueprint("registrar", __name__)

@bp.route('/registrar_usuario', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = Usuario.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Ya existe un usuario registrado con ese mail', 'error')
            form.email.data = ''
            return render_template('/comunes/registrar.html', form=form, password=request.form['password'])
        
        existing_user_dni = Usuario.query.filter_by(dni=form.dni.data).first()
        if existing_user_dni:
            flash('Ya existe un usuario registrado con ese dni', 'error')
            form.dni.data = ''
            return render_template('/comunes/registrar.html', form=form, password=request.form['password'])

        if len(form.password.data) < 8:
            flash('La contraseña debe tener mínimo 8 caracteres', 'error')
            form.password.data = ''
            return render_template('/comunes/registrar.html', form=form,password=request.form['password'])
        
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = Usuario(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
            password=hashed_password,
            dni=form.dni.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            telefono=form.telefono.data,
            id_rol=1
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Fue registrado correctamente', 'success')
            return redirect(url_for('root.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'ups ocurrio un error: {e}', 'error')
    else:
        password = request.form.get('password', '')
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                if (err == 'This field is required.'):
                    flash(f'El campo {fieldName} es obligatorio', 'error')
                else:
                    form.fecha_nacimiento.data = None
                    form.fecha_nacimiento.data = ''
                    flash(f'{err}', 'error')
        return render_template('/comunes/registrar.html', form=form, password=password)
    return render_template('/comunes/registrar.html', form=form, password='')
