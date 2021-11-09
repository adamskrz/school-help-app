from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    ObjectProperty,
    StringProperty,
    NumericProperty,
    ListProperty,
    OptionProperty,
    BooleanProperty,
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

import kivymd.material_resources as m_res
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.button import MDIconButton
from kivymd.theming import ThemableBehavior
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.list import MDList
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import ILeftBody
from kivymd.uix.list import IRightBodyTouch

class ContactPhoto(ILeftBody):
    source = StringProperty()
    pass

class MessageButton(IRightBodyTouch, MDIconButton):
    phone_number = StringProperty()

    def on_release(self):
        # sample code:
        #Dialer.send_sms(phone_number, "Hey! What's up?")
        pass

# Sets up ScrollView with MDList, as normally used in Android:
sv = ScrollView()
ml = MDList()
sv.add_widget(ml)

contacts = [
    ["Annie", "555-24235", "http://myphotos.com/annie.png"],
    ["Bob", "555-15423", "http://myphotos.com/bob.png"],
    ["Claire", "555-66098", "http://myphotos.com/claire.png"]
]

for c in contacts:
    item = TwoLineAvatarIconListItem(
        text=c[0],
        secondary_text=c[1]
    )
    item.add_widget(ContactPhoto(source=c[2]))
    item.add_widget(MessageButton(phone_number=c[1]))
    ml.add_widget(item)