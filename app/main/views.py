from datetime import datetime
from os import error
from flask import render_template,session,redirect,url_for,flash,abort,request,current_app
from flask_login.utils import login_required,current_user
from werkzeug.datastructures import RequestCacheControl
from wtforms import fields
from . import main
from .forms import EditProfileAdminForm, IndexForm,ShopForm,EditProfileForm,PostForm
from .. import db
from ..model import Itemname, Permission, Post,Price,Shop,User,Role
from ..crub.main import work
import pandas as pd
from sqlalchemy import and_
from  ..decorators import admin_required,permission_required

@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return 'For administrator'

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderate_only():
    return 'For comment Moderates'

@main.route('/', methods=['GET', 'POST'])
def index():
    # name = None
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post=Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for(".index"))
    posts=Post.query.order_by(Post.timestamp.desc()).all()
    page=request.args.get('page',1,type=int)#取得當前頁數
    pagination=Post.query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False
    )#將結果轉換成頁數
    posts=pagination.items#取出頁數裡的物件(文章)
    return render_template('index.html',form=form,posts=posts,pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)

@main.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user=User.query.get_or_404(id)
    form=EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email=form.email.data
        user.username=form.username.data
        user.confirmed=form.confirmed.data
        user.role=Role.query.get(form.role.data)
        user.username=form.name.data
        user.location=form.location.data
        user.about_me=form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been update')
        return redirect(url_for('.user',username=user.username))
    form.email.data=user.email
    form.username.data=user.username
    form.confirmed.data=user.confirmed
    form.name.data=user.username
    form.role.data=user.role
    form.location.data=user.location
    form.about_me.data=user.about_me
    return render_template('edit_profile.html',form=form,user=user)

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form=EditProfileForm()
    if form.validate_on_submit():
        current_user.username=form.name.data
        current_user.location=form.location.data
        current_user.about_me=form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been update')
        return redirect(url_for('.user',username=current_user.username))
    form.name.data=current_user.username
    form.location.data=current_user.location
    form.about_me.data=current_user.about_me
    return render_template('edit_profile.html',form=form)

@main.route('/edit-users',methods=['GET','POST'])
@login_required
@admin_required
def edit_users_admin():
    users=User.query.all()
    return render_template("edit_users.html",users=users)

@main.route('/delete-users/<int:username>',methods=['DELETE'])
@login_required
@admin_required
def delete_users_admin(username):
    user=User.query.filter_by(name=username)
    db.session.delete(user)
    db.session.commit()
    return render_template("edit_users.html",users=user)