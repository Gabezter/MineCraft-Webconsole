import sqlite3
from flask import current_app, g
import click


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init():
    db = get_db()
    with current_app.open_resource('sql/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_app(app):
    app.teardown_appcontext(close_db)


def get_console_permissions(user):
    restart = False
    stop = False
    start = False
    admin = False
    db = get_db()
    c = db.cursor()
    user_id = 1
    c.execute('SELECT * FROM console_permissions WHERE user_id=?', user_id)
    return ((admin, restart, stop, start))


def get_plugin_permissions(user):
    restart = False
    stop = False
    start = False
    admin = False
    db = get_db()
    c = db.cursor()
    user_id = 1
    c.execute('SELECT * FROM console_permissions WHERE user_id=?', user_id)
    return ((admin, restart, stop, start))


def get_user_permissions(user):
    restart = False
    stop = False
    start = False
    admin = False
    db = get_db()
    c = db.cursor()
    user_id = 1
    c.execute('SELECT * FROM console_permissions WHERE user_id=?', user_id)
    return ((admin, restart, stop, start))


def get_user(id):
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE id = ?', id).fetchone()
    return user
