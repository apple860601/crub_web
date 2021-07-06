def retencrub(itname):
    import requests
    resq=requests.Session()
    import json
    from fake_useragent import UserAgent
    from .. import db
    from ..model import Shop,Price,Itemname
    import datetime
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }
    resq2=resq.get(f"https://rtapi.ruten.com.tw/api/search/v3/index.php/core/prod?q={itname}&type=direct&sort=rnk%2Fdc&offset=1&limit=48&2628348&_callback=jsonpcb_CoreProd",headers=headers)
    str1=resq2.text
    start=str1.find("Id")-3
    last=str1.find("LimitedTotalRows")-2
    str2=str1[start:last]
    # print(str2)
    items=[]
    jd=json.loads(str2)
    with db.session.no_autoflush:
        for itemid in jd:
            resq3=resq.get(f"https://rtapi.ruten.com.tw/api/prod/v2/index.php/prod?id={itemid['Id']}&_callback=jsonpcb_Prod",headers=headers)
            str3=resq3.text
            start2=str3.find("ProdId")-3
            last2=str3.find("catch")-3
            str4=str3[start2:last2]
            jd2=json.loads(str4)
            itemname=jd2[0]['ProdName']
            minitemprice=jd2[0]['PriceRange'][0]
            maxitemprice=jd2[0]['PriceRange'][1]
            url="https://goods.ruten.com.tw/item/show?"+itemid['Id']
            imageids=json.dumps(["https://img.ruten.com.tw/"+jd2[0]['Image']]).replace("'",'"')
            imageids="https://img.ruten.com.tw/"+jd2[0]['Image']
            print("ruten: "+imageids)
            # print(itemname)
            if Itemname.query.filter_by(itemid=itemid['Id']).first() is None:
                items.append(Itemname(
                    itemid=itemid['Id'],
                    itemname=itemname,
                    shopname=Shop.query.filter_by(shop='ruten').first(),
                    imageurl=imageids,
                    price=Price(
                        itemid=itemid['Id'],
                        minprice=minitemprice,
                        maxprice=maxitemprice,
                        updatetime=datetime.datetime.now())
                    ))
        db.session.add_all(items)
        db.session.commit()