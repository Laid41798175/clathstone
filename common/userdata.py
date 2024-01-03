import pickle

from common.enums import CardPack, Faction

class UserData:
    
    def __init__(self, id=None, nickname=None, gold=None, dust=None, packs=None,
                 cards=None, decks=None, levels=None, wins=None):
        self.id : int = id
        self.nickname : str = nickname
        self.gold : int = gold
        self.dust : int = dust
        self.packs : dict[CardPack, int] = packs
        self.cards : dict[int, int] = cards # his/her own collections
        self.decks : list[str] = decks # deck lists
        self.levels : dict[Faction, int] = levels
        self.wins : dict[Faction, int] = wins
    
    @staticmethod
    def encode(inst) -> bytes:
        return pickle.dumps(inst)

    @staticmethod
    def decode(bts: bytes):
        return pickle.loads(bts)
    
class UserDataBuilder:
    def __init__(self):
        self.user_data = UserData()

    def set_id(self, id):
        self.user_data.id = id
        return self

    def set_nickname(self, nickname):
        self.user_data.nickname = nickname
        return self

    def set_gold(self, gold):
        self.user_data.gold = gold
        return self

    def set_dust(self, dust):
        self.user_data.dust = dust
        return self
    
    def set_packs(self, packs):
        self.user_data.packs = packs
        return self

    def set_cards(self, cards):
        self.user_data.cards = cards
        return self

    def set_decks(self, decks):
        self.user_data.decks = decks
        return self
    
    def set_levels(self, levels):
        self.user_data.levels = levels
        return self

    def set_wins(self, wins):
        self.user_data.wins = wins
        return self
    
    def build(self):
        return self.user_data