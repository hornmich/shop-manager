'''
Created on 27. 11. 2019

@author: michal
'''
from _datetime import datetime

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

class DataModel():
    def __init__(self):
        self.settings = SettingsModel()
        self.stock=StockModel()
        
