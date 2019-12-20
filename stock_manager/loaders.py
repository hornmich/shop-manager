'''
Created on 2. 12. 2019

@author: michal@apartman.cz
'''

import xmltodict
import urllib
import html
from copyreg import constructor


class HeurekaXMLLoader(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def get_products_names(self, url):
        '''
        Construct frozen set all shop products names.
        '''    
        shop_products=[]
        with urllib.request.urlopen(url) as fd:
            doc = xmltodict.parse(fd.read())
            for product in doc['SHOP']['SHOPITEM']:
                prod_name=html.unescape(product['PRODUCTNAME'])
                shop_products.append(prod_name)
        return frozenset(shop_products)
            
            
class EshopRychleOrdersLoader(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        constructor
        '''
        pass
    
    def get_orders(self, url):
        '''
        Construct list of all orders in the imported XML.
        '''    
        orders=[]
        with urllib.request.urlopen(url) as fd:
            xml_orders = xmltodict.parse(fd.read())['orders']['order']
            if (type(xml_orders) != list):
                print('\tConverting orders into list.')
                xml_orders = [xml_orders]
            for xml_order in xml_orders:
                order = self._load_order(xml_order)
                orders.append(order)

        return orders       
    
    def _load_order(self, xml):
        state = xml['info']['lastState']
        order_id = xml['info']['orderID']
        date = xml['info']['date']
        price = xml['info']['total']
        xml_products=xml['products']['product']
        items = self._load_items(xml_products)
        return {'id' : order_id, 'date': date, 'state': state, 'price': price, 'items': items}
    
    def _load_items(self, xml):
        products = []
        if (type(xml) != list):
            xml = [xml]
            
        for xml_product in xml:
            cnt=int(xml_product['pieces'])
            price=int(xml_product['price'])
            prod_name=html.unescape(xml_product['name'])
            #index = re.search("[0-9]\ *ks", html.unescape(xml_product['name']))
            #prod=xml_product['name'][:index.end()]
            if (prod_name != ''):
                products.append({'name': prod_name, 'count': cnt, 'price': price})                
            else:
                ''' invalid name of product '''
                pass
        return products
    