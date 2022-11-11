#!/usr/bin/python3
import json
import subprocess
import flask 
import psutil
import queue
import fish_controller
import threading
import logging
from fish_facts import get_random_fish_fact

logging.basicConfig(filename='/home/loc/flask.log', level=logging.DEBUG)

SAY_SCRIPT = '/home/loc/workspace/trunkortreat/www/speech.sh'
SONG_FILE  = 'INSERT-SONG-PATH-HERE'
SILENT_FILE = '/home/loc/workspace/trunkortreat/www/silent_delay.mp3'
SPEECH_DETECTOR = '/home/loc/workspace/trunkortreat/www/speech_detector.py'

global fish_mutex
global command_queue
global response_queue
global enable_users

app = flask.Flask(__name__)
enable_users = True

def say_message(message):
    global command_queue
    global response_queue
    global fish_mutex

    kill_audio()
    with fish_mutex:
        item = "speech"
        command_queue.put(item)
        ret = response_queue.get()
    app.logger.info(f"Fish speech: {message}")
    subprocess.Popen(['mplayer', SILENT_FILE])
    subprocess.Popen([SAY_SCRIPT, message])

def play_song(repeat = False):
    global command_queue
    global response_queue
    global fish_mutex

    kill_audio()
    with fish_mutex:
        item = "song"
        command_queue.put(item)
        ret = response_queue.get()
    if repeat == True:
        app.logger.info(f"Fish song")
        subprocess.Popen(['mplayer', '-loop', '0', SONG_FILE])
    else:
        app.logger.info(f"Fish song")
        subprocess.Popen(['mplayer', SONG_FILE])

def kill_audio():
    for proc in psutil.process_iter():
        if proc.name() == 'mplayer':
            proc.kill()

def start_fish_controller():
    global command_queue
    global response_queue
    global fish_mutex
    command_queue = queue.Queue()
    response_queue = queue.Queue()
    fish_mutex = threading.Lock()

    app.logger.info(f"Starting fish controller")
    fish = fish_controller.FishThread(command_queue, response_queue)
    fish_thread = threading.Thread(target=fish.start)
    fish_thread.start()

    app.logger.info(f"Starting speech detector")
    subprocess.Popen(['python', SPEECH_DETECTOR])
    
    app.logger.info(f"Starting speech detector conplete!")
    return fish_thread

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/control')
def control():
    return flask.render_template('control.html')

@app.route('/control', methods=["POST"])
def control_post():
    global enable_users
    app.logger.info(f"POST message received")
    flask.flash("Message Sent!")
    if flask.request.method == "POST":
        for key, value in flask.request.form.items():
            if key == 'FishMessage':
                message = str(flask.request.form['FishMessage'])
                if enable_users:
                    say_message(message)
                else:
                    flask.flash("Fish control has been disabled. Ask the fisherman to turn it back on.")
                    app.logger.info(f"Message received while disabled: {message}")
            elif key =='fish_fact':
                say_message(get_random_fish_fact())
        
    return flask.redirect(flask.url_for('control')) 

@app.route('/details')
def details():
    return flask.render_template('details.html')

@app.route('/secret')
def secret():
    return flask.render_template('secret.html')

@app.route('/secret', methods=["POST"])
def secret_post():
    global enable_users
    if flask.request.method == "POST":
        for key, value in flask.request.form.items():
            if key == 'stopaudio':
                kill_audio()
                pass
            elif key =='song':
                play_song()
                pass
            elif key =='song_repeat':
                play_song(repeat=True)
                pass
            elif key =='pretyped':
                if value == '1':
                    message = "Happy Halloween!"
                    say_message(message)
                elif value == '2':
                    message = "What are you look at?"
                    say_message(message)
                elif value == '3':
                    message = "This is my life now."
                    say_message(message)
            elif key =='FishMessage':
                message = str(value)
                say_message(message)
            elif key =='enable':
                enable_users = True
            elif key =='disable':
                enable_users = False
            elif key =='fish_fact':
                say_message(get_random_fish_fact())

    return flask.redirect(flask.url_for('secret')) 

if __name__ == '__main__':
    try:
        start_fish_controller()
        app.secret_key='12345'
        app.run(host='0.0.0.0')
    finally:
        pass
