from flask import render_template

from watchlist import app


@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400
# 使用 app.errorhandler() 注册错误处理函数，传入一个 Http 状态码作参数
# 普通视图函数不用写出状态码，默认使用 200 状态码表示响应成功


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
