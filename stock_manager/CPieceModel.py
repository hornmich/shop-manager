'''
Created on 15. 11. 2019

@author: Michal Horn
'''
from CPurchaseHistory import ItemPurchase

class PieceModel():
    '''
    classdocs
    '''


    def __init__(self, name, price, purchases):
        '''
        Constructor
        '''
        self._name=name
        self._price=price
        self._purchases=purchases
        
    def get_piece(self):
        return {"name":self._name, "price":self._price, "purchases": self._purchases}
        