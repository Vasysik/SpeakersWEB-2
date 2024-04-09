import db
import time
import socket
import threading

def handle_client(connection, client_address):
    print('Connection from', client_address)

    try:
        conn = db.create_connection()
        while True:
            audio_data = db.get_audio_to_play(conn)
            if audio_data:
                for data in audio_data:
                    audio_str = ','.join(map(str, data))
                    connection.sendall(audio_str.encode())
            time.sleep(1)
    except ConnectionResetError:
        print(f"Client {client_address} disconnected.")
    finally:
        connection.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 10180))
server_socket.listen(10)
print('Waiting for a connection...')
while True:
    connection, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
    client_thread.start()
