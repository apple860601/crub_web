def PChomecrub(itname):    
    from datetime import datetime
    import requests
    resq=requests.Session()
    import json
    from ..model import db,Shop,Price,Itemname
    resq2=resq.get(f"https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={itname}&page=1&sort=sale/dc&sortParm=rnk")
    ress=resq2.text
    jd=json.loads(ress)
    items=[]
    mainurl="http://24h.pchome.com.tw/prod/"
    with db.session.no_autoflush:
        for item in jd['prods']:
            # itemname=item['name']
            # itemprice=item['price']
            # url=mainurl+item['Id']
            # imageids=json.dumps(["https://e.ecimg.tw"+item['picS']]).replace("'",'"')
            print("PChome "+"https://e.ecimg.tw"+item['picS'])
            if Itemname.query.filter_by(itemid=item['Id']).first() is None:
                items.append(Itemname(
                    itemid=item['Id'],
                    itemname=item['name'],
                    shopname=Shop.query.filter_by(shop='PChome').first(),
                    imageurl=json.dumps(["https://e.ecimg.tw"+item['picS']]).replace("'",'"'),
                    price=Price(
                        itemid=item['Id'],
                        minprice=item['price'],
                        maxprice=item['price'],
                        updatetime=datetime.now()
                    )))
                # items.append(Price(itemid=item['Id'],minprice=item['price'],maxprice=item['price'],updatetime=datetime.now()))
        db.session.add_all(items)
        db.session.commit()

