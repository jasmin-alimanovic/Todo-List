#app/admin/views.py


from flask import redirect, request, render_template, url_for, session, flash, jsonify, abort
from flask_login import login_required, login_user, logout_user, current_user, UserMixin
from datetime import datetime
from sqlalchemy import func, text

from . import admin
from ..models import db, User, List, Task
from .forms import LoginForm



@admin.errorhandler(404)
def not_found_error(error):
    return render_template('auth/404.html'), 404


@admin.before_request
def before():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow( )
        db.session.commit()

@admin.route('/', methods=['GET'])
@login_required
def adminHome():
    """Handle the admin index page
    """
    if current_user.is_admin == True:

        return render_template('admin/index.html', Title = 'Admin')
    else:
        abort(403)
@admin.route('/login', methods=['GET', 'POST'])
def login():
    """Handle request to admin login page
    Log in an admin in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user is not None and user.verify_password(form.password.data) and user.is_admin:
            login_user(user)
            return redirect(url_for('admin.adminHome'))
        else:
            flash('Incorrect email or password')
    if current_user.is_authenticated and not current_user.is_admin:
        return redirect(url_for('home.homepage'))
    return render_template('admin/login.html', form = form)

@admin.route('/logout')
@login_required
def logout():
    """Handle the request to the /admin/logout page
    Log the admin out through the logout link
    """
    logout_user()
    flash('You are successfully logged out.')
    return redirect(url_for('admin.login'))

@admin.route('/profile')
@login_required
def profile():
    """
    Handle the request to admin profile page
    """
    user = User.query.filter_by(id = session['_user_id']).first()
    return render_template('admin/profile.html', firstName = user.first_name, lastName = user.last_name, email = user.email, username = user.username)


@admin.route('/users')
@login_required
def total_users():
    """
    Handle the request to /users route, display all registered users
    """
    if current_user.is_admin is True:
        users = User.query.order_by(User.id.desc()).all()
        duzina = len(users)
        return render_template('admin/total_users.html', users = users, duzina=duzina)
    else:
        abort(500)


@admin.route('/users/<username>')
@login_required
def user(username):
    """
    Handle the request to /users/<username> route, display all info except password of selected user
    """
    if current_user.is_admin is True:
        user = User.query.filter_by(username=username).first()
        return render_template('admin/user.html', user = user)
    else:
        abort(403)

@admin.route('/users/delete/user/<int:id>')
def deleteuser(id):
    print('LISTS ')
    user = User.query.filter_by(id=id).first()
    lists = List.query.filter(List.user_id==id)
    # tasks = List.query.filter(Task.list_id == User.lists.id)
    print('LISTS ')
    for list in lists:
        print(Task.query.filter(Task.list_id == list.id))
    return redirect(url_for('admin.user', username=user.username))

@admin.route('/usersinlast24h')
def users_24h():
    users = []
    d = datetime(2020,12,11)
    users = User.query.filter(func.datediff(datetime.utcnow(), User.date_created)<=1)
    duzina = 1
    return render_template('admin/total_users.html', users = users, duzina=duzina)

@admin.route('/listscreated')
def listscreated():
    lists = List.query.order_by(List.id.desc()).all() 
    duzina = len(lists)
    return render_template('admin/total_lists.html', lists=lists, duzina = duzina, Title = 'Lists')


@admin.route('/list/<int:id>/tasks')
def list_tasks(id):
    tasks = Task.query.filter_by(list_id = id)
    prazna = False
    if tasks is None:
        prazna = True
    return render_template('admin/tasks.html', Title='Tasks', tasks = tasks, prazna = prazna)

@admin.route('/api/users', methods=['GET'])
def fetch():
    users = []
    user = {}
    db_users = User.query.order_by(User.id.desc()).all()
    for db_user in db_users:
        user={}
        user['user_id'] = db_user.id
        user['username'] = db_user.username
        user['first_name'] = db_user.first_name
        user['last_name'] = db_user.last_name
        user['email'] = db_user.email
        user['date_created'] = db_user.date_created
        user['last_seen'] = db_user.last_seen
        users.append(user)

    return jsonify(users)