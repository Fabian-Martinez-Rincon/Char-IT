from flask import Flask
from src.core.config import config
from src.core.models import database
from src.web import controllers

def create_app(env: str = "development", static_folder: str = "../static"):
    app = Flask(
        __name__, static_folder=static_folder, template_folder="./templates"
    )
    app.config.from_object(config[env])
    
    database.init_app(app)
    controllers.init_app(app)
    @app.cli.command(name="resetdb")
    def resetdb():
        with app.app_context():
         database.reset_db()
    
    return app