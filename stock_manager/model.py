'''
Created on 27. 11. 2019

@author: michal
'''
from _datetime import datetime
from stock_manager.loaders import HeurekaXMLLoader
import logging
from asciimatics.screen import logger
from cupshelpers.cupshelpers import activateNewPrinter

class PieceModel():
    '''
    classdocs
    '''


    def __init__(self, name, price, purchases, sales, reduces):
        '''
        Constructor
        '''
        self._name=name
        self._price=price
        self._purchases=purchases
        self._sales=sales
        self._reduces=reduces
        
    def get_piece(self):
        return {"name":self._name, "price":self._price, "purchases": self._purchases}
    
    def add_purchase(self, count, price, shop):
        purchase = ItemPurchase(datetime.today(), count, price, shop)
        self._purchases.append(purchase)
    
    def reduce_item(self, count, reason):
        reduce = ItemReduce(datetime.today(), count, reason)
        self._reduces.append(reduce)
      
class ItemPurchase(object):
    '''
    classdocs
    '''


    def __init__(self, date, pieces, price, place):
        '''
        Constructor
        '''
        
        self._date = date
        self._pieces = pieces
        self._price = price
        self._place = place
        
    def get_item_history(self):
        return {"date":self._date, "pieces":self._pieces, "price":self._price, "place":self._place}
        
class ItemReduce(object):
    '''
    classdocs
    '''


    def __init__(self, date, pieces, reason):
        '''
        Constructor
        '''
        
        self._date = date
        self._pieces = pieces
        self._reason = reason
        
    def get_item_history(self):
        return {"date":self._date, "pieces":self._pieces, "reason":self._reason}
        
class ItemSale(object):
    '''
    classdocs
    '''


    def __init__(self, date, pieces):
        '''
        Constructor
        '''
        
        self._date = date
        self._pieces = pieces
        
    def get_item_history(self):
        return {"date":self._date, "pieces":self._pieces}
        
class SettingsModel():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._feedUrl = "http://somefeedurl.com"
        self._margin = 15
        
        
    def get_settings(self):
        return {"feedUrl": self._feedUrl, "margin": self._margin}

class StockModel(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._currentId=None
        self._items=[
            PieceModel("Plenky1", 20,
                       [ItemPurchase("2.3.2019", 60, 500, "Billa"), ItemPurchase("2.4.2019", 60, 150, "Tesco"), ItemPurchase("2.5.2019", 60, 300, "Kaufland")],
                       [ItemSale("2.3.2019", 5), ItemSale("3.3.2019", 5), ItemSale("4.3.2019", 5)],
                       [ItemReduce("2.3.2019", 1, "Duvod 1"), ItemReduce("3.3.2019", 1, "Duvod 2"), ItemReduce("4.3.2019", 1, "Duvod 3")]
                       ),
            PieceModel("Plenky2", 30,
                       [ItemPurchase("12.3.2019", 60, 500, "Billa"), ItemPurchase("12.4.2019", 60, 150, "Tesco"), ItemPurchase("12.5.2019", 60, 300, "Kaufland")],
                       [ItemSale("12.3.2019", 5), ItemSale("13.3.2019", 5), ItemSale("14.3.2019", 5)],
                       [ItemReduce("12.3.2019", 1, "Duvod 1"), ItemReduce("13.3.2019", 1, "Duvod 2"), ItemReduce("14.3.2019", 1, "Duvod 3")]
                       ),
            PieceModel("Plenky3", 40,
                       [ItemPurchase("22.3.2019", 60, 500, "Billa"), ItemPurchase("22.4.2019", 60, 150, "Tesco"), ItemPurchase("22.5.2019", 60, 300, "Kaufland")],
                       [ItemSale("22.3.2019", 5), ItemSale("23.3.2019", 5), ItemSale("24.3.2019", 5)],
                       [ItemReduce("22.3.2019", 1, "Duvod 1"), ItemReduce("23.3.2019", 1, "Duvod 2"), ItemReduce("24.3.2019", 1, "Duvod 3")]
                       )
            ]
        
        self._deleted=[]
        
    def get_stock_summary(self):
        summary = []
        i = 0
        for item in self._items:
            rec = (item._name, i)
            summary.append(rec)
            i = i+1
            
        return summary
    
    def get_products_names(self):
        names = []
        for item in self._items:
            names.append(item._name)
        return frozenset(names)
    
    def get_purchase_history(self):
        if self._currentId is None:
            return [(["N/A","N/A","N/A","N/A"],1)]
        else:
            history = []
            i = 0
            for purchase in self._items[self._currentId]._purchases:
                historyRecord = ([str(purchase._date), str(purchase._pieces), str(purchase._price), str(purchase._place)], i)
                i = i+1
                history.append(historyRecord)
            return history
            
    def get_sell_history(self):
        if self._currentId is None:
            return [(["N/A","N/A"],1)]
        else:
            history = []
            i = 0
            for purchase in self._items[self._currentId]._sales:
                historyRecord = ([str(purchase._date), str(purchase._pieces)], i)
                i = i+1
                history.append(historyRecord)
            return history
           
    def get_reduce_history(self):
        if self._currentId is None:
            return [(["N/A","N/A","N/A"],1)]
        else:
            history = []
            i = 0
            for purchase in self._items[self._currentId]._reduces:
                historyRecord = ([str(purchase._date), str(purchase._pieces), str(purchase._reason)], i)
                i = i+1
                history.append(historyRecord)
            return history
        
    def add_purchased_item(self, count, price, shop):
        if self.currentId is None:
            return
        
        self._items[self.currentId].add_purchase(count, price, shop)
        
    def add_item(self, name, price):
        self._items.append(PieceModel(name, price, [], [], []))
        logger.debug("_items: %s", str(self._items))
        
    def delete_by_name(self, name):
        idx = 0
        for item in self._items:
            if item._name is name:
                del(self._items[idx])
            idx = idx+1

    def reduce_item(self, count, reason):
        if self.currentId is None:
            return
        
        self._items[self.currentId].reduce_item(count, reason)

    def delete_item(self):
        if self.currentId is None:
            return
        
        self._deleted.append(self._items[self.currentId])
        self._items.remove(self._items[self.currentId])
    
    @property
    def currentId(self):
        return self._currentId
    
    @currentId.setter
    def currentId(self, cId):
        self._currentId=cId
        
class HeurekaFeedModel():
    def __init__(self, feedLoader, stock):
        self._currentActionId=None
        self._feedLoader = feedLoader
        self._stock = stock
        self._actions = []
        logging.basicConfig(filename='./app.log', filemode='w', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

            
    def load(self, url):
        self._actions = []
        shop_products = self._feedLoader.get_products_names(url=url)    
        index=0
        current_products = self._stock.get_products_names()
        for add_product in (shop_products-current_products) :
            action = ([add_product, 'Pridat'], index)
            index = index+1
            self._actions.append(action)
        for remove_product in (current_products-shop_products) :
            action = ([remove_product, 'Odebrat'], index)
            index = index+1
            self._actions.append(action)
    
    def get_actions(self):
        return self._actions
    
    def find_selected_action_index(self):
        index = 0
        for action in self._actions:
            if action[1] is self._currentActionId:
                return index
            index = index+1
        return None
    
    def apply_selected(self):
        if self._currentActionId is None:
            return
        
        idx = self.find_selected_action_index()
        if idx is None:
            return
        
        if (self._actions[idx][0][1] is "Odebrat"):
            logging.debug('Odebirani produktu id %d', self._currentActionId)
            self._stock.delete_by_name(self._actions[idx][0][0])
            del(self._actions[idx])
        elif (self._actions[idx][0][1] is "Pridat"):
            logging.debug('Pridavani produktu id %d', self._currentActionId)
            self._stock.add_item(self._actions[idx][0][0], price=10)
            del(self._actions[idx])
                
        logging.debug('Akce id %d typ %s', self._currentActionId, str(self._actions))
    
    def ignore_selected(self):
        if self._currentActionId is None:
            return
        
        idx = self.find_selected_action_index()
        if idx is None:
            return
        
        del(self._actions[idx])
            
    def apply_all(self):
        for action in self._actions:
            self._currentActionId = action[1]
            self.apply_selected()
    
    @property
    def currentActionId(self):
        return self._currentActionId
    
    @currentActionId.setter
    def currentActionId(self, cId):
        self._currentActionId=cId

class DataModel():
    def __init__(self, feedLoader):
        self.settings = SettingsModel()
        self.stock=StockModel()
        self.xmlFeed=HeurekaFeedModel(feedLoader, self.stock)
        
