from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, ValidationError
from wtforms.validators import DataRequired, Length, Optional
from datetime import date

def validate_fecha_nacimiento(form, field):
    today = date.today()
    born = field.data
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    if age < 18:
        raise ValidationError("Debes tener al menos 18 años para registrarte.")

class RegisterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Length(max=255)])
    dni = StringField('DNI', validators=[Optional(), Length(min=8)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired(), validate_fecha_nacimiento], format='%Y-%m-%d')
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=50)])
    submit = SubmitField('Registrarme')
    