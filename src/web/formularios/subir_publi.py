from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from src.core.models.categoria import Categoria  

class SubirPubliForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired(), Length(max=255)])
    descripcion = StringField('Descripcion', validators=[DataRequired(), Length(max=255)])
    horarios = StringField('Horarios', validators=[Length(max=255)])
    categoria = SelectField('Categoria', coerce=int, validators=[DataRequired()]) 
    submit = SubmitField('Publicar')
    submit_archivar = SubmitField('Archivar')

    def __init__(self, *args, **kwargs):
        super(SubirPubliForm, self).__init__(*args, **kwargs)
        # Obtén todas las categorías disponibles y llénalas en el campo de selección
        self.categoria.choices = [(categoria.id, categoria.nombre) for categoria in Categoria.query.all()]
