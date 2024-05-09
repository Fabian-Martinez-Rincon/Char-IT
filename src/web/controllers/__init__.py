import flask
from src.web.controllers import root, registrar, registrarColaborador, editarPubli, eliminarPubli, cambiarVisibilidad

_blueprints = (
    root.bp, registrar.bp, registrarColaborador.bp, editarPubli.bp, eliminarPubli.bp, cambiarVisibilidad.bp,
)

def init_app(app: flask.Flask):
    """Initializes the controllers.
    Registers the blueprints and error handlers for the application.
    Also registers the before request hook for the application.
    """

    for bp in _blueprints:
        app.register_blueprint(bp)


