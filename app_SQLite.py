#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import config

from flask import *

app = Flask(__name__)
app.config.from_object('config')


@app.before_request
def before_request():
    g.db = sqlite3.connect(app.config['DATABASE'])


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# URL 重定向
@app.route('/')
def index():
    if 'user' in session:
        return render_template('hello.html', name=session['user'])
    else:
        return redirect(url_for('login'), 302)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form['user']
        password = request.form['password']
        cursor = g.db.execute('select * from users where name=? and password=?', [name, password])
        if cursor.fetchone():
            session['user'] = name
            flash('login successfully!')
            return redirect(url_for('index'))
        else:
            flash('No such user!', 'error')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')



