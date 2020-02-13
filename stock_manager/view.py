'''
Created on 27. 11. 2019

@author: Michal Horn
'''

from asciimatics.widgets import Frame, Button, Layout, MultiColumnListBox, Widget, Divider, Text, Label, CheckBox, PopUpDialog, ListBox
from asciimatics.exceptions import NextScene, StopApplication
from stock_manager.model import SettingsModel


class MainMenuView(Frame):
    '''
    classdocs
    '''
    def __init__(self, screen, model):
        '''
        Constructor
        '''
        super(MainMenuView, self).__init__(screen,
                                          screen.height,
                                          screen.width,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Stock Manager",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model
        self._screen = screen

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Button("Výpis skladu         ", self._listItems))
        layout.add_widget(Button("Import dat z e-shopu ", self._importFromShop))
        layout.add_widget(Button("Započíst objednávku  ", self._acountOrder))
        layout.add_widget(Button("Nastaveni            ", self._settings))
        layout.add_widget(Button("Konec                ", self._exit))
        """self._screen.add_effect(Clock(screen, 10, 10, 5))"""

        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(MainMenuView, self).reset()
        #self.data = self._model.get_current_contact()

    def _listItems(self):
        raise NextScene("StockView")

    def _importFromShop(self):
        raise NextScene("LoadFeed")
    
    def _acountOrder(self):
        raise NextScene("LoadOrders")
    
    def _settings(self):
        raise NextScene("SettingsView")
    
    def _exit(self):
        self._model.save_settings()
        raise StopApplication('Success')

class SettingsView(Frame):
    def __init__(self, screen, model):
        super(SettingsView, self).__init__(screen,
                                          6,
                                          60,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Nastaveni",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Heureka Feer URL:", "feedUrl"))
        layout.add_widget(Text("Cesta k databazi:", "dbPath"))
        layout.add_widget(Text("Marze:", "margin"))
        layout.add_widget(Divider())
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 1)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(SettingsView, self).reset()
        self.data=self._model.settings.get_settings()
        # self.data = self._model.get_current_item()

    def _ok(self):
        self.save()
        self._model.settings = SettingsModel(feedUrl=self.data['feedUrl'], margin=self.data['margin'], dbPath=self.data['dbPath'])
        self._model.save_settings()
        raise NextScene("MainMenu")

    @staticmethod
    def _cancel():
        raise NextScene("MainMenu")

class StockView(Frame):
    '''
    classdocs
    '''

    def __init__(self, screen, model):
        '''
        Constructor
        '''
        super(StockView, self).__init__(screen,
                                          screen.height,
                                          screen.width,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Vypis skladu",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.stock.get_stock_summary(),
            name="products",
            add_scroll_bar=True,
            on_change=None,
            on_select=self._on_select)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Zpět", self._back))

        self.fix()
        self.reset()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(StockView, self).reset()
        self._reload_list()

    def _on_select(self):
        self.save()
        self._model.stock.currentId = self.data['products']
        self._scene.add_effect(PopUpDialog(self._screen, "Co se ma stat?.", ["Historie", "Nakup", "Odpis", "Upravit", "Smazat", "Zpet"], self._on_action_selected, True, u'green'))
        
    def _on_action_selected(self, action):
        if action == 0:
            self._scene.add_effect(PopUpDialog(self._screen, "Historie.", ["Nakupy", "Prodeje", "Odpisy", "Zpet"], self._on_history_selected, True, u'green'))
        elif action == 1:
            raise NextScene("AddStock")
        elif action == 2:
            raise NextScene("ReduceStock")
        elif action == 3:
            raise NextScene("EditItem")        
        elif action == 4:
            self._scene.add_effect(PopUpDialog(self._screen, "Opravdu smazat?.", ["Ano", "Ne"], self._delete_on_close, True, u'warning'))
        else :
            return

    def _on_history_selected(self, action):
        if action == 0:
            raise NextScene("PurchaseHistory")
        elif action == 1:
            raise NextScene("SellHistory")
        elif action == 2:
            raise NextScene("ReduceHistory")
        else :
            return

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.stock.get_stock_summary()
        self._list_view.value = new_value

    def _details(self):
        self.save()
        #self._model.currentId = None
        raise NextScene("ProductsDetails")
    
    def _delete(self):
        self.save()
        self._model.stock.currentId = self.data["products"]
        self._scene.add_effect(PopUpDialog(self._screen, "Opravdu smazat?.", ["Ano", "Ne"], self._delete_on_close, True, u'warning'))
        
    def _delete_on_close(self, selected):
        if selected == 0:
            self._model.stock.delete_item()
        self._reload_list()
        
    def _back(self):
        self.save()
        self._model.currentId = None
        raise NextScene("MainMenu")            

class AddStockView(Frame):
    def __init__(self, screen, model):
        super(AddStockView, self).__init__(screen,
                                          7,
                                          60,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Zadat sklad",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Počet kusů:", "count"))
        layout.add_widget(Text("Nákupní cena:", "price"))
        layout.add_widget(Text("Místo nákupu:", "shop"))
        layout.add_widget(Divider())
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 1)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(AddStockView, self).reset()
        # self.data = self._model.get_current_stock_item()

    def _ok(self):
        self.save()
        self._model.stock.add_purchased_item(self.data['count'], self.data['price'], self.data['shop'])
        raise NextScene("StockView")

    @staticmethod
    def _cancel():
        raise NextScene("StockView")

class ReduceStockView(Frame):
    def __init__(self, screen, model):
        super(ReduceStockView, self).__init__(screen,
                                          6,
                                          60,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Odepsat zboží",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Počet kusů:", "count"))
        layout.add_widget(Text("Důvod:", "reason"))
        layout.add_widget(Divider())
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 1)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(ReduceStockView, self).reset()
        # self.data = self._model.get_current_item()

    def _ok(self):
        self.save()
        self._model.stock.reduce_item(self.data['count'], self.data['reason'])
        raise NextScene("StockView")

    @staticmethod
    def _cancel():
        raise NextScene("StockView")

class PurchaseHistoryView(Frame):
    def __init__(self, screen, model):
        super(PurchaseHistoryView, self).__init__(screen,
                                          screen.height,
                                          screen.width,
                                          on_load=self._reload_list,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Historie nákupů",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._list_view = MultiColumnListBox(
            height=Widget.FILL_FRAME,
            options=model.stock.get_purchase_history(),
            columns=("25%", "25%", "25%", "25%"),
            titles=("Datum", "Ks.", "Cena", "Misto"),
            name="purchases",
            add_scroll_bar=True,
            on_change=None,
            on_select=None)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Zpět", self._back))

        self.fix()

#    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
#        super(PurchaseHistoryView, self).reset()
#        self.data = self._model.stock.get_purchase_history()

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.stock.get_purchase_history()
        self._list_view.value = new_value
        
    def _back(self):
        self.save()
        self._model.currentId = None
        raise NextScene("StockView")
  
class ReduceHistoryView(Frame):
    def __init__(self, screen, model):
        super(ReduceHistoryView, self).__init__(screen,
                                          screen.height,
                                          screen.width,
                                          on_load=self._reload_list,
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
            options=model.stock.get_reduce_history(),
            columns=("33%", "33%", "33%"),
            titles=("Datum", "Ks.", "Duvod"),
            name="reduces",
            add_scroll_bar=True,
            on_change=None,
            on_select=None)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Zpět", self._back))

        self.fix()

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.stock.get_reduce_history()
        self._list_view.value = new_value
        
    def _back(self):
        self.save()
        self._model.currentId = None
        raise NextScene("StockView")

class SellHistoryView(Frame):
    def __init__(self, screen, model):
        super(SellHistoryView, self).__init__(screen,
                                          screen.height,
                                          screen.width,
                                          on_load=self._reload_list,
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
            options=model.stock.get_sell_history(), 
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
        
    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.stock.get_sell_history()
        self._list_view.value = new_value
        
    def _back(self):
        self.save()
        self._model.currentId = None
        raise NextScene("StockView")
    
class LoadFeedView(Frame):
    '''
    classdocs
    '''
    def __init__(self, screen, model):
        '''
        Constructor
        '''
        super(LoadFeedView, self).__init__(screen,
                                          5,
                                          60,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Nahrat XML feed",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model
        self._screen = screen

        # Create the form for displaying the list of contacts.
        layout = Layout([2], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Adresa XML:", "xmlUrl"))
        layout.add_widget(Divider())
        layout2=Layout([1,1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Nacist", self._load), 0)
        layout2.add_widget(Button("Zpet", self._back), 1)

        self.reset()
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(LoadFeedView, self).reset()
        #self.data = self._model.get_current_contact()

    def _load(self):
        self.save()
        try:
            self._model.xmlFeed.load(url=self.data["xmlUrl"])
        except Exception as e:
            self._scene.add_effect(PopUpDialog(self._screen, "Nelze nacist: "+str(e), ["OK"], self._on_error, True, u'warning'))
        else:
            raise NextScene("ProcessFeed")

    def _on_error(self, btn):
        raise NextScene("MainMenu")        
    
    def _back(self):
        self.save()
        self._model.currentId = None
        raise NextScene("MainMenu")
    
class ProcessXMLFeedView(Frame):
    def __init__(self, screen, model):
        super(ProcessXMLFeedView, self).__init__(screen,
                                          screen.height,
                                          screen.width,
                                          on_load=self._reload_list,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Aplikovat zmeny",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._list_view = MultiColumnListBox(
            height=Widget.FILL_FRAME,
            options=model.xmlFeed.get_actions(), 
            columns=("50%", "50%"),
            titles=("Produkt", "Akce"),
            name="actions",
            add_scroll_bar=True,
            on_change=None,
            on_select=self._on_select)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Aplikovat vse", self._apply_all), 0)
        layout2.add_widget(Button("Zpět", self._back), 1)


        self.fix()
        
    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.xmlFeed.get_actions()
        self._list_view.value = new_value
        
    def _on_select(self):
        self.save()
        self._model.xmlFeed.currentActionId = self.data['actions']
        self._scene.add_effect(PopUpDialog(self._screen, "Co se ma stat?.", ["Provest", "Ignorovat", "Zpet"], self._on_action_selected, True, u'green'))

    def _on_action_selected(self, action):
        if action == 0:
            self._model.xmlFeed.apply_selected()
            self._reload_list()
        elif action == 1:
            self._model.xmlFeed.ignore_selected()
            self._reload_list()
        else :
            return
    def _apply_all(self):
        self.save()
        self._model.xmlFeed.currentActionId = None
        self._model.xmlFeed.apply_all()    
        self._scene.add_effect(PopUpDialog(self._screen, "Vsechy polozky se aktualizovaly.", ["OK"], None, True, u'green'))

    def _back(self):
        self.save()
        self._model.xmlFeed.currentActionId = None
        raise NextScene("MainMenu")

class LoadOrdersView(Frame):
    '''
    classdocs
    '''
    def __init__(self, screen, model):
        '''
        Constructor
        '''
        super(LoadOrdersView, self).__init__(screen,
                                          5,
                                          60,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Importovat objednavky",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model
        self._screen = screen

        # Create the form for displaying the list of contacts.
        layout = Layout([2], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Adresa XML:", "xmlUrl"))
        layout.add_widget(Divider())
        layout2=Layout([1,1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Nacist", self._load), 0)
        layout2.add_widget(Button("Zpet", self._back), 1)

        self.reset()
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(LoadOrdersView, self).reset()
        #self.data = self._model.get_current_contact()

    def _load(self):
        self.save()
        try:
            self._model.orders.load(url=self.data["xmlUrl"])
        except Exception as e:
            self._scene.add_effect(PopUpDialog(self._screen, "Nelze nacist: "+str(e), ["OK"], self._on_error, True, u'warning'))
        else:
            raise NextScene("ProcessOrders")

    def _on_error(self, btn):
        raise NextScene("MainMenu")        
    
    def _back(self):
        self.save()
        self._model.currentId = None
        raise NextScene("MainMenu")
    
class ProcessOrdersView(Frame):
    def __init__(self, screen, model):
        super(ProcessOrdersView, self).__init__(screen,
                                          screen.height,
                                          screen.width,
                                          on_load=self._reload_list,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Zauctovat objednavky",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._list_view = MultiColumnListBox(
            height=Widget.FILL_FRAME,
            options=model.orders.get_orders(), 
            columns=("25%", "25%", "25%", "25%"),
            titles=("ID", "Datum", "Stav", "Celkova cena"),
            name="actions",
            add_scroll_bar=True,
            on_change=None,
            on_select=self._on_select)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Zauctovat vse", self._apply_all), 0)
        layout2.add_widget(Button("Zpět", self._back), 1)

        self.fix()
        
    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.orders.get_orders()
        self._list_view.value = new_value
        
    def _on_select(self):
        self.save()
        self._model.orders.currentOrderId = self.data['actions']
        self._scene.add_effect(PopUpDialog(self._screen, "Co se ma stat?.", ["Zauctovat", "Ignorovat", "Detaily", "Zpet"], self._on_action_selected, True, u'green'))

    def _on_action_selected(self, action):
        if action == 0:
            try:
                self._model.orders.apply_selected()
            except Exception as exc: 
                self._scene.add_effect(PopUpDialog(self._screen, str(exc), ["OK"], None, True, u'warning'))
            self._reload_list()
        elif action == 1:
            self._model.orders.ignore_selected()
            self._reload_list()
        else :
            return

    def _apply_all(self):
        self.save()
        self._model.orders.currentOrderId = None
        self._model.orders.apply_all()    
        self._scene.add_effect(PopUpDialog(self._screen, "Vsechy objednavky zauctovany.", ["OK"], None, True, u'green'))

    def _back(self):
        self.save()
        self._model.orders.currentOrderId = None
        raise NextScene("MainMenu")    
    