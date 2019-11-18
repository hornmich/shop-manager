'''
Created on 13. 11. 2019

@author: Michal Horn
'''

from asciimatics.widgets import Frame, Button, Layout, MultiColumnListBox, Widget, Divider
from asciimatics.exceptions import NextScene

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
        self._model.current_id = None
        raise NextScene("ProductsDetails")