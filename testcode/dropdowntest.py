from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock

KV = '''
<NewTaskPage>
    NewDropDown:
        id: drop_item
        pos_hint: {'center_x': .9, 'center_y': .5}
        text: 'Item 0'
        on_release: app.menu.open()
'''


class NewTaskPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        menu_items = [{"icon": "git", "text": f"Item {i}"} for i in range(5)]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.drop_item,
            items=menu_items,
            position="center",
            callback=self.set_item,
            width_mult=4,
        )
    
    def set_item(self, instance):
        self.screen.ids.drop_item.set_item(instance.text)



class Test(MDApp):
    menu = None


    def build(self):
        return NewTaskPage()


Test().run()