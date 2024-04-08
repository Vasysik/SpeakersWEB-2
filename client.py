import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 10180))

while True:
    data = client_socket.recv(1024).decode()
    if data:
        # Split the received data into separate values
        data_list = data.split(',')
        # Here you can handle the received data
        # For now, we'll just print it
        print('Received: ', data_list)
