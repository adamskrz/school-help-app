from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemeManager


class MyLayout(BoxLayout):

    scr_mngr = ObjectProperty(None)

    def check_data_login(self):
        username = self.scr_mngr.screen1.username.text
        password = self.scr_mngr.screen1.password.text

        print(username)
        print(password)

        if username == "KivyMD" and password == "kivy":
            self.change_screen("screen2")

    def change_screen(self, screen, *args):
        self.scr_mngr.current = screen


KV = """

#:import MDToolbar kivymd.uix.toolbar
#:import ThemeManager kivymd.theming.ThemeManager
#:import MDTextField kivymd.uix.textfield.MDTextField
#:import MDCard kivymd.uix.card.MDCard
#:import MDSeparator kivymd.uix.card.MDSeparator
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import colors kivymd.color_definitions.colors

#:import partial functools.partial

MyLayout:
    scr_mngr: scr_mngr
    orientation: 'vertical'

    ScreenManager:
        id: scr_mngr
        screen1: screen1

        Screen:
            id: screen1
            name: 'screen1'
            username: username
            password: password

            MDCard:
                size_hint: None, None
                size: dp(520), dp(340)
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}

                BoxLayout:
                    orientation:'vertical'
                    padding: dp(20)
                    spacing:20

                    MDLabel:
                        text: 'Connexion'
                        theme_text_color: 'Secondary'
                        font_style:"H2"
                        size_hint_y: None
                        height: dp(36)

                    MDSeparator:
                        height: dp(1)

                    MDTextField:
                        id: username
                        hint_text: "Username "
                        helper_text_mode: "on_focus"

                    MDTextField:
                        id: password
                        hint_text: "Password "
                        helper_text_mode: "on_focus"
                        password: True

                    MDFlatButton:
                        text: "Connexion"
                        pos_hint: {'center_x': 0.5}
                        on_release: root.check_data_login()
        Screen:
            name: 'screen2'

            MDToolbar:
                id: toolbar
                title: "Welcome ! "
                pos_hint: {'center_x': 0.5, 'center_y': 0.97}
                md_bg_color: app.theme_cls.primary_color
                background_palette: 'DeepPurple'
                background_hue: 'A400'
                left_action_items: [['arrow-left', partial(root.change_screen, 'screen1') ]]
                right_action_items: [['animation', lambda x: MDThemePicker().open()]]

            MDLabel:
                font_style: 'H2'
                theme_text_color: 'Primary'
                text: "Data :"
                height: self.texture_size[1] + dp(3)
                halign: 'center'
                pos_hint: {'center_x': 0.5, 'center_y': 0.85}
"""


class MyApp(MDApp):
    title = "Kivy MD Demo"

    def build(self):
        return Builder.load_string(KV)


MyApp().run()