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