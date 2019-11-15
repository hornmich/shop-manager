'''
Created on 13. 11. 2019

@author: Michal Horn
'''

from asciimatics.widgets import Frame, Button, Layout, Text, Divider
from asciimatics.exceptions import NextScene

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
        # self._model.update_current_contact(self.data)
        raise NextScene("StockView")

    @staticmethod
    def _cancel():
        raise NextScene("StockView")

