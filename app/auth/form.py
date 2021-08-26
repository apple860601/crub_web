from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..model import User

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember_me=BooleanField('keep me logged in')
    submit=SubmitField('Log In')

class RegistionForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    username = StringField('Username',validators=[DataRequired(),Length(1,64),
    Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters,numbers,dots or underscores')])
    password=PasswordField('Password',validators=[DataRequired(),
                            EqualTo('password2',message='Passwords must match.')])
    password2=PasswordField('Confirm password',validators=[DataRequired()])
    submit=SubmitField('註冊')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registersd.')
    
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class ChangePasswordForm(FlaskForm):
    old_password=PasswordField('Old Password',validators=[DataRequired()])
    new_password=PasswordField('New Password',validators=[DataRequired(),
                            EqualTo('confirm_password',message='Passwords must match.')])
    confirm_password=PasswordField('Confirm password',validators=[DataRequired()])
    submit=SubmitField('儲存')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')

class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')