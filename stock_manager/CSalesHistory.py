'''
Created on 18. 11. 2019

@author: Michal Horn
'''

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
        