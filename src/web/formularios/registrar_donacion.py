
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, EmailField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Optional, NumberRange

class RegistrarDonacionForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=6, max=255), Email()])
    nombre = StringField('Nombre', validators=[Optional()])
    apellido = StringField('Apellido', validators=[Optional()])
    telefono = StringField('Teléfono', validators=[Optional()])
    monto = DecimalField('Monto', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Registrar Donación')
    # ¿Nombre y apellido del donante?