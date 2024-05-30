from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, HiddenField, IntegerField
from wtforms.validators import DataRequired, Length

class ComentarForm(FlaskForm):
    contenido = TextAreaField('', validators=[DataRequired(), Length(max=255)])
    comentario_padre_id = IntegerField(default=None)
    submit = SubmitField("Agregar comentario")
