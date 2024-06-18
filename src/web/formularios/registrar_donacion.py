
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

class RegistrarDonacionForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=6, max=255)])
    telefono = StringField('Teléfono', validators=[Length(min=6, max=50)])
    monto = StringField('Monto', validators=[Length(min=1, max=255)])
    submit = SubmitField('Registrar Donación')
    # ¿Nombre y apellido del donante?