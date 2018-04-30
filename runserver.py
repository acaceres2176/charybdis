import re
from flask import Flask
from flask import render_template, jsonify
from flask import request, session, url_for, redirect, abort
import traceback
import sys
import string
from stem.control import Controller
from hashlib import sha224
import datetime
from stem import SocketError
import textwrap
app = Flask(__name__)
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
import random


def id_generator(size=6,
                 chars=string.ascii_uppercase + string.digits +
                 string.ascii_lowercase):
    
    return ''.join(random.choice(chars) for i in range(size))

app.secret_key = id_generator(size=64)

def check_older_than(chat_dic, secs_to_live = 180):
    now = datetime.datetime.now()
    timestamp = chat_dic["timestamp"]
    diff = now - timestamp
    secs = diff.total_seconds()

    if secs >= secs_to_live:
        return True

    return False

def get_random_color():

    r = lambda: random.randint(0,128)
    return (r(),r(),r())


@app.route('/', methods=["GET", "POST"])
def main_page(url_addition):

    return render_template("index.html")


def main():

    app.run(debug=True, threaded = True)


    
if __name__ == "__main__":
    main()
