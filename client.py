import socket
import signal
import sys
import pyglet

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(1)
client_socket.connect(('127.0.0.1', 10180))

def handle_keyboard_interrupt(signal, frame):
    print("\nExiting...")
    client_socket.close()
    pyglet.app.exit()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_keyboard_interrupt)

def play_audio(audio_url):
    player = pyglet.media.Player()
    source = pyglet.media.load(audio_url, streaming=True)
    player.queue(source)
    player.play()
    pyglet.app.run()

while True:
    try:
        data = client_socket.recv(1024).decode()
        if data:
            data_list = data.split(',')
            print('Received: ', data_list)
            
            audio_file = data_list[3]
            audio_url = f'http://127.0.0.1:5000/static/audio/{audio_file}'
            play_audio(audio_url)
    except socket.timeout:
        pass
