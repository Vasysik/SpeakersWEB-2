from flask import Flask, render_template, request, redirect, url_for, flash, session
from pydub import AudioSegment
from datetime import datetime, timedelta
import uuid
import os
import db

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def check_login():
    return 'username' in session

@app.route('/')
def index():
    if 'username' in session:
        newBell = {
            "time": "",
            "duration": "",
            "info": "",
            "uploaderName": session['username']
        }
        current_time = datetime.now()
        return render_template('index.html', newBell=newBell, bells=db.get_all_bells(), current_time=current_time, datetime=datetime, username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']
        user = db.get_user(input_username)
        if user and user['password'] == input_password:
            session['username'] = input_username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/create_bell', methods=['POST'])
def create_bell():
    if not check_login():
        return redirect(url_for('login'))
    
    info = request.form['info']
    time_str = request.form['time']

    audio_file = request.files['audio']

    unique_filename = f"{uuid.uuid4()}-{audio_file.filename}"

    audio_file.save(os.path.join('static', 'audio', unique_filename))

    audio = AudioSegment.from_file(os.path.join('static', 'audio', unique_filename))
    duration = len(audio) / 1000

    try:
        time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
    except:
        time_str += ":00"
        time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')

    db.add_bell(info, time, unique_filename, duration, session['username'])

    return redirect(url_for('index'))

@app.route('/create_emergency_bell', methods=['POST'])
def create_emergency_bell():
    if not check_login():
        return redirect(url_for('login'))

    emergency_type = request.form['emergency_type']
    duration = 0

    info = {
        'fire': 'Пожар',
        'terrorism': 'Угроза терроризма'
        # Добавьте другие типы ситуаций по мере необходимости
    }.get(emergency_type, 'Неизвестная ситуация')

    future_time = (datetime.now() + timedelta(seconds=2)).replace(microsecond=0)

    db.add_bell(info, future_time, f"emergency_audios/{emergency_type}.mp3", duration, session['username'])

    return redirect(url_for('index'))

@app.route('/delete_bell/<int:bell_id>', methods=['POST'])
def delete_bell(bell_id):
    if not check_login():
        return redirect(url_for('login'))
    
    db.delete_bell(bell_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')