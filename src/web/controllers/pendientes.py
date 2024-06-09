from flask import render_template, Blueprint, session, flash, redirect, url_for
from datetime import date
from src.core.models.oferta import Oferta
from src.core.models.estado import Estado
from src.core.models.publicacion import Publicacion
from src.core.models.usuario import Usuario
from src.core.models.notificacion import Notificacion
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
    return render_template("owner/pendientes.html", ofertas=ofertas, estado=estado_aceptada_id.nombre )


# <div>

#         <form method="POST" action="{{ url_for('confirmarIntercambio.cancelarIntercambio', oferta_id=id) }}">
#             <button class="px-6 py-2 my-4 text-white transition duration-300 rounded bg-cyan-shade hover:bg-green-cyan-shade">
#                 Cancelar
#             </button>                            
#         </form>
#     </div>

        