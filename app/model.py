from enum import unique
from operator import index

from werkzeug.wrappers import request
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from flask_login import UserMixin,AnonymousUserMixin
# from itsdangerous import TimedSerializer as Serializer
from itsdangerous.jws import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,request
import hashlib

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    default=db.Column(db.Boolean,default=False,index=True)
    permissions=db.Column(db.Integer)
    name=db.Column(db.String(64),unique=True)
    users=db.relationship('User',backref='role')

    def __init__(self,**kwargs) -> None:
        super(Role,self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    #檢查是否有該權限
    def has_permission(self,perm):
        return self.permissions & perm == perm

    def add_permission(self,perm):
        if not self.has_permission(perm):
            self.permissions+=perm

    def remove_permission(self,perm):
        if self.has_permission(perm):
            self.permissions-=perm
    
    def reset_permission(self):
        self.permissions=0

    @staticmethod
    def insert_roles():
        roles={
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role='User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default=(role.name==default_role)
            db.session.add(role)
        db.session.commit()

    def __repr__(self) -> str:
        return f'<Role {self.name}>'
#UserMixin會將current_user和User模組連結在一起
class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    location=db.Column(db.String(64))
    about_me=db.Column(db.Text())
    member_since=db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen=db.Column(db.DateTime(),default=datetime.utcnow)
    email=db.Column(db.String(64),unique=True,index=True)
    username=db.Column(db.String(128),unique=True,index=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    password_hash=db.Column(db.String(128))
    confirmed=db.Column(db.Boolean,default=False)
    avatar_hash=db.Column(db.String(32))

    def gravatar(self,size=100,default='identicon',rating='g'):
        if request.is_secure:
            url='https://secure.gravatar.com/avatar'
        else:
            url='http://www.gravatar.com/avatar'
        hash=self.avatar_hash or self.gravatar_hash()
        return f'{url}/{hash}?s={size}&d={default}&r={rating}'

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.email == current_app.config['FLASKY_ADMIN']:
            self.role = Role.query.filter_by(name='Administrator').first()
        if self.role is None:
            self.role=Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash=self.gravatar_hash()

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash=self.gravatar_hash()
        db.session.add(self)
        return True

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()



    def ping(self):
        #更新使用者登入時間
        self.last_seen=datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    @property
    def password(self):
        #宣告password非可讀取的項目(因為經過hash過了)
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        #生成password hash碼
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        #確認使用者輸入的密碼是否跟database裡的一樣
        return check_password_hash(self.password_hash,password)

    def generate_confirmation_token(self,expiration=3600):
        #生成確認權杖，時限為一小時，若有效則confirmed為True
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')

    def confirm(self,token):
        #確認權杖的id符合登入的使用者(current_app)
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm')!= self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        return True

    def can(self,perm):
        return self.role is not None and self.role.has_permission(perm)
    
    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def __repr__(self) -> str:
        return f'<User {self.username}>'

class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False
    def is_administrator(self):
        return False

class Price(db.Model):
    __tablename__='price'
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
    __tablename__='shop'
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
    __tablename__='itemname'
    itemid=db.Column(db.String(30),primary_key=True)
    itemname=db.Column(db.String(150))
    shopid=db.Column(db.Integer,db.ForeignKey('shop.id'))
    priceid=db.Column(db.String(100),db.ForeignKey('price.itemid'))
    imageurl=db.Column(db.String(150))
    itemurl=db.Column(db.String(100))

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

login_manager.anonymous_user = AnonymousUser