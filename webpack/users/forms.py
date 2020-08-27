from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField,StringField,PasswordField,BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from webpack.models import User
from flask_login import current_user

class Registration_Form(FlaskForm):

    username = StringField('Username',validators = [DataRequired(),Length(min = 3 , max = 20,message="Length should be between 3 to 20")])
    email = StringField('Email', validators = [DataRequired(), Email()])
    # password = PasswordField('Password',validators = [DataRequired()])
    # confirm_password = PasswordField('Password',validators = [DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')
    checkbox = BooleanField('checkbox',validators=[DataRequired()])

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username Already Exists')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email Already Exists')

class Login_form(FlaskForm):

    email = StringField('Username/Email', validators = [DataRequired()])
    password = PasswordField('Password',validators = [DataRequired()])
    submit = SubmitField('Login')
    checkbox = BooleanField('checkbox')

class Update_Form(FlaskForm):
    first_name = StringField('First',validators = [DataRequired()])
    last_name = StringField('Last',validators = [DataRequired()])
    country = StringField('Country',validators = [DataRequired()])
    skills = StringField('Skills',validators = [DataRequired()])
    username = StringField('Username',validators = [DataRequired(),Length(min = 3 , max = 20,message="Length should be between 3 to 20")])
    email = StringField('Email', validators = [DataRequired(), Email()])
    profile_pic = FileField('Update Profile Picture' , validators= [FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Username Already Exists')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Email Already Exists')


class Request_reset_form(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    submit = SubmitField('Request Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if not user:
            raise ValidationError('No such email address exists. Please Register .')

class Change_password(FlaskForm):
    password = PasswordField('Password',validators = [DataRequired()])
    confirm_password = PasswordField('Password',validators = [DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')

class Chatting(FlaskForm):
    message = StringField('Type here ...',validators = [DataRequired()])
    submit = SubmitField('Send')