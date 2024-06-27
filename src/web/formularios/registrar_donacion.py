
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Optional

class RegistrarDonacionForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=6, max=255), Email()])
    nombre = StringField('Nombre', validators=[Optional()])
    apellido = StringField('Apellido', validators=[Optional()])
    telefono = StringField('Teléfono', validators=[Optional()])
    monto = StringField('Monto', validators=[DataRequired(), Length(min=1, max=255)])
    submit = SubmitField('Registrar Donación')
    # ¿Nombre y apellido del donante?