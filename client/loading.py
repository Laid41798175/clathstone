import os

from client.socket_manager import client_socket
from client.popup import show_popup
from client.config import PATH_TO_FONT, FONT_SIZE, BUTTON_BACKGROUND_COLOR
from client.config import SERVER_IP

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

class LoadingScreen(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        
        layout = FloatLayout()
        bg_image = Image(source=os.path.join('images', 'loading.jpg'), allow_stretch=True)
        layout.add_widget(bg_image)
        self.add_widget(layout)

        btn = Button(text='Connect', size_hint=(.3, .1),
                     font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                     pos_hint={'center_x': .5, 'center_y': .25},
                     background_color=BUTTON_BACKGROUND_COLOR)
        btn.bind(on_press=self.connect_server)
        self.add_widget(btn)

    def connect_server(self, inst):
        connect, title, text = self.client_connect()
        show_popup(title, text)
        if not connect:
            client_socket.close()
            os._exit(1)
        
        self.manager.current = 'login'
        
    def client_connect(self) -> (bool, str, str):    
        try:
            # client_socket.connect((SERVER_IP, 12345))
            client_socket.connect(('localhost', 12345))
            return (True, "Connection Success", "Connected to the server!")
        except ConnectionRefusedError:
            return (False, "Connection Failed", "Server is currently closed. Please retry next time :)")