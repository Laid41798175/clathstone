import pickle
from common.enums import ServerEnum, LobbyEnum, GameEnum, CardPack, Faction

class Serial:
    
    @staticmethod
    def encode(inst) -> bytes:
        return pickle.dumps(inst)

    @staticmethod
    def decode(bts: bytes):
        return pickle.loads(bts)

class ServerResponse(Serial):
    
    def __init__(self, content: ServerEnum):
        self.content = content

class ServerAccept(ServerResponse):
    
    def __init__(self, title: str, text: str):
        super().__init__(ServerEnum.accept)
        self.title = title
        self.text = text

class ServerDecline(ServerResponse):
    
    def __init__(self, title: str, text: str):
        super().__init__(ServerEnum.decline)
        self.title = title
        self.text = text

class Lobby(Serial):
    
    def __init__(self, content: LobbyEnum):
        self.content = content

class Register(Lobby):
    
    def __init__(self, loginid: str, loginpw: str, nickname: str, testkey: str):
        super().__init__(LobbyEnum.register)
        self.loginid = loginid
        self.loginpw = loginpw
        self.nickname = nickname
        self.testkey = testkey
        
class Login(Lobby):
    
    def __init__(self, loginid: str, loginpw: str):
        super().__init__(LobbyEnum.login)
        self.loginid = loginid
        self.loginpw = loginpw
        
class Logout(Lobby):
    
    def __init__(self):
        super().__init__(LobbyEnum.logout)
        
class Purchase(Lobby):
    
    def __init__(self, id: int, cardpack: CardPack, qty: int):
        super().__init__(LobbyEnum.purchase)
        self.id = id
        self.cardpack = cardpack
        self.qty = qty        
        
class Craft(Lobby):
    
    def __init__(self, id: int, card_id: int):
        super().__init__(LobbyEnum.craft)
        self.id = id
        self.card_id = card_id
    
class Game(Serial):
    
    def __init__(self, content: GameEnum):
        self.content = content