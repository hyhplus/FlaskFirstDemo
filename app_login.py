import time

from flask import Flask, render_template, request, session, redirect, url_for, make_response

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


# HTTP 请求方法设置
# session
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['user'] == 'admin':
            session['user'] = request.form['user']
            return 'Admin login successfully!'
        else:
            return 'No such user!'

    if 'user' in session:
        return 'Hello %s!' % session['user']
    else:
        title = request.args.get('title', 'Default')
        response = make_response(render_template('login.html', title=title), 200)
        response.headers['key'] = 'value'
        return response


# 特别提醒，使用session时一定要设置一个密钥app.secret_key
app.secret_key = 'asd1421as3414geg1247n'


# 登出, 清除字典里的键值
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# cookies
@app.route('/login_c', methods=['POST', 'GET'])
def login_cookies():
    if request.method == 'POST':
        if request.form['user'] == 'admin':
            session['user'] = request.form['user']
            response = make_response('Admin login successfully！')
            response.set_cookie('login_time', time.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            return 'No such user!'
    else:
        if 'user' in session:
            login_time = request.cookies.get('login_time')
            response = make_response('Hello {0}, your logged in on {1}'.format(session['user'], login_time))
            response.set_cookie('login_time', time.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            title = request.args.get('title', 'Default')
            response = make_response(render_template('login.html', title=title), 200)

    return response


if __name__ == '__main__':

    app.run(host='0.0.0.0',  debug=True)
