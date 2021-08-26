from os import error
from flask import render_template,redirect,request,url_for,flash,abort
from flask_login import login_user,logout_user,login_required
from ..model import User
from .form import LoginForm,RegistionForm,ChangePasswordForm,PasswordResetRequestForm,PasswordResetForm
from . import auth
from .. import db
from ..email import send_email
from flask_login import current_user
from flask import current_app
import string
import random


@auth.route('/login',methods=['GET','POST'])
def login():
    print(current_app.config['FLASKY_ADMIN'])
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            next=request.args.get('next')
            if next is None or not next.startswith('/'):
                next=url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')

    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logout')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['POST','GET'])
def register():
    form=RegistionForm()
    if form.validate_on_submit():
        user=User(  email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token=user.generate_confirmation_token()     #生成確認權杖
        send_email(user.email,'Confirm Your Account','auth/email/confirm',user=user,token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.route('confirm/<token>')
@login_required #要求登入後才能造訪
def confirm(token):
    if current_user.confirmed:                              #已認證過的帳號會直接跳轉至首頁
        return redirect(url_for('main.index'))
    if current_user.confirm(token):                         #未認證過的帳號且收到確認權杖
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:                                                   #未認證過的帳號且未收到確認權杖
        flash('The confirmed is invalid or has expired')
    return redirect(url_for('main.index'))
    
@auth.before_app_request
def before_request():
    #在使用者對網站發出請求前的動作
    if current_user.is_authenticated :
        current_user.ping()
        if not current_user.confirmed \
        and request.blueprint != 'auth' \
        and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirm.html')

@auth.route("/confirm")
@login_required
def resend_confirmation():
    token=current_user.generate_confirmation_token()
    send_email(current_user.email,'Confirm Your Account','auth/email/confirm',
                user=current_user,token=token)
    flash('A new confirmation email has been sent to you by email')
    return redirect(url_for('main.index'))


@auth.route('/change_password',methods=['GET','POST'])
@login_required
def change_password():
    form=ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            if not current_user.verify_password(form.new_password.data):
                current_user.password=form.new_password.data
                db.session.add(current_user._get_current_object())
                db.session.commit()
                flash("Password has been change")
                return redirect(url_for("main.index"))
            flash("Password must be different from origin")
            return redirect(url_for(f".change_password"))
        flash("The old password was entered incorrectly")
        return redirect(url_for(f".change_password"))  
    return render_template('auth/change_password.html',form=form)      

@auth.route('/reset',methods=['GET','POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token)
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)