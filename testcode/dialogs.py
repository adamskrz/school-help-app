from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView

from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDTextButton
from kivymd.uix.textfield import MDTextField, MDTextFieldRect
from kivymd.theming import ThemableBehavior
from kivymd import images_path
from kivymd.material_resources import DEVICE_IOS
from kivymd.uix.dialog import BaseDialog
from kivymd.app import MDApp
from kivy.factory import Factory
from kivymd.uix.dialog import MDInputDialog, MDDialog
from kivy.utils import get_hex_from_color

class MainApp(MDApp):

    def build(self):
        return Builder.load_file('dialogs.kv')

    def callback_for_menu_items(self, *args):
        from kivymd.toast.kivytoast import toast

        toast(args[0])

    def show_example_input_dialog(self):
        dialog = MDHWInputDialog()
        dialog.open()
    
    def show_example_okcancel_dialog(self):
        dialog = MDDialog(
            title="Title",
            size_hint=(0.8, 0.3),
            text_button_ok="Yes",
            text="Your [color=%s][b]text[/b][/color] dialog"
            % get_hex_from_color(self.theme_cls.primary_color),
            text_button_cancel="Cancel",
            events_callback=self.callback_for_menu_items,
        )
        dialog.open()

class MDHWInputDialog(BaseDialog):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.content_dialog = ContentHWInputDialog()
        self.add_widget(self.content_dialog)
        self.set_content(self.content_dialog)
        Clock.schedule_once(self.set_field_focus, 0.5)