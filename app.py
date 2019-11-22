from flask import Flask, render_template, request, Markup

app = Flask(__name__)


@app.route('/hello_world')
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


# HTTP 请求方法设置
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.date)
        return 'This is a POST request'

    else:
        return 'This is a GET request'


# HTTP 自动转义
# 但有时我们并不想让这些HTML标签自动转义，特别是传递表单参数时，很容易导致HTML注入的漏洞
# 我们把下面的代码改下，引入”Markup”类
@app.route('/')
def index():
    # return '<div>Hello %s</div>' % '<em>Flask</em>'
    return Markup('<div>Hello %s</div>') % '<em>Flask</em>'


if __name__ == '__main__':
    app.run(host='0.0.0.0',  debug=True)
