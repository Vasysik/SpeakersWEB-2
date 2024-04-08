import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 10180))

while True:
    data = client_socket.recv(1024).decode()
    if data:
        data_list = data.split(',')
        print('Received: ', data_list)
