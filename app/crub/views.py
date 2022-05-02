from datetime import datetime
from os import error
from flask import render_template,session,redirect,url_for,flash,abort,request,current_app
from flask_login.utils import login_required,current_user
from werkzeug.datastructures import RequestCacheControl
from wtforms import fields
from . import crub
from .. import db
from ..model import Itemname, Permission, Post,Price,Shop,User,Role
from .main import work
import pandas as pd
from sqlalchemy import and_
from  ..decorators import admin_required,permission_required
from .forms import ShopForm,TraceForm

@crub.route('/', methods=['GET', 'POST'])
@login_required
def shopcrub():
    # name = None
    # db.session.rollback()
    db.create_all()
    form = ShopForm()
    trace = TraceForm()
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
                "id":i.itemid,
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

    return render_template('shopcrub.html', form=form,trace=trace,itemtable=product, 
    name=session.get('name'),known=session.get('known',False))

@crub.route('/trace/<product>', methods=['GET', 'POST'])
@login_required
def trace(product):
    product=Itemname.query.filter_by(itemid=product).first()
    if product is None:
        flash('Invalid product')
        return redirect(url_for('.shopcrub'))
    if current_user.is_tracing(product):
        flash('You have already trace this item')
        return redirect(url_for('.shopcrub'))
    current_user.trace(product)
    db.session.commit()
    flash("trace successful")
    return redirect(url_for('.shopcrub'))

@crub.route('/untrace/<product>', methods=['GET', 'POST'])
@login_required
def untrace(product):
    product=Itemname.query.filter_by(itemid=product).first()
    if product is None:
        flash('Invalid product')
        return redirect(url_for('.shopcrub'))
    if not current_user.is_tracing(product):
        flash('You have not trace this item yet')
        return redirect(url_for('.shopcrub'))
    current_user.untrace(product)
    db.session.commit()
    flash("untrace successful")
    return redirect(url_for('.shopcrub'))