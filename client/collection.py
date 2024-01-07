from client.socket_manager import client_socket
from client.config import PATH_TO_FONT, FONT_SIZE, BUTTON_BACKGROUND_COLOR
from client.popup import show_popup
from client.client_info import user_data, load_user_data

from common import ServerEnum, ServerResponse, ServerAccept, ServerDecline
from common import UserData

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

class CollectionScreen(Screen):
        
    def __init__(self, **kw):
        super().__init__(**kw)
        
        # TODO
        # Collections