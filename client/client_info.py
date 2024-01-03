from common.userdata import UserData

user_data : UserData = None

def load_user_data(bts: bytes):
    user_data = UserData.decode(bts)