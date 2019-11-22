#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误处理
"""
from flask import *
from logging.handlers import TimedRotatingFileHandler
import logging

app = Flask(__name__)

# 日志
server_log = TimedRotatingFileHandler('server.log', 'D')
server_log.setLevel(logging.DEBUG)
server_log.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))

error_log = TimedRotatingFileHandler('error.log', 'D')
error_log.setLevel(logging.ERROR)
error_log.setFormatter(logging.Formatter('%(asctime)s: %(message)s [in %(pathname)s:%(lineno)d]'))

app.logger.addHandler(server_log)
app.logger.addHandler(error_log)


@app.route('/error')
def error():
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


"""
不过，在实际开发过程中，我们并不会经常使用 abort() 来退出，常用的错误处理方法一般
都是异常的抛出或捕获。装饰器@app.errorhandler() 除了可以注册错误代码外，
还可以注册指定的异常类型。让我们来自定义一个异常：
"""


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code


@app.errorhandler(InvalidUsage)
def invalid_usage(errors):
    response = make_response(errors.message)
    response.status_code = errors.status_code
    return response


@app.route('/exception')
def exception():
    # 日志
    app.logger.debug('Enter exception method')
    app.logger.error('403 error happened')
    raise InvalidUsage('No privilege to access the resource', status_code=403)


# URL 重定向
@app.route('/')
def index():
    if 'user' in session:
        return render_template('hello.html', name=session['user'])
    else:
        return redirect(url_for('login'), 302)


# 消息闪现
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['user']
        flash('Login successfully!', 'message')
        flash('Login as user: %s.' % request.form['user'], 'info')
        return redirect(url_for('index'))
    else:
        return '''
        <form name="login" action="/login" method="post">
            Username: <input type="text" name="user" />
        </form>
        '''


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'), 302)


# 注意加上 session 密钥
app.secret_key = '12345678'


if __name__ == '__main__':
    app.run(host='0.0.0.0',  debug=True)



