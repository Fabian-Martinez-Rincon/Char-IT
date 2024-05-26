from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import DateField, DateTimeField, StringField, SubmitField, SelectField, TimeField, ValidationError
from wtforms.validators import DataRequired, Length
from src.core.models.filial import Filial

def validate_date(form, field):
    if field.data < datetime.now().date():
        raise ValidationError('La fecha no puede ser anterior a la actual.')
    if field.data.weekday() >= 5:
        raise ValidationError('No se permiten fechas en sábado o domingo.')

"""
def validate_hours(form, field):
    start_time = datetime.time(hour=8, minute=0, second=0)
    end_time = datetime.time(hour=16, minute=0, second=0)

    if field.data < start_time or field.data > end_time:
        raise ValidationError('El horario debe estar entre las 8 AM y las 4 PM.')"""

class OfertarPubli(FlaskForm):
    publicacion = SelectField('Seleccione una publicación', coerce=int, validators=[DataRequired()])
    filial = SelectField('Filial a escoger', coerce=int, validators=[DataRequired()])
    fecha = DateField('Fecha propuesta', validators=[DataRequired(),validate_date], format='%Y-%m-%d')
    horarios = StringField('Horarios', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Enviar oferta')

    def __init__(self, *args, **kwargs):
        super(OfertarPubli, self).__init__(*args, **kwargs)
        self.filial.choices = [(filial.id, filial.nombre) for filial in Filial.query.all()]