from client.socket_manager import client_socket
from client.popup import show_popup
from client.config import PATH_TO_FONT, FONT_SIZE, BUTTON_BACKGROUND_COLOR

from common import Lobby, LobbyEnum, Register

from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

class RegisterScreen(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        
        main_layout = BoxLayout(orientation='vertical', spacing=50, padding=(100, 100))

        self.id_input = TextInput(hint_text='ID',
                                  font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                                  multiline=False)
        main_layout.add_widget(self.id_input)

        self.pw_input = TextInput(hint_text='Password',
                                  font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                                  password=True, multiline=False)
        main_layout.add_widget(self.pw_input)
        
        self.confirm_pw_input = TextInput(hint_text='Confirm Password',
                                          font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                                          password=True, multiline=False)
        main_layout.add_widget(self.confirm_pw_input)
        
        self.nickname_input = TextInput(hint_text='Nickname',
                                        font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                                        multiline=False)
        main_layout.add_widget(self.nickname_input)
        
        self.testkey_input = TextInput(hint_text='Test Key',
                                       font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                                       multiline=False)
        main_layout.add_widget(self.testkey_input)

        ok_btn = Button(text='Register',
                        font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                        background_color=BUTTON_BACKGROUND_COLOR)
        ok_btn.bind(on_press=self.check_validity)
        main_layout.add_widget(ok_btn)
        
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
        confirm_pw = self.confirm_pw_input.text
        nickname = self.nickname_input.text
        testkey = self.testkey_input.text
        
        if not check_text_validity(loginid):
            clear_text(self.id_input)
            show_popup("Invalid ID", "Your ID must be 4~16 alphanumeric characters.")
            return
        if not check_text_validity(loginpw):
            clear_text(self.pw_input)
            show_popup("Invalid Password", "Your Password must be 4~16 alphanumeric characters.")
            return
        if loginpw != confirm_pw:
            clear_text(self.pw_input)
            clear_text(self.confirm_pw_input)
            show_popup("Cannot confirm Password", "Please confirm your Password.")
            return
        if not check_text_validity(nickname):
            clear_text(self.nickname_input)
            show_popup("Invalid Nickname", "Your Nickname must be 4~16 alphanumeric characters.")
            return
        
        request = Lobby.encode(Register(loginid, loginpw, nickname, testkey))
        client_socket.sendall(request)