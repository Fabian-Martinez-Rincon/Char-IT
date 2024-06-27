from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Optional

class DonacionForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    nombre = StringField('Nombre', validators=[Optional()])
    apellido = StringField('Apellido', validators=[Optional()])
    telefono = StringField('Teléfono', validators=[Optional()])
    descripcion = StringField('Descripción del Producto', validators=[DataRequired()])
    categoria = SelectField('Categoría del Producto', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Registrar Donación')
