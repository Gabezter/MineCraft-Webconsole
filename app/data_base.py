import sqlite3
from flask import current_app, g, session
from app.util import hashify


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
    db = sqlite3.connect(
        current_app.config['DATABASE'],
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    pwd = hashify('ChangeMe1!')
    user_perms = {'create': True, 'assign': True, 'change': True,
                  'remove': True, 'reset': True, 'view': True, 'pause': True, 'admin': True}
    plugin_perms = {'upload': False, 'remove': False,
                    'e_config': False, 'admin': False}
    console_perms = {'start': False, 'stop': False,
                     'admin': False, 'cmd': False}
    create_user("admin", pwd, console_perms, plugin_perms, user_perms)


def init_app(app):
    app.teardown_appcontext(close_db)


def get_user(uid):
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE id = ?', uid).fetchone()
    id = user[0]
    username = user[1]
    valid = yn_to_boolean(user[3])
    fl = yn_to_boolean(user[4])
    return ((id, username, valid, fl))


def create_user(user, password, console_perms, plugin_perms, user_perms):
    db = get_db()
    try:
        db.execute('INSERT INTO user (username, password, valid, first_login) VALUES (?,?,?,?)',
                   (user, password, 'Y', 'Y'))
        db.commit()
    except Exception as e:
        print(e)
        return False
    return True


def get_console_permissions(user):
    db = get_db()
    c = db.cursor()
    user_id = 1
    perms = c.execute(
        'SELECT * FROM console_permissions WHERE user_id=?', user_id)

    stop = yn_to_boolean(perms[1])
    start = yn_to_boolean(perms[2])
    cmd = yn_to_boolean(perms[3])
    admin = yn_to_boolean(perms[4])

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
    perms = c.execute(
        'SELECT * FROM plugin_permissions WHERE user_id=?', user_id)

    upload = yn_to_boolean(perms[1])
    remove = yn_to_boolean(perms[2])
    e_config = yn_to_boolean(perms[3])
    admin = yn_to_boolean(perms[4])

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
    perms = c.execute(
        'SELECT * FROM console_permissions WHERE user_id=?', user_id)

    create = yn_to_boolean(perms[1])
    assign = yn_to_boolean(perms[2])
    change = yn_to_boolean(perms[3])
    remove = yn_to_boolean(perms[4])
    reset = yn_to_boolean(perms[5])
    view = yn_to_boolean(perms[6])
    pause = yn_to_boolean(perms[7])
    admin = yn_to_boolean(perms[8])

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


def set_user_permissions(user, create=False, assign=False, change=False, remove=False, reset=False, view=False, pause=False, admin=False):
    db = get_db()
    create = boolean_to_yn(create)
    change = boolean_to_yn(change)
    remove = boolean_to_yn(remove)
    reset = boolean_to_yn(reset)
    view = boolean_to_yn(view)
    pause = boolean_to_yn(pause)
    admin = boolean_to_yn(admin)
    assign = boolean_to_yn(assign)
    try:
        db.execute("INSERT INTO user_permissions (user_id, create_user, assign_perms, change_perms, remove_user, reset_pwd, view_users, pause_user, admin) VALUES (?,?,?,?,?,?,?,?,?)",
                   (get_user(user)[0], create, assign, change, remove, reset, view, pause, admin))
        db.commit()
    except Exception as e:
        print(e)
        return False
    return True


def set_plugin_permissions(user, upload=False, remove=False, e_config=False, admin=False):
    db = get_db()
    upload = boolean_to_yn(upload)
    e_config = boolean_to_yn(e_config)
    remove = boolean_to_yn(remove)
    admin = boolean_to_yn(admin)
    try:
        db.execute("INSERT INTO user_permissions (user_id, upload, remove, edit_config_files, admin) VALUES (?,?,?,?,?)",
                   (get_user(user)[0], upload, remove, e_config, admin))
        db.commit()
    except Exception as e:
        print(e)
        return False
    return True


def set_console_permissions(user, start=False, stop=False, admin=False, cmd=False):
    db = get_db()
    start = boolean_to_yn(start)
    stop = boolean_to_yn(stop)
    cmd = boolean_to_yn(cmd)
    admin = boolean_to_yn(admin)
    try:
        db.execute("INSERT INTO user_permissions (user_id, stop_perm, start_perm, execute_cmd, admin) VALUES (?,?,?,?,?)",
                   (get_user(user)[0], stop, start, cmd, admin))
        db.commit()
    except Exception as e:
        print(e)
        return False
    return True


def boolean_to_yn(obj):
    if obj == True:
        return 'Y'
    else:
        return 'N'


def yn_to_boolean(obj):
    if obj == 'Y':
        return True
    else:
        return False
