def work(itname):
    print("Crubing")
    import PChome
    import ruten
    import shopee2
    import sqlite3
    import mysql.connector as mysql
    import time
    from app import db,Shop,Price,Itemname
    # itname=str(input())
    start=time.time()
    print("shopee")
    shopee2.shopeecrub(itname)
    shopeetime=time.time()-start
    PChome.PChomecrub(itname)
    PChometime=time.time()-start-shopeetime
    ruten.retencrub(itname)
    rutentime=time.time()-start-PChometime-shopeetime
    # maindb=mysql.connect(
    #     host = "127.0.0.1",
    #     user = "root",
    #     password = "apple80558",
    #     database='itemdb'
    #     )
    # maincur=maindb.cursor()
    # sqlstr="create table if not exists mainlist (shop char(7),name char(100), minprice int(10),maxprice int(10), URL char(150),image JSON)"
    # maincur.execute(sqlstr)
    # sqlstr1="INSERT INTO mainlist SELECT * FROM PCitem where PCitem.name not in (select NAME from mainlist) "
    # sqlstr2="INSERT INTO mainlist SELECT * FROM shopeeitem where shopeeitem.name not in (select NAME from mainlist) "
    # sqlstr3="INSERT INTO mainlist SELECT * FROM rutenitem where rutenitem.name not in (select NAME from mainlist) "
    # maincur.execute(sqlstr1)
    # maincur.execute(sqlstr2)
    # maincur.execute(sqlstr3)
    # maindb.commit()
    
    print("shopeetime: ",shopeetime)
    print("PChometime: ",PChometime)
    print("rutentime: ",rutentime)
    print("totaltime: ",time.time()-start)




