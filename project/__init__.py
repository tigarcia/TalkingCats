from flask import Flask, Blueprint, redirect, render_template, request, flash, url_for, jsonify, json
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'talkingcats'

debug = True

if os.environ.get('ENV') == 'production':
    debug = False

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/sound', methods=["POST"])
def sound():
    return "hello"
