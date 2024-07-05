import os
from src.core.models.notificacion import Notificacion
from src.core.models.donacion import Donacion
from src.core.models.tipo import Tipo
from src.core.models.usuario import Usuario
from flask import render_template, request, flash, redirect, url_for, session, current_app
from src.web.formularios.donar_con_tarjeta import DonarConTarjeta
from src.core.models.banco import Banco
from src.core.models.database import db
from datetime import datetime
from datetime import time
from flask import (
    Blueprint,
    render_template
)


bp = Blueprint("donar_con_tarjeta", __name__)

@bp.route("/donar_con_tarjeta", methods= ['GET', 'POST'])
def donar_con_tarjeta():
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    if session.get('user_id'):
        rol = session.get('rol_id')
        if rol != 1 :  
                    flash('No tienes permiso para realizar esta operacion.', 'error')
                    return redirect(url_for('root.index_get'))            
    
    
    def validar_monto(form, tarjeta):
        return form.monto.data <= tarjeta.saldo
    
    def validar_tipo(form, tarjeta):
        return form.tarjetas_habilitadas.data == tarjeta.tipo
    
    def validar_fecha_expiracion(form, tarjeta):
        return form.fecha_expiracion.data == tarjeta.vencimiento
    
    def validar_codigo_seguridad(form, tarjeta):
        return form.codigo_seguridad.data == tarjeta.cvv    
    
    form = DonarConTarjeta()    

    try: 
        if form.validate_on_submit():        
            print('Validado')
            num_tarjeta = form.numero_tarjeta.data            
            tarjeta = Banco.query.filter_by(nro_tarjeta=num_tarjeta).first()
            if not tarjeta:
                flash('La tarjeta ingresada no está habilitada para donar.', 'error')
                return redirect(url_for('donar_con_tarjeta.donar_con_tarjeta'))
            print(tarjeta.activo)
            if not tarjeta.activo:
                flash('Fallo la conexión con el banco.', 'error')
                return redirect(url_for('donar_con_tarjeta.donar_con_tarjeta'))
            if tarjeta:                
                usuario = Usuario.query.filter_by(id=session.get('user_id')).first()               

                if tarjeta.nombre != usuario.nombre or tarjeta.apellido != usuario.apellido:
                    form.nombre_titular.data = ''
                    flash('La donación debe hacerce con una tarjeta a su nombre', 'error')
                    return render_template('/general/donar_con_tarjeta.html', form=form)                
                
                if not validar_monto(form, tarjeta):
                    form.monto.data = 0.0
                    print(form.monto.data)
                    flash('El monto ingresado supera el saldo de la tarjeta.', 'error')
                    return render_template('/general/donar_con_tarjeta.html', form=form)
                
                if not validar_tipo(form, tarjeta):
                    flash('El tipo de tarjeta no coincide.', 'error')
                    return render_template('/general/donar_con_tarjeta.html', form=form)
                
                if not validar_fecha_expiracion(form, tarjeta):
                    form.fecha_expiracion.data = ''
                    flash('La fecha de expiración no coincide.', 'error')
                    return render_template('/general/donar_con_tarjeta.html', form=form)
                
                if not validar_codigo_seguridad(form, tarjeta):
                    form.codigo_seguridad.data = ''
                    flash('El código de seguridad no coincide.', 'error')
                    return render_template('/general/donar_con_tarjeta.html', form=form)                
                
                if tarjeta.titular != form.nombre_titular.data:
                    form.nombre_titular.data = ''
                    flash('El nombre del titular no coincide.', 'error')
                    return render_template('/general/donar_con_tarjeta.html', form=form)
                
                monto = form.monto.data        
                tarjeta.saldo -= float(monto)
                id_tipo = Tipo.query.filter_by(nombre="Tarjeta").first()
                email = usuario.email
                nombre = usuario.nombre
                apellido = usuario.apellido
                telefono = usuario.telefono
                fecha_donacion = datetime.now()
                descripcion = fecha_donacion.strftime("%Y%m%d%H%M%S")        
                id_categoria = 10            
                nueva_donacion = Donacion(id_tipo=id_tipo.id, email=email, nombre=nombre, apellido=apellido, telefono=telefono, descripcion=descripcion, monto=monto, id_categoria=id_categoria, fecha_donacion=fecha_donacion )
                db.session.add(nueva_donacion)
                db.session.commit()            
                Notificacion.donacionTarjeta(nueva_donacion.id)
                flash('Donación realizada con éxito.', 'success')                
                return redirect(url_for('donar_con_tarjeta.donar_con_tarjeta'))
    except Exception as e:
        print(e)
        flash('Error al realizar la donación.', 'error')
        return redirect(url_for('donar_con_tarjeta.donar_con_tarjeta'))    
    return render_template('/general/donar_con_tarjeta.html', form=form)