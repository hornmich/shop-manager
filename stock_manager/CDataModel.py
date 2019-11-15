'''
Created on 15. 11. 2019

@author: Michal Horn
'''
from CSettingsModel import SettingsModel
from CStockModel import StockModel

class DataModel():
    def __init__(self):
        self.settings = SettingsModel()
        self.stock=StockModel()
        
    

