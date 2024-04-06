from flask import Flask, render_template, request, redirect, url_for
from pydub import AudioSegment
from datetime import datetime
import uuid
import os
import db

app = Flask(__name__)
username = "John Doe"

# Главная страница
@app.route('/')
def index():
    # Создание переменной newBell
    newBell = {
        "time": "",
        "duration": "",
        "info": "",
        "uploaderName": username
    }
    current_time = datetime.now()
    
    return render_template('index.html', newBell=newBell, bells=db.get_all_bells(), current_time=current_time, datetime=datetime)

# Страница логинизации
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/audio', methods=['POST'])
def upload_audio():
    audio_file = request.files['audio']

    os.makedirs(os.path.join('static', 'audio'), exist_ok=True)
    unique_filename = f"{uuid.uuid4()}-{audio_file.filename}"

    audio_file.save(os.path.join('static', 'audio', unique_filename))
    
    audio = AudioSegment.from_file('static/audio/' + audio_file.filename)
    duration_seconds = len(audio) / 1000
    
    return {
        'filename': audio_file.filename,
        'duration': duration_seconds
    }

@app.route('/create_bell', methods=['POST'])
def create_bell():
    info = request.form['info']
    time_str = request.form['time']
    audio_file = request.files['audio']

    unique_filename = f"{uuid.uuid4()}-{audio_file.filename}"

    audio_file.save(os.path.join('static', 'audio', unique_filename))

    audio = AudioSegment.from_file(os.path.join('static/audio', unique_filename))
    duration = len(audio) / 1000

    time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')

    db.add_bell(info, time, unique_filename, duration, username)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)