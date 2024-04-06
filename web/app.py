from flask import Flask, render_template, request
from pydub import AudioSegment

app = Flask(__name__)

# Главная страница
@app.route('/')
def index():
    username = "John Doe"
    # Создание переменной newBell
    newBell = {
        "time": "",
        "duration": "",
        "info": "",
        "uploaderName": username
    }
    return render_template('index.html', newBell=newBell)

# Страница логинизации
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/audio', methods=['POST'])
def upload_audio():
    audio_file = request.files['audio']
    # Сохраняем загруженный файл на сервере
    audio_file.save('static/audio/' + audio_file.filename)
    
    # Определяем длительность аудио
    audio = AudioSegment.from_file('static/audio/' + audio_file.filename)
    duration_seconds = len(audio) / 1000
    
    return {
        'filename': audio_file.filename,
        'duration': duration_seconds
    }

if __name__ == '__main__':
    app.run(debug=True)