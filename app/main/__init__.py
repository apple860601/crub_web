from ..model import Permission,Shop,Role,User
from flask import Blueprint
main=Blueprint('main',__name__)
import os
from .. import db
from . import views,errors

@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)

# shopee=Shop(shop="shopee",URLform="https://shopee.tw/product/",IURLform="https://cf.shopee.tw/file/")
# PChome=Shop(shop="PChome",URLform="http://24h.pchome.com.tw/prod/",IURLform="https://e.ecimg.tw")
# ruten=Shop(shop="ruten",URLform="https://goods.ruten.com.tw/item/show?",IURLform="https://img.ruten.com.tw/")
# Administrator=Role(permissions=Permission.ADMIN,name="admin")
# moderate=Role(permissions=Permission.MODERATE,name="moderate")
# users=Role(permissions=Permission.WRITE,name="user")
# db.session.add_all([shopee,PChome,ruten,Administrator,moderate,users])
# db.session.commit()