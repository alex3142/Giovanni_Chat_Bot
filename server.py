# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 23:45:17 2018

@author: rcarlini
"""
import logging
from flask import Flask, render_template, request, jsonify

from giovanni import pipeline as pl
import time

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

pipeline = pl.Pipeline("resources/project_giovanni.0.1.ttl")


@app.route("/run_pipeline", methods=['POST'])
def run_pipeline():

    data = request.form['sentence']
    response = str(pipeline.process_text(data))

    return jsonify(response=response)


@app.route("/echo", methods=['POST'])
def echo():
    data = request.form['sentence']
    time.sleep(0.5)
    print(data)
    response = 'I only know how to say hi.'
    return jsonify(response=response)


@app.route("/new_session", methods=['GET'])
def restart():
    pipeline.new_session(session_type='html')
    print("pipeline restarted")
    return ""


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.logger.debug("What?")
    app.run(port=9999, debug=True)
