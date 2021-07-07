from enum import unique
from . import db
from datetime import datetime
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
    itemid=db.Column(db.String(100),primary_key=True)
    minprice=db.Column(db.Integer)
    maxprice=db.Column(db.Integer)
    updatetime=db.Column(db.DateTime,onupdate=datetime.now,default=datetime.now)
    item=db.relationship('Itemname',backref='price')

    # def __repr__(self) -> str:
    #     return f'{self.minprice} ~ {self.maxprice}'
    def __init__(self,itemid,minprice,maxprice,updatetime) -> None:
        self.itemid=itemid
        self.minprice=minprice
        self.maxprice=maxprice
        self.updatetime=updatetime
        
class Shop(db.Model):
    __tablename__='Shop'
    id=db.Column(db.Integer,primary_key=True)
    shop=db.Column(db.String(10),unique=True)
    URLform=db.Column(db.String(150))
    IURLform=db.Column(db.String(150))
    item=db.relationship('Itemname',backref='shopname')

    # def __repr__(self):
    #     return f'{self.shop}' 
    def __init__(self,shop,URLform,IURLform) -> None:
        self.shop=shop
        self.URLform=URLform
        self.IURLform=IURLform

class Itemname(db.Model):
    __tablename__='Itemname'
    itemid=db.Column(db.String(30),primary_key=True)
    itemname=db.Column(db.String(150))
    shopid=db.Column(db.Integer,db.ForeignKey('Shop.id'))
    priceid=db.Column(db.String(100),db.ForeignKey('Price.itemid'))
    imageurl=db.Column(db.String(100))
    itemurl=db.Column(db.String(100))
    # item=db.relationship('Price',backref='itemnameId')
    # min_price=db.Column(db.Integer,db.ForeignKey('Price.id'))
    # maxprice=db.Column(db.Integer,db.ForeignKey('Price.maxprice'))

    # def __repr__(self):
    #     return str(self.itemname),str(self.shopname),str(self.price)
    def __init__(self,itemid,itemname,shopname,price,imageurl,itemurl) -> None:
        self.itemid=itemid
        self.itemname=itemname
        self.shopname=shopname
        self.price=price
        self.imageurl=imageurl
        self.itemurl=itemurl

    def all(self):
        return self.itemname,self.shopid,self.priceid
