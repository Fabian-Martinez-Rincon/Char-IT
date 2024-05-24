from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from src.core.models.filial import Filial

class OfertarPubli(FlaskForm):
    publicacion = SelectField('Seleccione una publicación', coerce=int, validators=[DataRequired()])
    horarios = StringField('Horarios', validators=[DataRequired(), Length(max=255)])
    filial = SelectField('Filial a escoger', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Enviar oferta')

    def __init__(self, *args, **kwargs):
        super(OfertarPubli, self).__init__(*args, **kwargs)
        self.filial.choices = [(filial.id, filial.nombre) for filial in Filial.query.all()]
