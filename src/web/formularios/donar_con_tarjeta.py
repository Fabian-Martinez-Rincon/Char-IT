from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, DateTimeField, StringField, SubmitField, SelectField, TimeField, ValidationError, FloatField
from wtforms.validators import DataRequired, Length
from src.core.models.filial import Filial
from wtforms.validators import NumberRange
import re
from wtforms.validators import ValidationError, Regexp


def validar_luhn(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10 == 0

def validar_numero_tarjeta(form, field):
    card_number = field.data  
    if not card_number.isdigit() or len(card_number) != 16:        
        raise ValidationError('El número de la tarjeta debe tener exactamente 16 dígitos.')
    if not validar_luhn(card_number):        
        raise ValidationError('El número de la tarjeta no es válido.')

def validar_fecha_expiracion(form, field):
    if not re.match(r'^(0[1-9]|1[0-2])\/([0-9]{2})$', field.data):
        raise ValidationError('La fecha de expiración debe estar en el formato MM/AA.')    
    
class DonarConTarjeta(FlaskForm):        
    monto = DecimalField('Monto', validators=[DataRequired(), NumberRange(min=0.00)])
    tarjetas_habilitadas = SelectField('Seleccione una tarjeta', choices=[('VISA', 'Visa'), ('MASTERCARD', 'Mastercard'), ('AMEX', 'American Express'), ('VISA ELECTRON', 'Visa Electrón'), ('ARGENCARD', 'Argencard'),('CABAL', 'Cabal'), ('COOPEPLUS', 'Coopleplus'), ('ITALCRED', 'Italcred'), ('TARJETANARANJA', 'Tarjeta Naranja'), ('TARJETANATIVA', 'Tarjeta Nativa') ], validators=[DataRequired()])        
    numero_tarjeta = StringField('Número de tarjeta', validators=[
        DataRequired(),
        validar_numero_tarjeta,
        Regexp(r'^\d{16}$', message="El número de tarjeta debe tener exactamente 16 dígitos.")
    ])    
    fecha_expiracion = StringField('Fecha de Expiración (MM/AA)', validators=[DataRequired(), validar_fecha_expiracion])
    codigo_seguridad = StringField('CVV', validators=[DataRequired()])
    nombre_titular = StringField('Nombre del titular', validators=[DataRequired()])           
    submit = SubmitField('Donar')
