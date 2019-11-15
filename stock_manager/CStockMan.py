'''
Created on 13. 10. 2019

@author: michal
'''

from asciimatics.screen import ManagedScreen
from asciimatics.scene import Scene

from CMainMenuView import MainMenuView
from CStockView import StockView
from CAddStockView import AddStockView
from CReduceStockView import ReduceStockView
from CProductsDetailsView import ProductsDetailsView
from CPurchaseHistoryView import PurchaseHistoryView
from CSellHistoryView import SellHistoryView
from CReduceHistoryView import ReduceHistoryView
from CImportFromEshopView import ImportFromEshopView

from CDataModel import DataModel


from time import sleep

class StockModel(object):
    def __init__(self):
        self.current_id = None

    def get_summary(self):
        dct = ("p1", "p2")
        
        return dct
    
    def get_current_item(self):        
        if self.current_id is None:
            return {"count": "", "price": "", "shop": ""}
        else:
            return self.get_contact(self.current_id)

@ManagedScreen
def demo(screen=None):
    model = DataModel()
    scenes = [
        Scene([MainMenuView(screen, None)], -1, name="MainMenu"),
        Scene([StockView(screen, model)], -1, name="StockView"),
        Scene([AddStockView(screen, model)], -1, name="AddStock"),
        Scene([ReduceStockView(screen, model)], -1, name="ReduceStock"),
        Scene([ProductsDetailsView(screen, model)], -1, name="ProductsDetails"),
        Scene([PurchaseHistoryView(screen, model)], -1, name="PurchaseHistory"),
        Scene([SellHistoryView(screen, model)], -1, name="SellHistory"),
        Scene([ReduceHistoryView(screen, model)], -1, name="ReduceHistory"),
        Scene([ImportFromEshopView(screen, model)], -1, name="ImportView"),
    ]
    screen.play(scenes, stop_on_resize=True, start_scene=scenes[0], allow_int=True)

    screen.print_at('Hello world!', 0, 0)
    screen.refresh()
    sleep(10)

if __name__ == '__main__':
    demo()