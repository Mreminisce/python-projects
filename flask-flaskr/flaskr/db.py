import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
# 创建一个数据库的连接，所有查询和操作都通过这个连接来执行，并在结束后关闭。
# 在 web 应用中连接往往与请求绑定，在处理请求时创建连接，返回响应之前关闭连接。


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db
# 使用 sqlite3.connect() 函数来建立一个数据库连接指向配置中指定的 DATABASE 文件。
# 该文件将会在初始化数据库的时候创建。

# g 是一个特殊对象，独立于每一个请求。用来在处理请求时保存多个函数都可能会用到的数据。
# 把连接保存在 g 对象中可以避免每次调用 get_db 时都创建一个新的连接。

# current_app 是另一个特殊对象，指向处理请求的 Flask 应用。
# 在应用创建之后处理一个请求时 get_db 会被调用，这时就需要使用 current_app。

# sqlite3.Row 告诉连接返回一个类似字典的行对象，这样就可以通过列名称来操作数据。


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
# close_db 通过检查 g.db 来判断是否已建立连接，如果已建立就关闭连接。
# 以后会在应用工厂中告诉应用 close_db 函数，这样每次请求后就会调用它。


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
# get_db 返回一个数据库连接来执行文件中的命令，open_resource() 方法打开一个文件。


@click.command('init-db')        
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialize the database.')
# click.command() 定义一个名为 init-db 的命令行，接着调用 init_db 函数为用户显示一个成功的消息。


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
# close_db 和 init_db_command 函数都需要在应用实例中注册，否则无法使用。
# 因为使用了工厂函数，所以在写函数的时候应用实例还无法使用。
# 作为代替，我们用一个 init_app 函数把应用作为参数，在函数中进行注册。

# app.teardown_appcontext() 告诉 Flask 在返回响应后进行清理时调用此函数。
# app.cli.add_command() 新添加一个可以与 flask 一起工作的命令。
