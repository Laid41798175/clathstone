from common.userdata import UserData, UserDataBuilder
from common.enums import CardPack, Faction

from server.database import cursor

def load_user_info(id: int) -> UserData:
    
    def execute_query(query: str):
        cursor.execute(query + " WHERE id = %s", (id,))
    
    builder = UserDataBuilder()
    builder.set_id(id)

    execute_query("SELECT nickname FROM USERS")
    result = cursor.fetchone()
    nickname = result[0]
    builder.set_nickname(nickname)
    
    execute_query("SELECT gold, dust FROM RESOURCES")
    result = cursor.fetchone()
    gold, dust = result
    builder.set_gold(gold)
    builder.set_dust(dust)
    
    execute_query("SELECT original, naxxramas, gobvsgno, blackrock FROM CARDPACKS")
    result = cursor.fetchone()
    original, naxxramas, gobvsgno, blackrock = result
    packs : dict[CardPack, int] = {}
    packs[CardPack.original] = original
    packs[CardPack.naxxramas] = naxxramas
    packs[CardPack.gobvsgno] = gobvsgno
    packs[CardPack.blackrock] = blackrock 
    builder.set_packs(packs)
    
    execute_query("SELECT cardid, qty FROM COLLECTIONS")
    results = cursor.fetchall()
    cards : dict[int, int] = {}
    for result in results:
        cardid, qty = result
        cards[cardid] = qty
    builder.set_cards(cards)
    
    execute_query("SELECT deckname, deckcode FROM DECKS")    
    results = cursor.fetchall()
    decks : list[tuple[str, str]] = results
    builder.set_decks(decks)
    
    execute_query("SELECT druid, hunter, mage, paladin, priest, rogue, shaman, warlock, warrior FROM LEVELS")    
    result = cursor.fetchone()
    druid, hunter, mage, paladin, priest, rogue, shaman, warlock, warrior = result
    levels : dict[Faction, float] = {}
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
    
    execute_query("SELECT druid, hunter, mage, paladin, priest, rogue, shaman, warlock, warrior FROM WINS")    
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
    
    return builder.build()

def commit_user_data(id: int, user_data: UserData):
    
    def execute_query(query: str):
        try:
            cursor.execute(query + " WHERE id = %s", (id,))
        except:
            print(f"Invalid syntax: {query}")
        
    execute_query(f"UPDATE RESOURCES
                    SET gold = {user_data.gold}, dust = {user_data.dust}")
    
    execute_query(f"UPDATE CARDPACKS
                    SET original = {user_data.packs[CardPack.original]},
                        naxxramas = {user_data.packs[CardPack.naxxramas]},
                        gobvsgno = {user_data.packs[CardPack.gobvsgno]},
                        blackrock = {user_data.packs[CardPack.blackrock]}")
    
    execute_query("DELETE FROM COLLECTIONS")
    for card_id, qty in user_data.cards.items():
        query = "INSERT INTO COLLECITONS VALUES %s, %s, %s"
        cursor.execute(query, (id, card_id, qty,))
    
    execute_query("DELETE FROM COLLECTIONS")
    for deckname, deckcode in user_data.decks:
        query = "INSERT INTO DECKS VALUES %s, %s, %s"
        cursor.execute(query, (id, deckname, deckcode,))
    
    # TODO
    # LEVELS
    
    # TODO
    # WINS