# app/__init__.py

# third-party imports
from flask import Flask, render_template, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_mail import Mail, Message
from threading import Thread
# from flask_mail import Mail, Message

# local imports

from config import app_config

# db variable initialization
db = SQLAlchemy()
# login manager
login_manager = LoginManager()
# mail
mail = Mail()

#function to send email to admin
def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, recipient, template, **kwargs):
    msg = Message(subject, sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[recipient])
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=async_send_mail, args=[current_app._get_current_object(), msg])
    thr.start()
    return thr


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    mail.init_app(app)
    migrate = Migrate()
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to acces this page"
    login_manager.login_view = "auth.login"
    migrate.init_app(app, db)
    Bootstrap(app)
    

    from app import models
    
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    @app.errorhandler(404)
    def err_404(er):
        if not app.debug:
            send_mail("ERROR 404", app.config['MAIL_DEFAULT_SENDER'],'errors/404.html')
        return render_template("errors/404.html"), 404
        

    return app