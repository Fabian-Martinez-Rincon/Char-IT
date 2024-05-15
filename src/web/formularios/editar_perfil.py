from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import DataRequired, Length


class EditarPerfilForm(FlaskForm): 
    password_actual = PasswordField('Contraseña Actual', validators=[DataRequired()])
    nueva_password = PasswordField('Nueva Contraseña', validators=[DataRequired()]) 
    submit = SubmitField('Actualizar')
    