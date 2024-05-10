import os
import typing as t
from dotenv import load_dotenv


class ConfigurationError(Exception):
    """Error raised when a configuration error occurs.

    Attributes:
        message: A human-readable message describing the error.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

def env_or_error(env: str, default: t.Union[str, None] = None) -> str:
    value = os.getenv(env, default)
    if value is None:
        raise ConfigurationError(f"Environment variable '{env}' not set")
    return value

class Config:
    # Flask-livetw config
    LIVETW_DEV: bool
    TESTING = False
    #Configurar la carga de imagenes
    UPLOAD_FOLDER = 'Char-IT/static/'
    ALLOWED_EXTENSIONS = {'png', 'jpg'}
    # Configurar la extensión Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'hopeTrade08@gmail.com'
    MAIL_PASSWORD = 'hgju fnoc xpfg rrwp'  # para ingresar a GMAIL: 08_hopeTrade
    MAIL_DEFAULT_SENDER = 'hopeTrade08@gmail.com'
    
    @classmethod
    def load_env_config(cls) -> None:
        cls.LIVETW_DEV = env_or_error("LIVETW_ENV", "production").lower() == "development"

class ProductionConfig(Config):
    """Production configuration"""

class DevelopmentConfig(Config):
    """Development configuration"""
    DB_USER = "postgres"
    load_dotenv()
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = "localhost" 
    DB_NAME = "grupo08"
    SQLALCHEMY_TRACK_NOTIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    LIVETW_DEV=True
    

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True

config = {"production": ProductionConfig,"development": DevelopmentConfig,"testing": TestingConfig}
#This is a dictionary used to properly return the configuration selected when the app was created

"""def init_app(app: Flask, env: str) -> None:
    Initializes the application configuration.

    Loads the environment variables from the .env file if the application
    is running in development mode, otherwise loads the environment variables
    from the database.
    
    if env == "development":
        load_dotenv()
        app.config.from_object(DevelopmentConfig)
    elif env == "testing":
        app.config.from_object(TestingConfig)
    else:
        raise ConfigurationError(f"Unknown environment '{env}'")
    
    Config.load_env_config()
    app.config.from_object(Config)
    
    from src.core.models.database import init_app as init_db_app
    init_db_app(app)
 """