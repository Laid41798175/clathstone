import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen()

clients_sock_to_id : dict[socket.socket, int] = {}
clients_id_to_sock : dict[int, socket.socket] = {}