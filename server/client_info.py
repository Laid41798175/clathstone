from common.userdata import UserData, UserDataBuilder
from common.enums import CardPack, Faction

from server.database import cursor

def load_user_info(id: int) -> UserData:
    builder = UserDataBuilder()
    builder.set_id(id)
    
    query = "SELECT nickname FROM USERS WHERE id = %s"
    cursor.execute(query, (id,))
    
    result = cursor.fetchone()
    nickname = result[0]
    builder.set_nickname(nickname)
    
    query = "SELECT gold, dust FROM RESOURCES WHERE id = %s"
    cursor.execute(query, (id,))
    
    result = cursor.fetchone()
    gold, dust = result
    builder.set_gold(gold)
    builder.set_dust(dust)
    
    query = "SELECT original, naxxramas, gobvsgno, blackrock FROM CARDPACKS WHERE id = %s"
    cursor.execute(query, (id,))
    
    result = cursor.fetchone()
    original, naxxramas, gobvsgno, blackrock = result
    packs : dict[CardPack, int] = {}
    packs[CardPack.original] = original
    packs[CardPack.naxxramas] = naxxramas
    packs[CardPack.gobvsgno] = gobvsgno
    packs[CardPack.blackrock] = blackrock 
    builder.set_packs(packs)
    
    query = "SELECT cardid, qty FROM COLLECTIONS WHERE id = %s"
    cursor.execute(query, (id,))
    
    results = cursor.fetchall()
    cards : dict[int, int] = {}
    for result in results:
        cardid, qty = result
        cards[cardid] = qty
    builder.set_cards(cards)
    
    query = "SELECT deckname, deckcode FROM DECKS WHERE id = %s"
    cursor.execute(query, (id,))
    
    results = cursor.fetchall()
    decks : list[tuple[str, str]] = results
    builder.set_decks(decks)
    
    query = "SELECT druid, hunter, mage, paladin, priest, rogue, shaman, warlock, warrior FROM LEVELS WHERE id = %s"
    cursor.execute(query, (id,))
    
    result = cursor.fetchone()
    druid, hunter, mage, paladin, priest, rogue, shaman, warlock, warrior = result
    levels : dict[Faction, int] = {}
    levels[Faction.druid] = druid
    levels[Faction.hunter] = hunter
    levels[Faction.mage] = mage
    levels[Faction.paladin] = paladin
    levels[Faction.priest] = priest
    levels[Faction.rogue] = rogue
    levels[Faction.shaman] = shaman
    levels[Faction.warlock] = warlock
    levels[Faction.warrior] = warrior
    builder.set_levels(levels)
    
    query = "SELECT druid, hunter, mage, paladin, priest, rogue, shaman, warlock, warrior FROM WINS WHERE id = %s"
    cursor.execute(query, (id,))
    
    result = cursor.fetchone()
    druid, hunter, mage, paladin, priest, rogue, shaman, warlock, warrior = result
    wins : dict[Faction, int] = {}
    wins[Faction.druid] = druid
    wins[Faction.hunter] = hunter
    wins[Faction.mage] = mage
    wins[Faction.paladin] = paladin
    wins[Faction.priest] = priest
    wins[Faction.rogue] = rogue
    wins[Faction.shaman] = shaman
    wins[Faction.warlock] = warlock
    wins[Faction.warrior] = warrior
    builder.set_wins(wins)