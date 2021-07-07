def work(itname):
    print("Crubing")
    from .crub import PChomecrub,rutencrub,shopeecrub
    # import PChome
    # import ruten
    # import shopee2
    # import sqlite3
    import mysql.connector as mysql
    import time
    from ..model import Shop,db
    if Shop.query.filter_by(shop='shopee').first() is None:
        db.session.add(Shop(shop="shopee",URLform='https://shopee.tw/product/',IURLform="https://cf.shopee.tw/file/"))
    if Shop.query.filter_by(shop='PChome').first() is None:
        db.session.add(Shop(shop='PChome',URLform="http://24h.pchome.com.tw/prod/",IURLform="https://e.ecimg.tw"))
    if Shop.query.filter_by(shop='ruten').first() is None:
        db.session.add(Shop(shop='ruten',URLform="https://goods.ruten.com.tw/item/show?",IURLform="https://img.ruten.com.tw/"))
    db.session.commit()
    # from ..model import db,Shop,Price,Itemname
    # itname=str(input())
    start=time.time()
    print("shopee")
    PChomecrub(itname)
    shopeetime=time.time()-start
    rutencrub(itname)
    PChometime=time.time()-start-shopeetime
    shopeecrub(itname)
    rutentime=time.time()-start-PChometime-shopeetime
    
    print("shopeetime: ",shopeetime)
    print("PChometime: ",PChometime)
    print("rutentime: ",rutentime)
    print("totaltime: ",time.time()-start)




