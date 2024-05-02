#ACA SE REALIZA LA CONEXION CON LA BASE DE DATOS
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    """This is the initiation of the app"""
    with app.app_context():
        db.init_app(app)
        config_db()

def config_db():
    """This configures the DB to close the session when a request finishes"""
    @current_app.teardown_request
    def close_session(exception=None):
        db.session.close()
        
def reset_db():
    """This function deletes and recreates the DB to update the models' definitions"""
    with current_app.app_context():
        db.drop_all()
        print("parece que anda")
        db.create_all()
