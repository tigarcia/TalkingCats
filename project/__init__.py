from flask import Flask, Blueprint, redirect, render_template, request, flash, url_for, jsonify, json
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from subprocess import call
import os
import random
import string

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'talkingcats'
debug = True

if os.environ.get('ENV') == 'production':
    debug = False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in set(['wav'])

def mkdir_rand():
    dir_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    path = "./tmp/{}".format(dir_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/sound', methods=["POST"])
def sound():
    dataList = request.files.getlist('data')
    fnames = []
    if dataList:
        path = mkdir_rand()
        for idx, d in enumerate(dataList):
            filename = secure_filename("moxie{}.wav".format(idx))
            fnames.append(filename)
            d.save(os.path.join(path, filename))

        with open(os.path.join(path, 'AUDIO_index.txt'), 'w') as file:
            for f in fnames:
                file.write("file '{}'\n".format(f))
        call("ffmpeg -y -f concat  -i {} -ar 16000 -ac 1 {}".format(os.path.join(path, 'AUDIO_index.txt'), os.path.join(path, 'out.wav')),shell=True)

        return json.dumps({"text": "We Got Data!"})

    return json.dumps({"text": "Something went wrong"}), 400
