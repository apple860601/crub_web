from datetime import datetime


def PChomecrub(itname):    
    print("PChome crubing")
    import requests
    from bs4 import BeautifulSoup
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    resq=requests.Session()
    import json
    import sqlite3
    import mysql.connector as mysql
    from app import Itemname,Shop,Price,db
    itemdb=mysql.connect(
    host = "127.0.0.1",
    user = "root",
    password = "apple80558",
    database='itemdb'
    )
    cursor=itemdb.cursor()
    sqlstr="drop table if exists PCitem"
    cursor.execute(sqlstr)
    sqlstr="create table IF NOT exists PCitem (shop char(7),name char(100), minprice int(10),maxprice int(10), URL char(150),imageURL JSON)"
    cursor.execute(sqlstr)
    resq2=resq.get(f"https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={itname}&page=1&sort=sale/dc&sortParm=rnk")
    ress=resq2.text
    jd=json.loads(ress)
    items=[]
    prices=[]
    urls=[]
    mainurl="http://24h.pchome.com.tw/prod/"
    with db.session.no_autoflush:
        for item in jd['prods']:
            # itemname=item['name']
            # itemprice=item['price']
            # url=mainurl+item['Id']
            # imageids=json.dumps(["https://e.ecimg.tw"+item['picS']]).replace("'",'"')

            # print(imageids)
            # print (item['name'])
            # print ("價格",item['price'])
            # print("URL:",mainurl+item["Id"])
            
            if Itemname.query.filter_by(itemid=item['Id']).first() is None:
                items.append(Itemname(itemid=item['Id'],itemname=item['name'],shopname=Shop.query.filter_by(shop='PChome').first()))
                items.append(Price(itemnameId=Itemname.query.filter_by(itemid=item['id']).first(),minprice=item['price'],maxprice=item['price'],updatetime=datetime.now()))
            # sqlstr=f"insert into PCitem values('PChome','{itemname}','{itemprice}','{itemprice}','{url}','{imageids}')"
            # cursor.execute(sqlstr)
            # itemdb.commit()
        db.session.add_all(items)
        db.session.commit()

