from server.socket_manager import server_socket
from server.account import handle_client

from threading import Thread

while True:
    client_socket, addr = server_socket.accept()
    thread = Thread(target=handle_client, args=(client_socket, addr))
    thread.start()