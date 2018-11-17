#!/usr/bin/env python
from flask import Flask, render_template
import os
app = Flask(__name__)
@app.route('/')
def hello_world():
    username = "not defined"
    password = "not defined"
    bgcolor = "#aaa"
    textcolor = "#000"
    user_file = "/tmp/projected/secrets/username"
    password_file = "/tmp/projected/secrets/password"
    bgcolor_file = "/tmp/projected/configmap/bgcolor"
    textcolor_file = "/tmp/projected/configmap/textcolor"
     
    if os.path.exists(user_file):
        with open(user_file) as f:
            username = f.readline().strip()
    if os.path.exists(password_file):
        with open(password_file) as f:
            password = f.readline().strip()
    if os.path.exists(bgcolor_file):
        with open(bgcolor_file) as f:
            bgcolor = f.readline().strip()
    if os.path.exists(textcolor_file):
        with open(textcolor_file) as f:
            textcolor = f.readline().strip()

    return render_template('showall.html', 
            username = username, 
            password = password, 
            textcolor = textcolor,
            bgcolor = bgcolor)

if __name__ == '__main__':
   app.run(debug = True)
