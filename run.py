#run.py

import os
from flask import render_template, url_for
import logging



from app import create_app
from app.models import User, Task,List,db
from config import Config


config_name = os.getenv('FLASK_ENV') or production
app = create_app(config_name)




@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'List': List, 'Task': Task}

admins = ("jasko.alimanovic@gmail.com")

if __name__ == '__main__':
    app.run()
