import socket

from server.database import cursor
from server.socket_manager import clients_sock_to_id, clients_id_to_sock
from server.client_info import load_user_info

from common.serializes import *
from common.userdata import UserData

def handle_client(client: socket.socket, addr):
    while True:
        data_received : bytes = client.recv(1024)
        process(client, data_received)

def process(client: socket.socket, bts: bytes):
    request : Lobby = Lobby.decode(bts)
    if request.content == LobbyEnum.register:
        ret, title, text = register(request)
    elif request.content == LobbyEnum.login:
        ret, title, text = login(request, client)
    elif request.content == LobbyEnum.logout:
        ret, title, text = logout(request)
    elif request.content == LobbyEnum.purchase:
        ret, title, text = purchase(request, client)
    elif request.content == LobbyEnum.craft:
        ret, title, text = craft(request, client)
    else:
        ret, title, text = (False, "Process failed", "Unexpected error.")
    
    if ret:
        response = ServerAccept(ServerEnum.accept, title, text)
    else:
        response = ServerDecline(ServerEnum.decline, title, text)
    client.sendall(ServerResponse.encode(response))
    
    if request.content == LobbyEnum.login and ret:
        id : int = clients_sock_to_id[client]
        user_data : UserData = load_user_info(id)
        client.sendall(UserData.encode(user_data))
    
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

def purchase(inst: Purchase, client: socket.socket) -> (bool, str, str):
    CARDPACK_PRICE = 100
    
    query = "SELECT gold FROM RESOURCES WHERE id = %s"
    cursor.execute(query, (inst.id,))
    
    result = cursor.fetchone()
    if result:
        gold = result[0]
        if gold >= inst.qty * CARDPACK_PRICE:
            cardpack = inst.cardpack.name.lower()
            query = "UPDATE CARDPACKS SET %s = %s + %s WHERE id = %s"
            cursor.execute(query, (cardpack, cardpack, inst.qty, inst.id,))
            
            return (True, "Purchase success!", f"You purchased {inst.qty} {cardpack} pack(s).")
        else:
            return (False, "Purchase failed", "Insufficient gold.")
    else:
        return (False, "Purchase failed", "Unexpected error.")

def craft(inst: Craft, client: socket.socket):
    raise NotImplementedError

def give_basic_cards(id: int):
    
    # TODO
    # 파일을 읽어서 계정을 등록했을 때 기본 카드들을 줍시다.
    
    raise NotImplementedError