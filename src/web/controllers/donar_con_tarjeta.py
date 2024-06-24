import os
from src.core.models.notificacion import Notificacion
from src.core.models.donacion import Donacion
from src.core.models.tipo import Tipo
from src.core.models.usuario import Usuario
from flask import render_template, request, flash, redirect, url_for, session, current_app
from src.web.formularios.donar_con_tarjeta import DonarConTarjeta
from src.core.models.oferta import Oferta
from src.core.models.publicacion import Publicacion
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
    form = DonarConTarjeta()
    print(form.validate_on_submit())
    if form.validate_on_submit():        
        id_tipo = Tipo.query.filter_by(nombre="Tarjeta").first()
        monto = form.monto.data
        print(monto)
        email = form.email.data
        fecha_donacion = datetime.now()
        telefono = form.telefono.data
        descripcion = fecha_donacion.strftime("%Y%m%d%H%M%S")
        nueva_donacion = Donacion(id_tipo=id_tipo.id, email=email, monto=monto, fecha_donacion=fecha_donacion, telefono=telefono, descripcion=descripcion )

        db.session.add(nueva_donacion)
        db.session.commit()

        flash('Donación realizada con éxito.', 'success')
        return redirect(url_for('root.index_get'))

    return render_template('/general/donar_con_tarjeta.html', form=form)