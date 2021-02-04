#app/auth/views.py

from flask import flash, render_template, redirect, url_for, request, session, make_response, current_app
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime


from . import auth
from .forms import LoginForm, RegistrationForm, LoginForm, TaskForm
# from ..models import db
from ..models import User, List, Task
from app.utils import send_mail
from app import db



# @auth.errorhandler(404)
# def not_found_error(error):
#     return render_template('auth/404.html'), 404

# @auth.errorhandler(500)
# def not_found_error(error):
#     return render_template('auth/404.html'), 500


@auth.before_request
def before():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add a user to the database through the registration form
    """
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=form.password.data)
        email=form.email.data,
        name=form.username.data,
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        password=form.password.data
        db.session.add(user)
        db.session.commit()
        send_mail("Welcome new user", form.email.data,'auth/newuser.html', name=name[0], email=email[0])
        flash('You have succesfully registered! You may now login')

        return redirect(url_for('auth.login'))
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    return render_template('auth/register.html', form = form, title = 'Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data, is_admin = False).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)

            return redirect(url_for('home.homepage'))
        else:
            flash('Invalid email or password.')
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    return render_template('auth/login.html', form = form, title = 'Register')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have been successfully logged out.')

    return redirect(url_for('auth.login'))



@auth.route('/addlist', methods=['POST'])
@login_required
def addlist():

    """Add list to database
    """

    list = List(
            name = request.form['listName'],
            user_id = current_user.id
    )
    db.session.add(list)
    db.session.commit()
    
    return redirect(url_for('home.homepage'))

@auth.route('/list/<int:id>', methods=['GET', 'POST'])
@login_required
def showTasks(id):
    form = TaskForm()
    tasks = Task.query.filter(Task.list_id==id)
    if form.validate_on_submit(): 
        task = Task(
            name = form.name.data,
            end_date = form.end_date.data,
            list_id = id
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('auth.showTasks', id=id))
    return render_template('auth/tasks.html', form = form, tasks = tasks, Title = 'Tasks')

@auth.route('/list/delete/<int:id>')
@login_required
def deletelist(id):
    list = List.__table__.delete().where(List.id == id)
    task = Task.__table__.delete().where(Task.list_id == id)
    db.engine.execute(task)
    db.engine.execute(list)
    
    return redirect(url_for('home.homepage'))


@auth.route('/list/task/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_task(id):
    form = TaskForm()
    if request.method=='POST':
    
        name = request.form['taskname']
        enddate = request.form['enddate']
        task = Task.__table__.update().\
            values({'name':name, 'end_date': enddate}).where(Task.id == id)
        db.engine.execute(task)
        tasks = Task.query.filter(Task.id==id).first()
        return redirect(url_for('auth.showTasks', id = tasks.list_id))
    else:
        task = Task.query.filter(Task.id==id).first()
        return render_template('auth/edit_task.html', task = task)

@auth.route('/list/<int:list_id>/delete/task/<int:id>')
@login_required
def delete_task(list_id, id):
    task = Task.__table__.delete().where(Task.id == id)
    db.engine.execute(task)
    return redirect(url_for('auth.showTasks', id = list_id))

@auth.route('/list/<int:list_id>/update/task/<int:id>')
@login_required
def update_task(list_id, id):
    taskC = Task.query.filter(Task.id==id).first()
    
    if taskC.completed:
        task = Task.__table__.update().\
            values({'completed':0}).where(Task.id == id)
        db.engine.execute(task)
    else:
        task = Task.__table__.update().\
            values({'completed':1}).where(Task.id == id)
        db.engine.execute(task)
    return redirect(url_for('auth.showTasks', id = list_id))


@auth.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(id = current_user.id).first()
    return render_template('auth/profile.html', firstName = user.first_name, lastName = user.last_name, email = user.email, username = user.username)

@auth.route('/changepassword', methods=['POST'])
@login_required
def changepassord():
    oldpass = request.form['oldpassword']
    newpass = request.form['newpassword']
    repeatpass = request.form['repeatpassword']
    pass_hash = generate_password_hash(newpass)
    user = User.query.filter_by(id = session['_user_id']).first()
    if user.verify_password(oldpass):
        if newpass == repeatpass:
            user = User.__table__.update().values({'password_hash': pass_hash}).where(User.id==session['_user_id'])
            db.engine.execute(user)
            return redirect(url_for('auth.logout'))





