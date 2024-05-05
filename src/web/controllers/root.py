from flask import Blueprint, render_template
from src.core.models.filial import Filial  # Importa el modelo Filial
from src.core.models.usuario import Usuario
from src.core.models.publicacion import Publicacion

from flask import (
    Blueprint,
    render_template
)

bp = Blueprint("root", __name__)

@bp.get("/")
def index_get():
    try:
        todas_las_filiales = Filial.query.all()
        return render_template("index.html", filiales=todas_las_filiales)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@bp.get("/generales")
def usuarios_generales_get():
    try:
        usuarios_rol_2 = Usuario.query.filter(Usuario.id_rol == 2).all()
        return render_template("/owner/usuarios.html", usuarios=usuarios_rol_2)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@bp.get("/colaboradores")
def usuarios_colaboradores_get():
    try:
        usuarios_rol_3 = Usuario.query.filter(Usuario.id_rol == 3).all()
        return render_template("/owner/usuarios.html", usuarios=usuarios_rol_3)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@bp.get("/publicaciones")
def publicaciones_get():
    try:
        todas_las_publicaciones = Publicacion.query.all()
        return render_template("/owner/publicaciones.html", publicaciones=todas_las_publicaciones)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
