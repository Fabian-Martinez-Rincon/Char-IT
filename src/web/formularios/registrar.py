from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Optional

class RegisterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(max=255)])
    dni = StringField('DNI', validators=[Optional(), Length(max=12)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired()], format='%Y-%m-%d')
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=50)])
    submit = SubmitField('Registrar')