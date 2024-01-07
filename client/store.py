from client.socket_manager import client_socket
from client.config import PATH_TO_FONT, FONT_SIZE, BUTTON_BACKGROUND_COLOR, LABEL_TEXT_COLOR
from client.popup import show_popup
from client.client_info import user_data

from common import ServerEnum, ServerResponse, ServerAccept, ServerDecline
from common import UserData
from common import LobbyEnum, Lobby, Cheat
from common import CardPack

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

from functools import partial

CARDPACK_PRICE = 100

class StoreScreen(Screen):
        
    def __init__(self, **kw):
        super().__init__(**kw)
        main_layout = BoxLayout(orientation='vertical', spacing=50, padding=(100, 300))
        
        # self.cheat_input = TextInput(hint_text='cheat code',
        #                           font_name=PATH_TO_FONT, font_size=FONT_SIZE,
        #                           multiline=False)
        # main_layout.add_widget(self.cheat_input)

        button_layout = BoxLayout(spacing=50)

        purchase_btn = Button(text='Purchase', 
                              font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                              background_color=BUTTON_BACKGROUND_COLOR)
        purchase_btn.bind(on_press=partial(self.purchase, CardPack.original, 1))
        button_layout.add_widget(purchase_btn)

        self.qty = Label(text=str(0),
                         font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                         color=LABEL_TEXT_COLOR)
        self.gold = Label(text=str(0),
                          font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                          color=LABEL_TEXT_COLOR)

        up_btn = Button(text='Up',
                        font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                        background_color=BUTTON_BACKGROUND_COLOR)
        up_btn.bind(on_press=self.up_qty)

        down_btn = Button(text='Down',
                          font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                          background_color=BUTTON_BACKGROUND_COLOR)
        down_btn.bind(on_press=self.down_qty) 

        lobby_btn = Button(text='Lobby',
                           font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                           background_color=BUTTON_BACKGROUND_COLOR)
        down_btn.bind(on_press=self.lobby)
        button_layout.add_widget(lobby_btn)

        main_layout.add_widget(button_layout)

        self.add_widget(main_layout)
    
    def on_enter(self, *args):
        self.update(self)
    
    def update(self):
        gold : int = user_data.gold
        self.gold.text = str(gold)
    
    def up_qty(self, inst):
        qty : int = self.qty.text
        if qty < 100:
            self.qty.text = str(qty + 1)
        
    def down_qty(self, inst):
        qty : int = self.qty.text
        if 0 < qty:
            self.qty.text = str(qty - 1)
    
    def purchase(self, inst, *args):
        pack : CardPack = args[0]
        qty : int = args[1]
        if pack == CardPack.original:
            pass
        elif pack == CardPack.naxxramas:
            pass
        elif pack == CardPack.gobvsgno:
            pass
        elif pack == CardPack.blackrock:
            pass
    
    def lobby(self, inst):
        self.manager.current = 'lobby'