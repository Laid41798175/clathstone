import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen()

clients_sock_to_id : dict[socket.socket, int] = {}
clients_id_to_sock : dict[int, socket.socket] = {}

def client_disconnected(client: socket.socket):
    
    clients_sock_to_id.pop(client, None)
    
    keys_to_remove = [key for key, value in clients_id_to_sock.items() if value == client]
    for key in keys_to_remove:
        clients_id_to_sock.pop(key, None)