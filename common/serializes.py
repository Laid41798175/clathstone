import pickle
from common.enums import ServerEnum, LobbyEnum, GameEnum, CardPack, Faction
from common.userdata import UserData

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
    
    def __init__(self, title: str, text: str, user_data: UserData = None):
        super().__init__(ServerEnum.accept)
        self.title = title
        self.text = text
        self.user_data = user_data

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
        
class Changed(Lobby):
    
    def __init__(self, user_data = None):
        super().__init__(LobbyEnum.changed)
        self.user_data = user_data
        
class Cheat(Lobby):
    
    def __init__(self, text: str):
        super().__init__(LobbyEnum.cheat)
        self.text = text
        
    
class Game(Serial):
    
    def __init__(self, content: GameEnum):
        self.content = content