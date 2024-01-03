from client.config import PATH_TO_FONT, FONT_SIZE, BUTTON_BACKGROUND_COLOR

from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

def show_popup(title: str, text: str):
    layout = BoxLayout(orientation='vertical', padding=10)
    popup_label = Label(text=text)
    layout.add_widget(popup_label)
        
    ok_btn = Button(text='OK',
                    size_hint_y=None, height=50)
    layout.add_widget(ok_btn)
        
    popup = Popup(title=title, content=layout,
                  size_hint=(None, None), size=(800, 400))

    ok_btn.bind(on_press=popup.dismiss)
    popup.open()