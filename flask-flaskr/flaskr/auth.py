import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
# Blueprint 是一种组织一组相关视图及其他代码的方式。与把视图及其他代码直接注册到应用的方式不同，
# 蓝图方式是先把它们注册到蓝图，然后在工厂函数中把蓝图注册到应用。每个蓝图的代码都在一个单独的模块中。

bp = Blueprint('auth', __name__, url_prefix='/auth')
# 这里创建了一个名称为 'auth' 的 Blueprint 。和应用对象一样， 蓝图需要知道是在哪里定义的，
# 因此把 __name__ 作为函数的第二个参数。 url_prefix 会将 '/auth' 添加到所有与该蓝图关联的 URL 前面。


@bp.route('/register', methods=('GET', 'POST')) # bp.route 关联URL /register 和 register 视图函数
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # request.form 是一个特殊类型的字典对象，映射了提交表单的键和值

        db = get_db()
        error = None

        # 验证 username 和 password 不为空。
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'select id from user where username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        # 通过检查数据库是否有查询结果返回来验证 username 是否已被注册。
        # db.execute 使用了带有 ? 占位符 的 SQL 查询语句，占位符可以代替后面的元组参数中的相应值。
        # 使用占位符的好处是它会自动转义输入值，以抵御 SQL 注入攻击。

        # fetchone() 根据查询返回一个记录行。 如果查询没有结果则返回 None。
        # 后面还将用到 fetchall()，它返回包括所有结果的列表。

        if error is None:
            db.execute(
                'insert into user (username, password) values (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
        # 如果验证成功，那么在数据库中插入新用户数据。
        # 使用 generate_password_hash() 生成安全的哈希值储存到数据库中。
        # 使用 db.commit() 保存修改。

        flash(error)
        # flash() 用于储存在渲染模块时可以调用的信息，如果验证失败就向用户显示一个出错信息。
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'select * from user where username = ?', (username,)
        ).fetchone()
        # 查询用户并保存在变量中以备后面使用。

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        # check_password_hash() 比较密码的哈希值。

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        # session 是一个用于储存横跨请求值字典对象，如果验证成功用户的 id 会被储存在一个新的会话中。
        # session 数据会被储存到一个 cookie 中，浏览器会在后继请求中返回它。
        # Flask 会对数据进行签名以防数据被篡改。

        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request    
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'select * from user where id = ?', (user_id,)
        ).fetchone()
# bp.before_app_request() 注册一个在所有视图之前运行的函数：检查用户 id 是否已经储存在 session 中，
# 并从数据库中获取用户数据储存在 g.user 中，g.user 的持续时间比请求更长。


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
# 把用户 id 从 session 中移除。


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
# 装饰器返回一个新的视图，包含了传递给装饰器的原视图。
# 新的函数检查用户是否已载入，如果已载入就继续正常执行原视图，否则重定向到登录页面。 