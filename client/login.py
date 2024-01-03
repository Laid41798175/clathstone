from client.socket_manager import client_socket
from client.config import PATH_TO_FONT, FONT_SIZE, BUTTON_BACKGROUND_COLOR
from client.popup import show_popup

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
        
        # ID 입력 필드
        self.id_input = TextInput(hint_text='ID',
                                  font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                                  multiline=False)
        main_layout.add_widget(self.id_input)

        # 비밀번호 입력 필드
        self.pw_input = TextInput(hint_text='Password',
                                  font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                                  password=True, multiline=False)
        main_layout.add_widget(self.pw_input)

        # 버튼들을 위한 수평 BoxLayout입니다.
        button_layout = BoxLayout(spacing=50)

        # 'Log in' 버튼
        login_btn = Button(text='Log in',
                           font_name=PATH_TO_FONT, font_size=FONT_SIZE, 
                           background_color=BUTTON_BACKGROUND_COLOR)
        login_btn.bind(on_press=self.login)
        button_layout.add_widget(login_btn)

        # 'Register' 버튼
        register_btn = Button(text='Register',
                              font_name=PATH_TO_FONT, font_size=FONT_SIZE, 
                              background_color=BUTTON_BACKGROUND_COLOR)
        register_btn.bind(on_press=self.register)
        button_layout.add_widget(register_btn)

        # 버튼 레이아웃을 메인 레이아웃에 추가합니다.
        main_layout.add_widget(button_layout)

        # 메인 레이아웃을 화면에 추가합니다.
        self.add_widget(main_layout)
    
    def login(self, inst):
        loginid = self.id_input.text
        loginpw = self.pw_input.text
        request = Lobby.encode(Login(loginid, loginpw))
        client_socket.sendall(request)

        data_received = client_socket.recv(1024)
        response : ServerAccept | ServerDecline = ServerResponse.decode(data_received)
        if response.content == ServerEnum.accept:
            show_popup(response.title, response.text)
            self.manager.current = 'lobby'
        elif response.content == ServerEnum.decline:
            show_popup(response.title, response.text)
        else: # unexpected error
            pass
            
    def register(self, inst):
        self.manager.current = 'register'