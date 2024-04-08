import db
import time
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 10180))
server_socket.listen(10)
while True:
    print('Waiting for a connection...')
    connection, client_address = server_socket.accept()
    try:
        print(f'Connection from {client_address}')

        while True:
            audio_data = db.get_audio_to_play()
            for data in audio_data:
                # Convert data to a string and send it to the connected client
                audio_str = ','.join(map(str, data))
                connection.sendall(audio_str.encode())
            time.sleep(1)  # Check every second

    finally:
        print('Connection close...')
        connection.close()
