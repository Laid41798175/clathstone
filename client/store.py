from client.socket_manager import client_socket
from client.config import PATH_TO_FONT, FONT_SIZE, BUTTON_BACKGROUND_COLOR, LABEL_TEXT_COLOR
from client.popup import show_popup
from client.client_info import user_data, load_user_data

from common import ServerEnum, ServerResponse, ServerAccept, ServerDecline
from common import UserData
from common import LobbyEnum, Lobby, Changed
from common import CardPack

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

from functools import partial

CARDPACK_PRICE = 100
MAX_PACK : int = 100

class StoreScreen(Screen):
        
    def __init__(self, **kw):
        super().__init__(**kw)
        main_layout = BoxLayout(orientation='vertical', spacing=50, padding=(100, 300))
        
        # self.cheat_input = TextInput(hint_text='cheat code',
        #                           font_name=PATH_TO_FONT, font_size=FONT_SIZE,
        #                           multiline=False)
        # main_layout.add_widget(self.cheat_input)

        button_layout = BoxLayout(spacing=50)

        original_btn = Button(text='Original',
                              font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                              background_color=BUTTON_BACKGROUND_COLOR)
        naxxramas_btn = Button(text='Curse of Naxxramas',
                               font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                               background_color=BUTTON_BACKGROUND_COLOR)
        gobvsgno_btn = Button(text='Goblins VS Gnomes',
                              font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                              background_color=BUTTON_BACKGROUND_COLOR)
        blackrock_btn = Button(text='Blackrock Mountain',
                               font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                               background_color=BUTTON_BACKGROUND_COLOR)

        purchase_btn = Button(text='Purchase', 
                              font_name=PATH_TO_FONT, font_size=FONT_SIZE,
                              background_color=BUTTON_BACKGROUND_COLOR)
        purchase_btn.bind(on_press=self.purchase)
        button_layout.add_widget(purchase_btn)

        self.current_pack = CardPack.original
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
    
    def change_pack(self, inst, *args):
        pack : CardPack = args[0]
        self.current_pack = pack
    
    def up_qty(self, inst):
        qty : int = self.qty.text
        if qty < MAX_PACK:
            self.qty.text = str(qty + 1)
        
    def down_qty(self, inst):
        qty : int = self.qty.text
        if 0 < qty:
            self.qty.text = str(qty - 1)
    
    def purchase(self, inst):
        pack : CardPack = self.current_pack
        qty = int(self.qty.text)
        
        if user_data.gold < qty * CARDPACK_PRICE:
            show_popup("Purchase failed", "You don't have enough gold.")
            return
        
        user_data.gold -= qty * CARDPACK_PRICE
        user_data.packs[pack] += qty
        request = Lobby.encode(Changed(user_data))
        client_socket.sendall(request)
        
        data_received = client_socket.recv(1024)
        response : ServerAccept | ServerDecline = ServerResponse.decode(data_received)
        if response.content == ServerEnum.accept:
            show_popup("Purchase success!", f"You purchased {qty} {pack.name} pack(s).")
        elif response.content == ServerEnum.decline:
            show_popup("Purchase failed", "Couldn't commit your purchase.")
        load_user_data(response)
    
    def lobby(self, inst):
        self.manager.current = 'lobby'