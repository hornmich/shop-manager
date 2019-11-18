'''
Created on 18. 11. 2019

@author: Michal Horn
'''

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
        