'''
Created on 13. 10. 2019

@author: michal
'''

from asciimatics.screen import ManagedScreen
from asciimatics.scene import Scene

from stock_manager.view import MainMenuView, StockView, AddStockView, ReduceStockView, PurchaseHistoryView, SellHistoryView, ReduceHistoryView, LoadFeedView, ProcessXMLFeedView, LoadOrdersView, ProcessOrdersView, SettingsView, EditItemView 
from stock_manager.model import DataModel


from time import sleep
from stock_manager.loaders import HeurekaXMLLoader, EshopRychleOrdersLoader

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
    xmlLoader = HeurekaXMLLoader()
    orderLoader = EshopRychleOrdersLoader()
    model = DataModel(xmlLoader, orderLoader)
    scenes = [
        Scene([MainMenuView(screen, model)], -1, name="MainMenu"),
        Scene([SettingsView(screen, model)], -1, name="SettingsView"),
        Scene([LoadOrdersView(screen, model)], -1, name="LoadOrders"),
        Scene([ProcessOrdersView(screen, model)], -1, name="ProcessOrders"),
        Scene([StockView(screen, model)], -1, name="StockView"),
        Scene([AddStockView(screen, model)], -1, name="AddStock"),
        Scene([EditItemView(screen, model)], -1, name="EditItem"),
        Scene([ReduceStockView(screen, model)], -1, name="ReduceStock"),
        Scene([PurchaseHistoryView(screen, model)], -1, name="PurchaseHistory"),
        Scene([SellHistoryView(screen, model)], -1, name="SellHistory"),
        Scene([ReduceHistoryView(screen, model)], -1, name="ReduceHistory"),
        Scene([LoadFeedView(screen, model)], -1, name="LoadFeed"),
        Scene([ProcessXMLFeedView(screen, model)], -1, name="ProcessFeed"),
    ]
    screen.play(scenes, stop_on_resize=True, start_scene=scenes[0], allow_int=True)

    screen.print_at('Hello world!', 0, 0)
    screen.refresh()
    sleep(10)

if __name__ == '__main__':
    demo()