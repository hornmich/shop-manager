'''
Created on 15. 11. 2019

@author: Michal Horn
'''

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
        