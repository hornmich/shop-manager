'''
Created on 13. 11. 2019

@author: Michal Horn <michal@apartman.cz>
'''

from asciimatics.widgets import Frame, Button, Layout, ListBox, Divider, Widget
from asciimatics.exceptions import NextScene

class StockView(Frame):
    '''
    classdocs
    '''

    def __init__(self, screen, model):
        '''
        Constructor
        '''
        super(StockView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Stock View",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model
        self._delete_btn = Button("Smazat", self._delete)
        self._add_btn = Button("Zadat", self._add)
        self._account_btn = Button("Odepsat", self._account)
        self._details_btn = Button("Detaily", self._details)


        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.stock.get_stock_summary(),
            name="Stock",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._details)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(self._details_btn, 0)
        layout2.add_widget(self._add_btn, 1)
        layout2.add_widget(self._account_btn, 2)
        layout2.add_widget(self._delete_btn, 3)
        layout2.add_widget(Button("Zpět", self._back), 4)

        self.fix()
        self._on_pick()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(StockView, self).reset()
        #self.data = self._model.get_current_contact()

    def _on_pick(self):
        self._delete_btn.disabled = self._list_view.value is None
        self._add_btn.disabled = self._list_view.value is None
        self._account_btn.disabled = self._list_view.value is None
        self._details_btn.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.stock.get_stock_summary()
        self._list_view.value = new_value

    def _add(self):
        self._model.current_id = None
        raise NextScene("AddStock")

    def _account(self):
        self.save()
        self._model.current_id = None
        raise NextScene("ReduceStock")
   
    def _details(self):
        self.save()
        self._model.current_id = None
        raise NextScene("ProductsDetails")
    
    def _delete(self):
        self.save()
        #self._model.delete_contact(self.data["contacts"])
        self._reload_list()
        
    def _back(self):
        self.save()
        self._model.current_id = None
        raise NextScene("MainMenu")
            