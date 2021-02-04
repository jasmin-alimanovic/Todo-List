
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email




class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
