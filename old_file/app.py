from enum import unique
from flask import Flask,request,make_response,render_template,session
from flask.helpers import url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate
from datetime import datetime
from flask_wtf import FlaskForm
from sqlalchemy.orm import backref
from main import work
# from sqlalchemy.orm import session
from werkzeug.utils import redirect
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
app=Flask(__name__)

bootstrap=Bootstrap(app)
moment=Moment(app)

basedir=os.path.abspath(os.path.dirname(__file__))
#設置"charset=utf8mb4"是為了辨識特殊字元(如:🔊),其經utf-8編碼後會有四個位元，而utf8預設編碼只能辨識三個位元，因此須加上此參數才能正確辨認
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:apple80558@localhost/flaskdb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = 'hard to guess string'
db=SQLAlchemy(app)
migrate=Migrate(app,db)
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
    

class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    users=db.relationship('User',backref='role')

    def __repr__(self) -> str:
        return f'<Role {self.name}>'

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self) -> str:
        return f'<User {self.username}>'

class Price(db.Model):
    __tablename__='Price'
    itemid=db.Column(db.String(100),db.ForeignKey('Itemname.itemid'),primary_key=True)
    minprice=db.Column(db.Integer)
    maxprice=db.Column(db.Integer)
    updatetime=db.Column(db.DateTime,onupdate=datetime.now,default=datetime.now)
    # item=db.relationship('Itemname',backref='price')

    def __repr__(self) -> str:
        return f'<Price {self.minprice} ~ {self.maxprice}>'
        
class Shop(db.Model):
    __tablename__='Shop'
    id=db.Column(db.Integer,primary_key=True)
    shop=db.Column(db.String(10),unique=True)
    URLform=db.Column(db.String(150))
    IURLform=db.Column(db.String(150))
    item=db.relationship('Itemname',backref='shopname')

    def __repr__(self) -> str:
        return f'<Shopname {self.shop}>' 

class Itemname(db.Model):
    __tablename__='Itemname'
    itemid=db.Column(db.String(30),primary_key=True)
    itemname=db.Column(db.String(150))
    shopid=db.Column(db.Integer,db.ForeignKey('Shop.id'))
    item=db.relationship('Price',backref='itemnameId')
    # min_price=db.Column(db.Integer,db.ForeignKey('Price.id'))
    # maxprice=db.Column(db.Integer,db.ForeignKey('Price.maxprice'))

    def __repr__(self) -> str:
        return f'{self.itemname}'


         
db.create_all()
# print(User.query.filter_by(username='tt').first())
if Shop.query.filter_by(shop='shopee').first() is None:
    
    shopee=Shop(shop="shopee",URLform='https://shopee.tw/product/',IURLform="https://cf.shopee.tw/file/")
    db.session.add(shopee)
if Shop.query.filter_by(shop='PChome').first() is None:
    
    PChome=Shop(shop='PChome',URLform="http://24h.pchome.com.tw/prod/",IURLform="https://e.ecimg.tw")
    db.session.add(PChome)
if Shop.query.filter_by(shop='ruten').first() is None:
    ruten=Shop(shop='ruten',URLform="https://goods.ruten.com.tw/item/show?",IURLform="https://img.ruten.com.tw/")
    db.session.add(ruten)
db.session.commit()
# db.session.no_autoflush()
# db.session.add(Shop(shop='shopee',URLform='https://shopee.tw/product/',IURLform="https://cf.shopee.tw/file/"))
# db.session.add(Shop(shop='PChome',URLform="http://24h.pchome.com.tw/prod/",IURLform="https://e.ecimg.tw"))
# db.session.add(Shop(shop='ruten',URLform="https://goods.ruten.com.tw/item/show?",IURLform="https://img.ruten.com.tw/"))
# db.session.commit()
@app.route('/', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
        # name = form.name.data
        # form.name.data = ''
    return render_template('index.html', form=form, name=session.get('name'),known=session.get('known',False))

@app.route('/shopcrub', methods=['GET', 'POST'])
def shopcrub():
    # name = None
    db.session.rollback()
    form = NameForm()
    itemnm=form.name.data
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
        # print(item)
        itemtable=pd.DataFrame(item).to_html()
    else:
        itemtable="抱歉，查無此商品"
        # print(itemtable)
    #     return redirect(url_for('index'))
    #     # name = form.name.data
    #     # form.name.data = ''
    return render_template('shopcrub.html', form=form,itemtable=itemtable, name=session.get('name'),known=session.get('known',False))

@app.route('/name/<name>')
def user(name):
    return f'<h1>Hello {name}!</h1>'

@app.route('/user/')
def user_agent():
    user_agent=request.headers.get('User-Agent')
    return f'<h1>Your browser is {user_agent}</h1>'

@app.route('/bad_request')
def bad_request():
    return f'<h1>bad_request</h1>',400

@app.route('/cookie')
def cookie():
    res=make_response('<h1>carried cookie</h1>')
    res.set_cookie('anwser','42')
    return res

@app.route('/render/<name>')
def render(name):
    return render_template('index.html',name=name)

@app.route('/square/<square>')
def square(square):
    try: 
        square=int(square)
        return render_template('integer.html',number=square)
    except Exception as e:
        print(str(e))
        return render_template('integer_error.html')

@app.route('/bootstrap/<name>')
def bootstrap_name(name):
    return render_template('./boolstrap_tmp/user.html',name=name)

# @app.route('/wtf/<name>')
# def bootstrap_name(name):
#     return render_template('./boolstrap_tmp/user.html',name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('./boolstrap_tmp/404.html'),404

if __name__ == '__main__':
    app.run(debug=True)
