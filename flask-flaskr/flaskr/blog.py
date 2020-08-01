from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)
# 与验证蓝图不同，博客蓝图没有 url_prefix 参数。因此 index 视图会用于 /，create 会用于 /create，
# 以此类推，但是 index 视图的端点会被定义为 blog.index 。


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'select p.id, title, body, created, author_id, username'
        '   from post p join user u on p.author_id = u.id'
        '   order by created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'insert into post (title, body, author_id)'
                '   values (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'select p.id, title, body, created, author_id, username'
        '   from post p join user u on p.author_id = u.id'
        '   where p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post
    # abort() 方法引发一个特殊的异常，返回一个 HTTP 状态码：
    # 404 “未找到”，403 “禁止访问”，401 “未授权”(重定向到登录页面返回)。
    # 另外还有一个可选参数用于显示出错信息，若不使用则返回缺省的出错信息。 
    # check_author 参数让函数可以在不检查作者的情况下获取 post。


@bp.route('/<int:id>/update', methods=('GET', 'POST'))    
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'update post set title = ?, body = ?'
                '   where id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)
    # <int:id> 中如果没有指定 int: 仅仅是 <id> 的话参数会被当作字符串传递。

    # 后续可以考虑使用一个视图和一个模板来同时完成 create 和 update 这两种功能。


@bp.route('/<int:id>/delete', methods=('POST',))    
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('delete from post where id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
    # 删除视图没有自己的模板，只处理 POST 方法并重定向到 index 视图。
