from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
# 500 错误处理程序在引发数据库错误后调用，执行 session 回滚将会话重置为未发生错误之前的状态    
