import requests
from fake_useragent import UserAgent 
ua = UserAgent()
class crub:
    headers = {
        'User-Agent':ua.random
    }
    ses=requests.Session()

class shopee(crub):
    basicURL="https://shopee.tw/api/v4/search/search_items?by=relevancy&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
    # limit=100
    
    def get_item(self,item,limit=100):
        if item!=None:
            response=self.ses.get(self.basicURL+f'&keyword={item}&limit={limit}',
            headers=self.headers,
            allow_redirects=False
            ).text
            return response
        else:
            return None

    def get_itemname(self,item):
        if item!=[]:
            return item['item_basic']['name']
        else:
            return None
    
    def get_itemid(self,item):
        if item!=[]:
            return item['item_basic']['itemid']
        else:
            return None  

    def get_min_price(self,item):
        if item!=[]:
            return item['item_basic']['price_min']/100000
        else:
            return None      

    def get_max_price(self,item):
        if item!=[]:
            return int(item['item_basic']['price_max'])/100000
        else:
            return None  

    def get_imageid(self,item):
        if item!=[]:
            return item['item_basic']['image']
        else:
            return None

class PChome(crub):
    basicURL="https://ecshweb.pchome.com.tw/search/v3.3/all/results?page=1&sort=sale/dc&sortParm=rnk"
    # limit=100
    
    def get_item(self,item,limit=100):
        if item!=None:
            response=self.ses.get(self.basicURL+f'&q={item}',
            headers=self.headers,
            allow_redirects=False
            ).text
            return response
        else:
            return None

    def get_itemname(self,item):
        if item!=[]:
            return item['name']
        else:
            return None
    
    def get_itemid(self,item):
        if item!=[]:
            return item['Id']
        else:
            return None  

    def get_price(self,item):
        if item!=[]:
            return item['price']
        else:
            return None    

    def get_imageid(self,item):
        if item!=[]:
            return item['picS']
        else:
            return None

class ruten(crub):
    basicURL='''https://rtapi.ruten.com.tw/api/search/v3/index.php/core/prod?type=direct&sort=rnk%2Fdc&offset=1&2628348&_callback=jsonpcb_CoreProd'''

    productURL="https://rtapi.ruten.com.tw/api/prod/v2/index.php/prod?_callback=jsonpcb_Prod"
    # limit=100
    
    def get_item(self,item,limit=48):
        if item!=None:
            response=self.ses.get(self.basicURL+f'&q={item}&limit={limit}',
            headers=self.headers,
            allow_redirects=False
            ).text
            return response
        else:
            return None

    def get_product(self,itemid):
        if itemid!=None:
            response=self.ses.get(self.productURL+f'&id={itemid}',
            headers=self.headers,
            allow_redirects=False
            ).text
            # print(self.productURL+f'&id={itemid}')
            return response
        else:
            return None

    def get_itemname(self,item):
        if item!=[]:
            return item[0]['ProdName']
        else:
            return None
    
    def get_itemid(self,item):
        if item!=[]:
            return item['Id']
        else:
            return None  

    def get_min_price(self,item):
        if item!=[]:
            return item[0]['PriceRange'][0]
        else:
            return None

    def get_max_price(self,item):
        if item!=[]:
            return item[0]['PriceRange'][1]
        else:
            return None
    
    def get_imageid(self,item):
        if item!=[]:
            return item[0]['Image']
        else:
            return None
