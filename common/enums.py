from enum import Enum

class ServerEnum(Enum):
    accept = 0
    decline = 1

class LobbyEnum(Enum):
    register = 0
    login = 1
    logout = 2
    changed = 3
    cheat = 4
    
class GameEnum(Enum):
    play = 0
    heropower = 1
    turnend = 2
    choice = 3
    attack = 4

class CardPack(Enum):
    original = 0
    naxxramas = 1
    gobvsgno = 2
    blackrock = 3

class Faction(Enum):
    neutral = 0
    druid = 1
    hunter = 2
    mage = 3
    paladin = 4
    priest = 5
    rogue = 6
    shaman = 7
    warlock = 8
    warrior = 9