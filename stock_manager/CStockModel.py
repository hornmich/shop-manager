'''
Created on 15. 11. 2019

@author: Michal Horn
'''
from CPieceModel import PieceModel
from CPurchaseHistory import ItemPurchase
from CSalesHistory import ItemSale
from CReducesHistory import ItemReduce

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
    
    @property
    def currentId(self):
        return self._currentId
    
    @currentId.setter
    def currentId(self, cId):
        self._currentId=cId
        
            
            
            