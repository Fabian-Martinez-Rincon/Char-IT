from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class EditarPerfilForm(FlaskForm): 
    password_actual = StringField('Contraseña Actual', validators=[DataRequired()])
    nueva_password = StringField('Nueva Contraseña', validators=[DataRequired(), Length(min=8, max=255)]) 
    submit = SubmitField('Actualizar')