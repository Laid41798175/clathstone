from client.socket_manager import client_socket
from client.config import PATH_TO_FONT, FONT_SIZE, BUTTON_BACKGROUND_COLOR
from client.popup import show_popup
from client.client_info import load_user_data

from common import ServerEnum, ServerResponse, ServerAccept, ServerDecline
from common import LobbyEnum, Lobby, Login

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

class LoginScreen(Screen):
        
    def __init__(self, **kw):
        super().__init__(**kw)
        main_layout = BoxLayout(orientation='vertical', spacing=50, padding=(100, 300))
        
        self.id_input = TextInput(hint_text='ID',
                                  font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                                  multiline=False)
        main_layout.add_widget(self.id_input)

        self.pw_input = TextInput(hint_text='Password',
                                  font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                                  password=True, multiline=False)
        main_layout.add_widget(self.pw_input)

        button_layout = BoxLayout(spacing=50)

        login_btn = Button(text='Log in',
                           font_name=PATH_TO_FONT, font_size=FONT_SIZE, 
                           background_color=BUTTON_BACKGROUND_COLOR)
        login_btn.bind(on_press=self.check_validity)
        button_layout.add_widget(login_btn)

        register_btn = Button(text='Register',
                              font_name=PATH_TO_FONT, font_size=FONT_SIZE, 
                              background_color=BUTTON_BACKGROUND_COLOR)
        register_btn.bind(on_press=self.register)
        button_layout.add_widget(register_btn)

        main_layout.add_widget(button_layout)

        self.add_widget(main_layout)
 
    def check_validity(self, inst):
        
        def check_text_validity(text: str) -> bool:
            if not text.isalnum():
                return False
            if 4 <= len(text) <= 16:
                return True
            return False
        
        def clear_text(input: TextInput):
            input.text = ''

        loginid = self.id_input.text
        loginpw = self.pw_input.text
        
        if not check_text_validity(loginid):
            clear_text(self.id_input)
            show_popup("Invalid ID", "Your ID must be 4~16 alphanumeric characters.")
            return
        if not check_text_validity(loginpw):
            clear_text(self.pw_input)
            show_popup("Invalid Password", "Your Password must be 4~16 alphanumeric characters.")
            return
        
        self.login(self, loginid, loginpw)
        
    def login(self, loginid: str, loginpw: str):
        request = Lobby.encode(Login(loginid, loginpw))
        client_socket.sendall(request)

        data_received = client_socket.recv(1024)
        response : ServerAccept | ServerDecline = ServerResponse.decode(data_received)
        if response.content == ServerEnum.accept:
            show_popup(response.title, response.text)
            load_user_data(response)
            self.manager.current = 'lobby'
        elif response.content == ServerEnum.decline:
            show_popup(response.title, response.text)
    
    def register(self, inst):
        self.manager.current = 'register'