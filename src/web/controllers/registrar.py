from flask import render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from src.core.models.database import db
from src.web.formularios.registrar import RegisterForm
from src.core.models.usuario import Usuario  # Asegúrate de que la importación es correcta
from flask import Blueprint
from src.web.controllers.root import index_get

bp = Blueprint("registrar", __name__)

from flask import render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from src.core.models.database import db
from src.web.formularios.registrar import RegisterForm
from src.core.models.usuario import Usuario
from flask import Blueprint

bp = Blueprint("registrar", __name__)

@bp.route('/registrar_usuario', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = Usuario.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Ya existe un usuario registrado con ese mail', 'error')
            return redirect(url_for('registrar.register'))  # Asegúrate de que el nombre de la función es correcto
        if len(form.password.data) < 8:
            flash('La contraseña debe tener mínimo 8 caracteres', 'error')
            return render_template('owner/registrar.html', form=form)
        
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
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f'{err}', 'error')
    return render_template('owner/registrar.html', form=form)

