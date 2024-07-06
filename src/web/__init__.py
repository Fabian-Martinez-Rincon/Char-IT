from flask import Flask, session, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from src.core.config import config
from src.core.models import database, Usuario
from src.web import controllers
from datetime import timedelta
import os

def create_app(env: str = "development", static_folder: str = "../static"):
    app = Flask(
        __name__, static_folder=static_folder, template_folder="./templates"
    )
    app.config.from_object(config[env])
    app.config['SECRET_KEY'] = 'e8771dffd56434456199d5087a3ea4d4'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = True  # Si estás usando HTTPS
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "src", "static").replace(os.sep, "/") # Ruta de la carpeta para las imagenes

    database.init_app(app)
    controllers.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "root.index_get"  # Asegúrate de tener una ruta de inicio de sesión

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    @app.before_request
    def check_if_user_is_active():
        if current_user.is_authenticated:
            user = Usuario.query.get(current_user.id)
            if user and user.penaltis >= 3:
                logout_user()                
                session['logged_in'] = False
                flash('Tu cuenta ha sido eliminada.', 'error')
                return redirect(url_for('root.index_get'))  # Redirige al usuario a la página de inicio de sesión

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
