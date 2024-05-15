from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class EditarPubliForm(FlaskForm):
    descripcion = StringField('Nueva Descripción', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Actualizar')
