'''
Created on 15. 11. 2019

@author: Michal Horn
'''
from CPieceModel import PieceModel
from CPurchaseHistory import ItemPurchase

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
            PieceModel("Plenky1", 20, [ItemPurchase("12.3.2019", 60, 500, "Billa"), ItemPurchase("12.4.2019", 60, 150, "Tesco"), ItemPurchase("12.5.2019", 60, 300, "Kaufland")]),
            PieceModel("Plenky2", 30, [ItemPurchase("12.3.2019", 60, 500, "Billa"), ItemPurchase("12.4.2019", 60, 150, "Tesco"), ItemPurchase("12.5.2019", 60, 300, "Kaufland")]),
            PieceModel("Plenky3", 40, [ItemPurchase("12.3.2019", 60, 500, "Billa"), ItemPurchase("12.4.2019", 60, 150, "Tesco"), ItemPurchase("12.5.2019", 60, 300, "Kaufland")])]
        
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
        return [(["N/A","N/A"],1)]
            
    def get_reduce_history(self):
        return [(["N/A","N/A","N/A"],1)]
    
    @property
    def currentId(self):
        logging.debug('currentId getter called.')
        logging.debug('current ID: %s ', str(self._currentId) or "None")
        return self._currentId
    
    @currentId.setter
    def currentId(self, cId):
        logging.debug('currentId setter called.')
        self._currentId=cId
        logging.debug('current ID: %s ', str(self._currentId) or "None")
        
            
            
            