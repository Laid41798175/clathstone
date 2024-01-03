import mysql.connector
from server.secret import DBUSER, DBPASSWORD, DBDATABASE

# 데이터베이스 연결 설정
config = {
    'user': DBUSER,
    'password': DBPASSWORD,
    'host': 'localhost',
    'port': 3307, # 3306 is reserved for WSL mysql, you may have to change port
    'database': DBDATABASE,
    'raise_on_warnings': True
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

def test():
    query = "show tables"
    cursor.execute(query)
    
    results = cursor.fetchall()
    for result in results:
        print(result[0])
        
# test()