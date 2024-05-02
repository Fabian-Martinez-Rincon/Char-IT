import os
import typing as t
from dotenv import load_dotenv
from flask import Flask

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

    @classmethod
    def load_env_config(cls) -> None:
        cls.LIVETW_DEV = env_or_error("LIVETW_ENV", "production").lower() == "development"



def init_app(app: Flask, env: str) -> None:
    """Initializes the application configuration.

    Loads the environment variables from the .env file if the application
    is running in development mode, otherwise loads the environment variables
    from the database.
    """
    if env == "development":
        load_dotenv()
    # else:
    #     load_db_dotenv()

    Config.load_env_config()

    app.config.from_object(Config)