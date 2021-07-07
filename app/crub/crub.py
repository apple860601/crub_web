import datetime
from os import path
import requests
resq=requests.Session()
import json
from .config import PChome,shopee,ruten
from ..model import db,Shop,Price,Itemname
from fake_useragent import UserAgent

PChome=PChome()
shopee=shopee()
ruten=ruten()
def PChomecrub(itname):    
    ress=PChome.get_item(item=itname)
    jd=json.loads(ress)
    items=[]
    with db.session.no_autoflush:
        for item in jd['prods']:
            itemid=PChome.get_itemid(item)
            minprice=maxprice=PChome.get_price(item)
            itemname=PChome.get_itemname(item)
            imageurl="https://e.ecimg.tw/"+PChome.get_imageid(item).replace("'",'"')
            # print("PChome: ",imageurl)
            if Itemname.query.filter_by(itemid=item['Id']).first() is None:
                items.append(Itemname(
                    itemid=itemid,
                    itemname=itemname,
                    shopname=Shop.query.filter_by(shop='PChome').first(),
                    imageurl=imageurl,
                    itemurl=Shop.query.filter_by(shop='PChome').first().URLform+itemid,
                    price=Price(
                        itemid=itemid,
                        minprice=minprice,
                        maxprice=maxprice,
                        updatetime=datetime.datetime.now()
                    )))
                # items.append(Price(itemid=item['Id'],minprice=item['price'],maxprice=item['price'],updatetime=datetime.now()))
        db.session.add_all(items)
        db.session.commit()

def shopeecrub(itname):
    ress=shopee.get_item(itname)
    items=[]
    jd=json.loads(ress)
    mainurl='https://shopee.tw/product/'
    with db.session.no_autoflush:
        for item in jd['items']:
            if item['ads_keyword']==None:
                itemname=shopee.get_itemname(item)
                maxitemprice=shopee.get_max_price(item)
                minitemprice=shopee.get_min_price(item)
                itemid=shopee.get_itemid(item)
                # imageids=json.dumps(["https://cf.shopee.tw/file/"+s for s in item['images']]).replace("'",'"')
                imageurl="https://cf.shopee.tw/file/"+shopee.get_imageid(item)
                # print("shopee ",imageurl)
                if Itemname.query.filter_by(itemid=itemid).first() is None:
                    items.append(Itemname(
                        itemid=itemid,
                        itemname=itemname,
                        shopname=Shop.query.filter_by(shop='shopee').first(),
                        imageurl=imageurl,
                        itemurl=Shop.query.filter_by(shop='shopee').first().URLform+str(item['shopid'])+'/'+str(itemid),
                        price=Price(
                            itemid=itemid,
                            minprice=minitemprice,
                            maxprice=maxitemprice,
                            updatetime=datetime.datetime.now())))
                    # items.append(Price(itemid=item['itemid'],minprice=minitemprice,maxprice=maxitemprice,updatetime=datetime.datetime.now()))
                    db.session.add_all(items)
                    db.session.commit()

def rutencrub(itname):
    resq2=ruten.get_item(itname)
    start=resq2.find("Id")-3
    last=resq2.find("LimitedTotalRows")-2
    str2=resq2[start:last]
    # print(str2)
    items=[]
    # print(str2)
    jd=json.loads(str2)
    with db.session.no_autoflush:
        for itemid in jd:
            id=ruten.get_itemid(itemid)
            product=ruten.get_product(id)
            start2=product.find("ProdId")-3
            last2=product.find("catch")-3
            product=product[start2:last2]
            print("ruten_product:",product)
            product_json=json.loads(product)
            itemname=ruten.get_itemname(product_json)
            minitemprice=ruten.get_min_price(product_json)
            maxitemprice=ruten.get_max_price(product_json)
            url="https://goods.ruten.com.tw/item/show?"+itemid['Id']
            imageurl="https://img.ruten.com.tw/"+ruten.get_imageid(product_json)
            # print("ruten: "+imageurl)
            # print(itemname)
            if Itemname.query.filter_by(itemid=itemid['Id']).first() is None:
                items.append(Itemname(
                    itemid=itemid['Id'],
                    itemname=itemname,
                    shopname=Shop.query.filter_by(shop='ruten').first(),
                    imageurl=imageurl,
                    itemurl=Shop.query.filter_by(shop='ruten').first().URLform+id,
                    price=Price(
                        itemid=itemid['Id'],
                        minprice=minitemprice,
                        maxprice=maxitemprice,
                        updatetime=datetime.datetime.now())
                    ))
        db.session.add_all(items)
        db.session.commit()