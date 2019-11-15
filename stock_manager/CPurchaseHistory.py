'''
Created on 15. 11. 2019

@author: eaton
'''

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
        