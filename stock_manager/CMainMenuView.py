'''
Created on 13. 11. 2019

@author: eaton
'''

from asciimatics.widgets import Frame, Button, Layout
from asciimatics.exceptions import NextScene


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

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Button("Výpis skladu       ", self._listItems))
        layout.add_widget(Button("Import z e-shopu   ", self._importFromShop))
        layout.add_widget(Button("Započíst objednávku", self._acountOrder))
        layout.add_widget(Button("Nastaveni          ", self._settings))
        layout.add_widget(Button("Konec              ", None))

        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(MainMenuView, self).reset()
        #self.data = self._model.get_current_contact()

    def _listItems(self):
        raise NextScene("StockView")

    def _importFromShop(self):
        raise NextScene("StockView")
    
    def _acountOrder(self):
        raise NextScene("StockView")
    
    def _settings(self):
        raise NextScene("StockView")
       