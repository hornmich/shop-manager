'''
Created on 13. 11. 2019

@author: Michal Horn
'''

from asciimatics.widgets import Frame, Button, Layout, ListBox, Widget, Divider
from asciimatics.exceptions import NextScene

class ProductsDetailsView(Frame):
    def __init__(self, screen, model):
        super(ProductsDetailsView, self).__init__(screen,
                                          screen.height,
                                          screen.width,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Detaily produktu",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model
        self._purchase_history_btn = Button("Historie nákupů", self._purchase_history)
        self._sell_history_btn = Button("Historie prodejů", self._sell_history)
        self._reduce_history_btn = Button("Historie odpisů", self._reduce_history)

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.get_summary(),
            name="Products",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=None)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(self._purchase_history_btn ,0)
        layout2.add_widget(self._sell_history_btn, 1)
        layout2.add_widget(self._reduce_history_btn, 2)
        layout2.add_widget(Button("Zpět", self._back), 3)

        self.fix()
        self._on_pick()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(ProductsDetailsView, self).reset()
        #self.data = self._model.get_current_contact()

    def _on_pick(self):
        self._purchase_history_btn.disabled = self._list_view.value is None
        self._sell_history_btn.disabled = self._list_view.value is None
        self._reduce_history_btn.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_summary()
        self._list_view.value = new_value

    def _purchase_history(self):
        self._model.current_id = None
        raise NextScene("PurchaseHistory")

    def _sell_history(self):
        self.save()
        self._model.current_id = None
        raise NextScene("SellHistory")
   
    def _reduce_history(self):
        self.save()
        self._model.current_id = None
        raise NextScene("ReduceHistory")
        
    def _back(self):
        self.save()
        self._model.current_id = None
        raise NextScene("MainMenu")