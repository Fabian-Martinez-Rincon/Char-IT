from flask import (
    Blueprint,
    render_template
)


bp = Blueprint("root", __name__)

@bp.get("/")
def index_get():
    return render_template("index.html")
