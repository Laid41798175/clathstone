import socket

from server.database import cursor
from server.socket_manager import clients_sock_to_id, clients_id_to_sock
from server.socket_manager import client_disconnected
from server.client_info import load_user_info
from server.secret import CHEAT_GOLD, CHEAT_DUST, CHEAT_LEVEL, \
    CHEAT_DRUID, CHEAT_HUNTER, CHEAT_MAGE, CHEAT_PALADIN, CHEAT_PRIEST, \
    CHEAT_ROGUE, CHEAT_SHAMAN, CHEAT_WARLOCK, CHEAT_WARRIOR

from common.serializes import *
from common.userdata import UserData

def handle_client(client: socket.socket, addr):
    while True:
        try: 
            data_received : bytes = client.recv(1024)
            process(client, data_received)
        except ConnectionResetError:
            print(f"{addr} disconnected")
            client_disconnected(client)
            break
    
    client.close()

def process(client: socket.socket, bts: bytes):
    request : Lobby = Lobby.decode(bts)
    if request.content == LobbyEnum.register:
        ret, title, text = register(request)
    elif request.content == LobbyEnum.login:
        ret, title, text = login(request, client)
        if ret:
            id : int = clients_sock_to_id[client] # clients_sock_to_id[client] is filled
            user_data : UserData = load_user_info(id)
            response = ServerAccept(title, text, user_data)
            client.sendall(ServerResponse.encode(response))
            return
    elif request.content == LobbyEnum.logout:
        ret, title, text = logout(request)
    elif request.content == LobbyEnum.changed:
        ret, title, text = changed(request, client)
    elif request.content == LobbyEnum.cheat:
        ret, title, text = cheat(request, client)
        if ret:
            id : int = clients_sock_to_id[client]
            user_data : UserData = load_user_info(id)
            response = ServerAccept(title, text, user_data)
            client.sendall(ServerResponse.encode(response))
            return
    else:
        ret, title, text = (False, "Process failed", "Unexpected error.")
    
    if ret:
        response = ServerAccept(title, text)
    else:
        response = ServerDecline(title, text)
    client.sendall(ServerResponse.encode(response))
    
def register(inst: Register) -> (bool, str, str):
    
    def is_valid_testkey(inst: Register) -> bool:
        query = "SELECT COUNT(*) FROM TESTKEYS WHERE testkey = %s"
        cursor.execute(query, (inst.testkey,))
            
        result = cursor.fetchone()
        if result is None or result[0] == 0:
            return False # invalid testkey

        query = "SELECT COUNT(*) FROM USERS WHERE testkey = %s"
        cursor.execute(query, (inst.testkey,))            

        result = cursor.fetchone()
        if result is None:
            return True
        else:
            return False # used testkey
            
    def is_valid_loginid(inst: Register) -> bool:
        query = "SELECT COUNT(*) FROM USERS WHERE loginid = %s"
        cursor.execute(query, (inst.loginid,))

        result = cursor.fetchone()
        if result and result[0] > 0:
            return False # used loginid
        else:
            return True
        
    def is_valid_nickname(inst: Register) -> bool:
        query = "SELECT COUNT(*) FROM USERS WHERE nickname = %s"
        cursor.execute(query, (inst.nickname,))  

        result = cursor.fetchone()
        if result and result[0] > 0:
            return False # used nickname
        else:
            return True
    
    if not is_valid_testkey(inst):
        return (False, "Register failed", "Invalid or used testkey.")
    if not is_valid_loginid(inst):
        return (False, "Register failed", "Used ID.")
    if not is_valid_nickname(inst):
        return (False, "Register failed", "Used nickname.")
    
    query = "INSERT INTO USERS (loginid, loginpw, testkey, nickname) \
        VALUES (%s, %s, %s, %s);"
    cursor.execute(query, (inst.loginid, inst.loginpw, inst.testkey, inst.nickname,))
    id = cursor.lastrowid
    
    query = "INSERT INTO CARDPACKS (id) VALUES (%s)"
    cursor.execute(query, (id,))
    
    query = "INSERT INTO RESOURCES (id) VALUES (%s)"
    cursor.execute(query, (id,))
    
    query = "INSERT INTO LEVELS (id) VALUES (%s)"
    cursor.execute(query, (id,))
    
    query = "INSERT INTO WINS (id) VALUES (%s)"
    cursor.execute(query, (id,))
    
    give_basic_cards(id)
    
    return (True, "Register success!", "You can login with your account!")
    
def login(inst: Login, client: socket.socket) -> (bool, str, str):
    query = "SELECT loginpw, nickname, id FROM USERS WHERE loginid = %s"
    cursor.execute(query, (inst.loginid,))
    
    result : tuple[str, str, int] = cursor.fetchone()
    if result:
        password, nickname, id = result
        if inst.loginpw == password:
            # if not id in clients.values():
                clients_sock_to_id[client] = id
                clients_id_to_sock[id] = client
                return (True, "Login success!", f"Welcome, {nickname}!")               
            # else:
            #     return (False, "Login failed", "Already login.")
        else:
            return (False, "Login failed", "Incorrect password.")
    else:
        return (False, "Login failed", "Login ID not found.")

def logout(inst: Logout) -> (bool, str, str):
    return (False, "Logout not implemented", "Please terminate instead.")

def changed(inst: Changed, client: socket.socket) -> (bool, str, str):
    pass

def cheat(inst: Cheat, client: socket.socket) -> (bool, str, str):

    id = clients_sock_to_id[client]
    
    def execute_query(query: str):
        cursor.execute(query + " WHERE id = %s", (id,))
    
    text = inst.text.lower()
    
    if text == CHEAT_GOLD: # Starcraft
        execute_query("UPDATE RESOURCES SET gold = gold + 10000")
    elif text == CHEAT_DUST: # T & Sugah x NCT
        execute_query("UPDATE RESOURCES SET dust = dust + 10000")
    elif text == CHEAT_LEVEL: # Web Novel
        execute_query("UPDATE LEVELS SET druid = 60.0, hunter = 60.0, mage = 60.0, paladin = 60.0, \
            priest = 60.0, rogue = 60.0, shaman = 60.0, warlock = 60.0, warrior = 60.0")
    elif text == CHEAT_DRUID: # DOTA 2
        execute_query("UPDATE WINS SET druid = druid + 100")
    elif text == CHEAT_HUNTER: # Anime
        execute_query("UPDATE WINS SET hunter = hunter + 100")
    elif text == CHEAT_MAGE: # Wizards of the Coast
        execute_query("UPDATE WINS SET mage = mage + 100")
    elif text == CHEAT_PALADIN: # Baldur's Gate 3
        execute_query("UPDATE WINS SET paladin = paladin + 100")
    elif text == CHEAT_PRIEST: # LostArk
        execute_query("UPDATE WINS SET priest = priest + 100")
    elif text == CHEAT_ROGUE: # Mission: Impossible
        execute_query("UPDATE WINS SET rogue = rogue + 100")
    elif text == CHEAT_SHAMAN: # Anime
        execute_query("UPDATE WINS SET shaman = shaman + 100")
    elif text == CHEAT_WARLOCK: # Princess Connect! Re:Dive
        execute_query("UPDATE WINS SET warlock = warlock + 100")
    elif text == CHEAT_WARRIOR: # Imagine Dragons
        execute_query("UPDATE WINS SET warrior = warrior + 100")
    else:
        return (False, "Cheat failed", "Invalid cheat.")
    
    return (True, "Cheat success!", "Cheat enabled.")
    
def give_basic_cards(id: int):
    
    query = "INSERT INTO COLLECTIONS (id, cardid, qty) \
        SELECT %s, cardid, qty FROM BASICCARDS"
    cursor.execute(query, (id,))