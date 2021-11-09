from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from kivymd.icon_definitions import md_icons
from kivymd.uix.tab import MDTabsBase

demo = """
BoxLayout:
    orientation: 'vertical'

    MDToolbar:
        title: app.title
        md_bg_color: app.theme_cls.primary_color
        background_palette: 'Primary'
        left_action_items: [['menu', lambda x: x]]

    MDTabs:
        id: android_tabs
        MyTab:
            text: 'Current Homework'
        MyTab:
            text: 'Archived Homework'
"""

if __name__ == '__main__':
    from kivy.factory import Factory
    from kivymd.uix.button import MDIconButton


    class MyTab(BoxLayout, MDTabsBase):
        pass


    class ExampleApp(MDApp):
        title = 'Example Tabs'

        def build(self):
            self.root = Builder.load_string(demo)

    ExampleApp().run()

