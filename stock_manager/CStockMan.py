'''
Created on 13. 10. 2019

@author: michal
'''

from asciimatics.screen import ManagedScreen
from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, Button, TextBox, Widget,\
    MultiColumnListBox
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication

from stock_manager.CMainMenuView import MainMenuView
from stock_manager.CStockView import StockView
from stock_manager.CAddStockView import AddStockView
from stock_manager.CReduceStockView import ReduceStockView
from stock_manager.CProductsDetailsView import ProductsDetailsView
from stock_manager.CPurchaseHistoryView import PurchaseHistoryView

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





    
class SellHistoryView(Frame):
    def __init__(self, screen, model):
        super(SellHistoryView, self).__init__(screen,
                                          screen.height,
                                          screen.width,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Historie prodejů",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._list_view = MultiColumnListBox(
            height=Widget.FILL_FRAME,
            options=model.get_summary(),
            columns=("50%", "50%"),
            titles=("Datum", "Ks."),
            name="Sales",
            add_scroll_bar=True,
            on_change=None,
            on_select=None)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Zpět", self._back))

        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(SellHistoryView, self).reset()
        #self.data = self._model.get_current_contact()

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_summary()
        self._list_view.value = new_value
        
    def _back(self):
        self.save()
        self._model.current_id = None
        raise NextScene("ProductsDetails")
    
class ReduceHistoryView(Frame):
    def __init__(self, screen, model):
        super(ReduceHistoryView, self).__init__(screen,
                                          screen.height,
                                          screen.width,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Historie odpisů",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._list_view = MultiColumnListBox(
            height=Widget.FILL_FRAME,
            options=model.get_summary(),
            columns=("33%", "33%", "33%"),
            titles=("Datum", "Ks.", "Duvod"),
            name="Purchases",
            add_scroll_bar=True,
            on_change=None,
            on_select=None)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Zpět", self._back))

        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(ReduceHistoryView, self).reset()
        #self.data = self._model.get_current_contact()

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_summary()
        self._list_view.value = new_value
        
    def _back(self):
        self.save()
        self._model.current_id = None
        raise NextScene("ProductsDetails")
    
@ManagedScreen
def demo(screen=None):
    model = StockModel()
    scenes = [
        Scene([MainMenuView(screen, None)], -1, name="MainMenu"),
        Scene([StockView(screen, model)], -1, name="StockView"),
        Scene([AddStockView(screen, model)], -1, name="AddStock"),
        Scene([ReduceStockView(screen, model)], -1, name="ReduceStock"),
        Scene([ProductsDetailsView(screen, model)], -1, name="ProductsDetails"),
        Scene([PurchaseHistoryView(screen, model)], -1, name="PurchaseHistory"),
        Scene([SellHistoryView(screen, model)], -1, name="SellHistory"),
        Scene([ReduceHistoryView(screen, model)], -1, name="ReduceHistory"),
    ]
    screen.play(scenes, stop_on_resize=True, start_scene=scenes[0], allow_int=True)

    screen.print_at('Hello world!', 0, 0)
    screen.refresh()
    sleep(10)

if __name__ == '__main__':
    demo()