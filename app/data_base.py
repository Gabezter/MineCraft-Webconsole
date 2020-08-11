import sqlite3
from flask import current_app, g, session
import click
import hashlib


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


def get_user(id):
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE id = ?', id).fetchone()
    id = user[0]
    username = user[1]
    if(user[3] == 'Y'):
        valid = True
    else:
        valid = False
    if(user[4] == 'Y'):
        fl = True
    else:
        fl = False
    return ((id, username, valid, fl))


def create_user(user, password):
    db = get_db()
    try:
        db.execute('INSERT INTO user (username, password, valid, first_login) VALUES (?,?,?,?)', user, password, 'Y', 'Y')
        db.commit()
    except:
        return (False)
    return True


def get_console_permissions(user):
    db = get_db()
    c = db.cursor()
    user_id = 1
    console_perms = c.execute(
        'SELECT * FROM console_permissions WHERE user_id=?', user_id)
    c.commit()

    if (console_perms[1] == 'Y'):
        stop = True
    else:
        stop = True
    if (console_perms[2] == 'Y'):
        start = False
    else:
        start = False
    if (console_perms[3] == 'Y'):
        cmd = True
    else:
        cmd = False
    if (console_perms[4] == 'Y'):
        admin = True
    else:
        admin = False

    session['permissions']['console'] = {
        'admin': admin,
        'stop': stop,
        'start': start,
        'cmd': cmd
    }

    return ((admin, stop, start, cmd))


def get_plugin_permissions(user):
    db = get_db()
    c = db.cursor()
    user_id = 1
    console_perms = c.execute(
        'SELECT * FROM plugin_permissions WHERE user_id=?', user_id)
    c.commit()

    if (console_perms[1] == 'Y'):
        upload = True
    else:
        upload = False
    if (console_perms[2] == 'Y'):
        remove = True
    else:
        remove = False
    if (console_perms[3] == 'Y'):
        e_config = True
    else:
        e_config = False
    if (console_perms[4] == 'Y'):
        admin = True
    else:
        admin = False

    session['permissions']['plugin'] = {
        'admin': admin,
        'upload': upload,
        'remove': remove,
        'edit_configs': e_config
    }

    return ((admin, upload, remove, e_config))


def get_user_permissions(user):
    db = get_db()
    c = db.cursor()
    user_id = 1
    console_perms = c.execute(
        'SELECT * FROM console_permissions WHERE user_id=?', user_id)
    c.commit()

    if (console_perms[1] == 'Y'):
        create = True
    else:
        create = False
    if (console_perms[2] == 'Y'):
        assign = True
    else:
        assign = False
    if (console_perms[3] == 'Y'):
        change = True
    else:
        change = False
    if (console_perms[4] == 'Y'):
        remove = True
    else:
        remove = False
    if (console_perms[5] == 'Y'):
        reset = True
    else:
        reset = False
    if (console_perms[6] == 'Y'):
        view = True
    else:
        view = False
    if (console_perms[7] == 'Y'):
        pause = True
    else:
        pause = False
    if (console_perms[8] == 'Y'):
        admin = True
    else:
        admin = False

    session['permissions']['user'] = {
        'admin': admin,
        'create': create,
        'assign': assign,
        'change': change,
        'remove': remove,
        'reset': reset,
        'view': view,
        'pause': pause
    }

    return ((admin, create, assign, change, remove, reset, view, pause))


def set_user_permissions(user, create, assign, change, rmeove, reset, view, pause, admin):
    pass


def set_plugin_permissions(user, upload, remove, e_config, admin):
    pass


def set_console_permissions(user, start, stop, admin, cmd):
    pass
