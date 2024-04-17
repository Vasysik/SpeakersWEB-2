import socket
import signal
import sys
import pygame
import tempfile
import os
import urllib.request

server = { 
    'ip': '127.0.0.1',
    'port': 10180
}

site = { 
    'ip': '127.0.0.1',
    'port': 5000
}

pygame.init()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(1)
client_socket.connect((server['ip'], server['port']))

def handle_keyboard_interrupt(signal, frame):
    print("\nExiting...")
    client_socket.close()
    pygame.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_keyboard_interrupt)

def play_audio(audio_url):
    try:
        with urllib.request.urlopen(audio_url) as response:
            with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
                temp_audio_file.write(response.read())
                temp_audio_file_name = temp_audio_file.name
        pygame.mixer.music.load(temp_audio_file_name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(30)
        pygame.mixer.music.stop() 
        pygame.mixer.music.unload() 
        os.remove(temp_audio_file_name)
    except Exception as e:
        print("Error:", e)

while True:
    try:
        data = client_socket.recv(1024).decode()
        if data:
            data_list = data.split(',')
            print('Received: ', data_list)
            
            audio_file = data_list[3]
            audio_url = f'http://{site["ip"]}:{site["port"]}/static/audio/{audio_file}'
            play_audio(audio_url)
    except socket.timeout:
        pass