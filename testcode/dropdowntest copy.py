from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock

KV ='''
Screen

    MDDropDownItem:
        id: drop_item
        pos_hint: {'center_x': .5, 'center_y': .5}
        text: 'Item 0'
        on_release: app.show_task_type_menu()
'''


class Test(MDApp):
    task_type_menu = None
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.screen = Builder.load_string(KV)
    #     menu_items = [{"icon": "git", "text": f"Item {i}"} for i in range(5)]
    #     self.menu = MDDropdownMenu(
    #         caller=self.screen.ids.drop_item,
    #         items=menu_items,
    #         position="center",
    #         callback=self.set_item,
    #         width_mult=4,
    #     )

    def show_task_type_menu(self):
        print('opening')
        if not self.task_type_menu:
            self.task_type_menu = MDDropdownMenu(
                caller=MDApp.get_running_app().ids.drop_item,
                items = ['Homework', 'Worksheet', 'Quiz', 'Test', 'Project'],
                callback=self.set_task_type_menu,
                )
        self.task_type_menu.open()

    def set_item(self, instance):
        self.screen.ids.drop_item.set_item(instance.text)

    def build(self):
        return Builder.load_string(KV)


Test().run()