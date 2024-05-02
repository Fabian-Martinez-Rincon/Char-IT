from flask import Flask
from src.core import config
from src.web import controllers

def create_app(env: str = "development", static_folder: str = "../static"):
    app = Flask(
        __name__, static_folder=static_folder, template_folder="./templates"
    )

    config.init_app(app, env)
    controllers.init_app(app)
    return app