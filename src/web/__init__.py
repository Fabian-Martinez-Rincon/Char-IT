from flask import Flask
from src.core.config import config
from src.core.models import database
from src.web import controllers
from datetime import timedelta

def create_app(env: str = "development", static_folder: str = "../static"):
    app = Flask(
        __name__, static_folder=static_folder, template_folder="./templates"
    )
    app.config.from_object(config[env])
    app.config['SECRET_KEY'] = 'e8771dffd56434456199d5087a3ea4d4'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = True  # Si estás usando HTTPS
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14) 
    database.init_app(app)
    controllers.init_app(app)
    
    @app.cli.command(name="resetdb")
    def resetdb():
        with app.app_context():
         database.reset_db()
    
    from src.core import seed
    @app.cli.command(name="seeddb")
    def seed_db():
        with app.app_context():
            database.reset_db()
            seed.seed_db()
            print("Database seeded successfully.")
            
    return app