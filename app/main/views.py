from datetime import datetime
from flask import render_template,session,redirect,url_for,flash,abort
from flask_login.utils import login_required,current_user
from wtforms import fields
from . import main
from .forms import EditProfileAdminForm, IndexForm,ShopForm,EditProfileForm
from .. import db
from ..model import Itemname, Permission,Price,Shop,User,Role
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

@main.route('/user/<username>')
def user(username):
    user=User.query.filter_by(username=username).first_or_404()
    return render_template('user.html',user=user)



@main.route('/', methods=['GET', 'POST'])
def index():
    # name = None
    form = IndexForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            print(session)
            session['known']=False
        else:
            print(session)
            session['known']=True
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('main.index'))
        # name = form.name.data
        # form.name.data = ''
    return render_template('index.html', form=form, name=session.get('name'),known=session.get('known',False))

@main.route('/shopcrub', methods=['GET', 'POST'])
def shopcrub():
    # name = None
    # db.session.rollback()
    db.create_all()
    form = ShopForm()
    itemnm=form.name.data
    product=[]
    if form.validate_on_submit():
        work(itemnm)
        # item=db.engine.execute(f"select * from mainlist where mainlist.name like '%%{itemnm}%%'").fetchall()
        item=Itemname.query.join(Price).filter(
                                    Price.maxprice < int(form.maxprice.data),
                                    Price.minprice > int(form.minprice.data),
                                    and_(Itemname.itemname.like(f"%{itemnm}%"),
                                    Itemname.shopid.in_(form.shop.data))).all()
        # print(item)
        if item is None:           
            # print(item)
            session['known']=False
        else:
            session['known']=True
        session['name']=form.name.data
        form.name.data=''

        for i in item:
            product.append({
                "item":i.itemname,
                "minprice":i.price.minprice,
                "maxprice":i.price.maxprice,
                "shop":i.shopname.shop,
                "iurl":i.imageurl,
                "url":i.itemurl})

        # print(pd.DataFrame(product))
        # itemtable=pd.DataFrame(product).to_html()
    else:
        itemtable="抱歉，查無此商品"
        # print(itemtable)
    #     return redirect(url_for('index'))
    #     # name = form.name.data
    #     # form.name.data = ''
    return render_template('shopcrub.html', form=form,itemtable=product, name=session.get('name'),known=session.get('known',False))

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