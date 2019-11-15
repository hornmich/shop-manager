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
        i = 1
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
            i = 1
            for purchase in self._items[self._currentId]._purchases:
                historyRecord = ([purchase._date, purchase._pieces, purchase._price, purchase._place], i)
                i = i+1
                history.append(historyRecord)
            return history
            
    def get_sell_history(self):
        return [(["N/A","N/A"],1)]
            
    def get_reduce_history(self):
        return [(["N/A","N/A","N/A"],1)]
            
            
            