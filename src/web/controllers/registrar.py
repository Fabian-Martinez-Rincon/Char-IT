from flask import render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from src.core.models.database import db
from src.web.formularios.registrar import RegisterForm
from src.core.models.usuario import Usuario  # Asegúrate de que la importación es correcta
from flask import Blueprint
from src.web.controllers.root import index_get

bp = Blueprint("registrar", __name__)

@bp.route('/registrar_usuario', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            existing_user = Usuario.query.filter_by(email=form.email.data).first()
            if existing_user is None:
                hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
                new_user = Usuario(
                    nombre=form.nombre.data,
                    apellido=form.apellido.data,
                    email=form.email.data,
                    password=hashed_password,
                    dni=form.dni.data,
                    fecha_nacimiento=form.fecha_nacimiento.data,
                    telefono=form.telefono.data,
                    id_rol=form.id_rol.data 
                )
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful!', 'success')
                print('no entiendo nada')
                return redirect(url_for('index_get'))  # Asegúrate de que el nombre de la función es correcto
            else:
                print('El mail ya esta registraado :c')
                flash('Email already registered.', 'danger')
        except Exception as e:
            print(f"Se rompio todo {e}")
            db.session.rollback()
            flash('Failed to register due to an error: {}'.format(e), 'danger')
    return render_template('owner/registrar.html', form=form)
