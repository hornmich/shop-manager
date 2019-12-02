'''
Created on 2. 12. 2019

@author: michal@apartman.cz
'''

import xmltodict
import urllib
import html


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
            