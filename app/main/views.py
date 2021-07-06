from datetime import datetime
from flask import render_template,session,redirect,url_for
from . import main
from .forms import NameForm
from .. import db
from ..model import Itemname,Price,Shop,User,Role
from ..crub.main import work
import pandas as pd

@main.route('/', methods=['GET', 'POST'])
def index():
    # name = None
    form = NameForm()
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
    form = NameForm()
    itemnm=form.name.data
    product=[]
    if form.validate_on_submit():
        work(itemnm)
        # item=db.engine.execute(f"select * from mainlist where mainlist.name like '%%{itemnm}%%'").fetchall()
        item=Itemname.query.filter(Itemname.itemname.like(f"%{itemnm}%")).all()
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
                "iurl":i.shopname.IURLform+i.imageurl})

        # print(pd.DataFrame(product))
        # itemtable=pd.DataFrame(product).to_html()
    else:
        itemtable="抱歉，查無此商品"
        # print(itemtable)
    #     return redirect(url_for('index'))
    #     # name = form.name.data
    #     # form.name.data = ''
    return render_template('shopcrub.html', form=form,itemtable=product, name=session.get('name'),known=session.get('known',False))