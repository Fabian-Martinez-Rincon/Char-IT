from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class RegistrarColbForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=255)])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    submit = SubmitField('Registrar')
