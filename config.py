#config.py
import os

class Config(object):
    """
    Common Configuration
    """
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'jasko.alimanovic@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'PI3141592'
    ADMINS = ['jasko.alimanovic@gmail.com']
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    FLASK_DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    FLASK_DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}