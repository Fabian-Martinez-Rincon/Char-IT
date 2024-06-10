from flask import render_template, Blueprint, session, flash, redirect, url_for
from datetime import date
from src.core.models.oferta import Oferta
from src.core.models.estado import Estado
from src.core.models.publicacion import Publicacion
from src.core.models.usuario import Usuario
from src.core.models.notificacion import Notificacion
from src.core.models.oferta_detalle import OfertaDetalle
from src.core.models.filial import Filial
bp = Blueprint("pendientes", __name__)

@bp.route("/pendientes", methods=['GET'])
def pendientes():
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    # Verifica si el usuario actual es el propietario de la publicación
    if session.get('user_id'):
        rol = Usuario.query.get(session.get('user_id')).id_rol
        if rol == 1 :  
                    flash('No tienes permiso para realizar esta operacion.', 'error')
                    return redirect(url_for('root.index_get'))
    hoy = date.today()
    
    estado_aceptada_id = Estado.query.filter_by(nombre="aceptada").first()  # Suponiendo que el estado "aceptada" 
    
    ofertas_anteriores = Oferta.query.join(Estado, Estado.id == Oferta.estado).filter(
        Oferta.fechaIntercambio < hoy,        
        ((Estado.nombre == "pendiente")) | ((Estado.nombre == "aceptada"))
    ).all() 
    
    cancelada = Estado.query.filter_by(nombre="cancelada").first()
    # Cambiar el estado de todas las ofertas anteriores a "cancelada"
    for oferta in ofertas_anteriores:
        oferta.estado = cancelada.id
        oferta.publicacion_ofrecido.id_visibilidad = 2
        oferta.publicacion_solicitado.id_visibilidad = 2
        oferta.descripcion = "Cancelada por el sistema - Oferta no aceptada en el tiempo establecido."
        Notificacion.cancelarOfertaAceptada(oferta.id)
    
    ofertas = Oferta.query.join(Estado, Estado.id == Oferta.estado).filter(
        Oferta.fechaIntercambio == hoy,
        Estado.id == estado_aceptada_id.id,         
    ).order_by(Oferta.horaIntercambio.asc()).all()

    intercambios_realizados = []
    for intercambio in ofertas:
        ofrecido = Publicacion.query.get(intercambio.ofrecido)
        solicitado = Publicacion.query.get(intercambio.solicitado)            
        solicitado_email = Usuario.query.get(solicitado.id_usuario).email            
        ofrecido_email = Usuario.query.get(ofrecido.id_usuario).email
        filial = Filial.query.get(intercambio.filial).nombre
        estado = Estado.query.get(intercambio.estado).nombre
        intercambio_detalle = OfertaDetalle(
            oferta_id=intercambio.id,
            ofrecido=ofrecido,
            solicitado=solicitado,
            fecha=intercambio.fechaIntercambio,
            hora=intercambio.horaIntercambio,
            filial=filial,
            estado=estado, 
            descripcion=intercambio.descripcion, 
            solicitado_email=solicitado_email,
            ofrecido_email=ofrecido_email
        )
        intercambios_realizados.append(intercambio_detalle)
    return render_template("owner/pendientes.html", ofertas=intercambios_realizados)        