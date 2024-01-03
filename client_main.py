from client import client_socket
from client import LoadingScreen, LoginScreen, RegisterScreen, LobbyScreen
import threading
import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

class Clathstone(App):
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoadingScreen(name='loading'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(LobbyScreen(name='lobby'))
        # sm.add_widget(CollectionScreen(name='collection'))
        # sm.add_widget(PlayScreen(name='play'))
        # sm.add_widget(GameScreen(name='game'))
        
        return sm

# Running the app
if __name__ == '__main__':
    Clathstone().run()