from flask import Flask, Blueprint, redirect, render_template, request, flash, url_for, jsonify, json
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from subprocess import call,check_output
import os
import random
import string
from jinja2 import Template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'talkingcats'
debug = True

if os.environ.get('ENV') == 'production':
    debug = False

regular_text = Template('{{text|e}}')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in set(['wav'])

def mkdir_rand():
    dir_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    path = "./tmp/{}".format(dir_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def speech_file(base):
    s = """---

settings:

  # Deep learning model
  cnn:
    kernels: 1000
    size: 11
    stride: 2
  rnn:
    size: 1000
    depth: 3
  vocab:
    # Need for CTC
    size: 73

  # Setting up the backend.
  backend:
    name: keras
    backend: tensorflow

  # Batch sizes
  provider: &provider
    batch_size: 32 
    force_batch_size: no

  # Where to put the data.
  data: &data
    path: "./"
    type: spec
    max_duration: 50
    max_frequency: 8000
    normalization: %s/norm.yml
    vocab: %s/vocab.json

  # Where to put the weights
  weights: &weights %s/weights

###############################################################################
model:

  # This is Baidu's DeepSpeech model:
  #   https://arxiv.org/abs/1412.5567
  # Kur makes prototyping different versions of it incredibly easy.

  # The model input is audio data (called utterances).
  - input: utterance

  # One-dimensional, variable-size convolutional layers to extract more
  # efficient representation of the data.
  - convolution:
      kernels: "{{ cnn.kernels }}"
      size: "{{ cnn.size }}"
      strides: "{{ cnn.stride }}"
      border: valid
  - activation: relu
  - batch_normalization

  # A series of recurrent layers to learn temporal sequences.
  - for:
      range: "{{ rnn.depth }}"
      iterate:
        - recurrent:
            size: "{{ rnn.size }}"
            sequence: yes
        - batch_normalization

  # A dense layer to get everything into the right output shape.
  - parallel:
      apply:
        - dense: "{{ vocab.size + 1 }}"
  - activation: softmax

  # The output is the transcription.
  - output: asr

###############################################################################
evaluate:
  data:
    - speech_recognition:
        path: %s/corp
        type: spec
        max_duration: 50
        max_frequency: 8000
        normalization: %s/norm.yml
        vocab: %s/vocab.json

  hooks:
    - transcript

  weights: *weights

...
""" % (base, base, base, base, base, base)
    return s

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/sound', methods=["POST"])
def sound():
    dataList = request.files.getlist('data')
    fnames = []
    if dataList:
        path = mkdir_rand()
        call("cp -R ./model_data/* {}".format(path), shell=True)
        for idx, d in enumerate(dataList):
            filename = secure_filename("moxie{}.wav".format(idx))
            fnames.append(filename)
            d.save(os.path.join(path, "corp", "audio", filename))

        with open(os.path.join(path, "corp", "audio", 'AUDIO_index.txt'), 'w') as file:
            for f in fnames:
                file.write("file '{}'\n".format(f))
        call("ffmpeg -y -f concat  -i {} -ar 16000 -ac 1 {}".format(os.path.join(path, "corp", "audio",'AUDIO_index.txt'), os.path.join(path, "corp", "audio", 'out.wav')),shell=True)
        speech_yml = speech_file(path)
        with open(os.path.join(path, "speech.yml"), 'w') as f:
            f.write(speech_yml)

        output = check_output("kur evaluate {}".format(os.path.join(path, "speech.yml")), shell=True)
        print(output.decode('utf-8'))
        o = output.decode('utf-8').split("\n")[0]
        prediction = o.split(" ")[1]
        print(prediction[1:-1])
        #if output.decode("utf-8").split("\n") and len(output.decode('utf-8').split("\n")) == 2:

        return json.dumps({"text": prediction[1:-1], "vtext": regular_text.render(text=prediction[1:-1]) })

    return json.dumps({"text": "Something went wrong"}), 400
