
from flask import render_template, session, redirect, url_for, request
from flask_login import login_required, current_user
from ..models import User, List

from . import home

@home.route('/')
def homepage():
    """
    Render the homepage template on / route
    """
    
    if not current_user.is_authenticated:
        print('IP adresa')
        print(request.environ['REMOTE_ADDR'])
        return render_template('home/index.html', title = 'Welcome')
    elif current_user.is_authenticated and current_user.is_admin is False:
        print('IP adresa')
        print(request.environ['REMOTE_ADDR'])
        print(request.remote_addr)
        lists = List.query.filter_by(user_id=current_user.id)
        return render_template('home/dashboard.html', lists = lists, Title='Dashboard')
    elif current_user.is_admin is True and current_user.is_authenticated:
        print('IP adresa')
        print(request.environ['REMOTE_ADDR'])
        return redirect(url_for('admin.adminHome'))
    
    
        
        

