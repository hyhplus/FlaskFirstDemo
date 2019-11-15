from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % username


# 不输入最后的‘/’斜杆，url会自动加上‘/’
@app.route('/projects/')
def projects():
    return 'The project page'


# url后不能添加‘/’，否则返回404
# 这样可以保持 URL 唯一，并帮助 搜索引擎避免重复索引同一页面。
@app.route('/about')
def about():
    return 'The about page'


# 模板渲染例子，带参数的路由
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0',  debug=False)
