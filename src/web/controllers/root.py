from flask import Blueprint, render_template
from src.core.models.database import db  # Asegúrate de que esta ruta de importación sea correcta
from src.core.models.filial import Filial  # Importa el modelo Filial


from flask import (
    Blueprint,
    render_template
)


bp = Blueprint("root", __name__)

@bp.get("/")
def index_get():
    try:
        todas_las_filiales = Filial.query.all()  # Obtener todas las filiales
        return render_template("index.html", filiales=todas_las_filiales)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


