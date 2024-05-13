from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class EditarPerfilForm(FlaskForm): 
    password = StringField('Nueva Contraseña', validators=[DataRequired(), Length(min=8, max=255)]); 
    SubmitField = SubmitField('Actualizar');