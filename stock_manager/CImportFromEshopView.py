'''
Created on 14. 11. 2019

@author: eaton
'''

from asciimatics.widgets import Frame, Button, Layout, Text, Label, PopUpDialog,\
    CheckBox, Divider
from asciimatics.exceptions import NextScene

class ImportFromEshopView(Frame):
    '''
    classdocs
    '''
    def __init__(self, screen, model):
        '''
        Constructor
        '''
        super(ImportFromEshopView, self).__init__(screen,
                                          10,
                                          60,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Import profuktu",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model
        self._screen = screen

        # Create the form for displaying the list of contacts.
        layout = Layout([2], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Adresa XML:", "xmlUrl"))
        layout.add_widget(Label(""))
        layout.add_widget(CheckBox("Smazat vsechny chybejici.", "Smazat vsechny", "deleteAll"))
        layout.add_widget(CheckBox("Pridat vsechny nove (0 na sklade).", "Pridat vsechny", "addAll"))
        layout.add_widget(CheckBox("Jen zobrazit zmeny.", "Zobrazit zmeny", "dryRun"))
        layout.add_widget(Divider())
        layout2=Layout([1,1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Nacist", self._load), 0)
        layout2.add_widget(Button("Zpet", self._back), 1)

        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(ImportFromEshopView, self).reset()
        #self.data = self._model.get_current_contact()

    def _load(self):
        self._scene.add_effect(PopUpDialog(self._screen, "Nelze nacist.", ["OK"], None, True, u'warning'))
    
    def _back(self):
        self.save()
        self._model.current_id = None
        raise NextScene("MainMenu")