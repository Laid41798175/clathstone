from client.socket_manager import client_socket
from client.config import PATH_TO_FONT, FONT_SIZE, BUTTON_BACKGROUND_COLOR
from client.popup import show_popup
from client.client_info import load_user_data

from common import ServerEnum, ServerResponse, ServerAccept, ServerDecline
from common import UserData
from common import LobbyEnum, Lobby, Cheat

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

class CheatScreen(Screen):
        
    def __init__(self, **kw):
        super().__init__(**kw)
        main_layout = BoxLayout(orientation='vertical', spacing=50, padding=(100, 300))
        
        self.cheat_input = TextInput(hint_text='cheat code',
                                     font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                                     multiline=False)
        main_layout.add_widget(self.cheat_input)

        button_layout = BoxLayout(spacing=50)

        enter_btn = Button(text='Enter',
                           font_name=PATH_TO_FONT, font_size=FONT_SIZE, 
                           background_color=BUTTON_BACKGROUND_COLOR)
        enter_btn.bind(on_press=self.cheat)
        button_layout.add_widget(enter_btn)

        lobby_btn = Button(text='Lobby',
                           font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                           background_color=BUTTON_BACKGROUND_COLOR)
        lobby_btn.bind(on_press=self.lobby)
        button_layout.add_widget(lobby_btn)

        main_layout.add_widget(button_layout)

        self.add_widget(main_layout)
    
    def cheat(self, inst):
        
        def clear_text(input: TextInput):
            input.text = ''
        
        text = self.cheat_input.text
        clear_text(self.cheat_input)
        
        request = Lobby.encode(Cheat(text))
        client_socket.sendall(request)
        
        data_received = client_socket.recv(1024)
        response : ServerAccept | ServerDecline = ServerResponse.decode(data_received)
        if response.content == ServerEnum.accept:
            show_popup(response.title, response.text)
            load_user_data(response)
        elif response.content == ServerEnum.decline:
            show_popup(response.title, response.text)
        
    def lobby(self, inst):
        self.manager.current = 'lobby'