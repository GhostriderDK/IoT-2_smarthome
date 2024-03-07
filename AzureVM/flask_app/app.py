import sqlite3
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)
app.run(debug=True)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mqtt')
def mqtt():
    return render_template('mqtt.html')


@app.route('/kitchen')
def kitchen():
    return render_template('kitchen.html')

@app.route('/livingroom')
def livingroom():
    return render_template('livingroom.html')

