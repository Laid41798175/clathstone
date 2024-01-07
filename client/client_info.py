from common.userdata import UserData
from common.serializes import ServerAccept

user_data : UserData = None

def load_user_data(response: ServerAccept):
    global user_data
    user_data = response.user_data
    
    # TODO
    # update UIs