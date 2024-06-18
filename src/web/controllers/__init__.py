import flask
from src.web.controllers import root, registrar, registrar_colaborador, editar_publi, cambiar_visibilidad, editar_perfil, eliminar_publi, subir_publi, pendientes, ofertar_publi, rechazarOferta, confirmar_intercambio, cancelar_intercambio, aceptarOferta, eliminar_colaborador, usuario_operaciones, todas_donaciones, mis_donaciones, registrar_donacion

_blueprints = (
    root.bp, registrar.bp, registrar_colaborador.bp, editar_publi.bp, eliminar_publi.bp, cambiar_visibilidad.bp, subir_publi.bp, editar_perfil.bp, pendientes.bp, ofertar_publi.bp, rechazarOferta.bp, confirmar_intercambio.bp, cancelar_intercambio.bp, aceptarOferta.bp, eliminar_colaborador.bp, usuario_operaciones.bp, todas_donaciones.bp, mis_donaciones.bp, registrar_donacion.bp
)

def init_app(app: flask.Flask):
    """Initializes the controllers.
    Registers the blueprints and error handlers for the application.
    Also registers the before request hook for the application.
    """

    for bp in _blueprints:
        app.register_blueprint(bp)
