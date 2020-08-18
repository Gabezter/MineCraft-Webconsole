import sqlite3
from flask import current_app, g, session, request
from app.utilities.util import hashify, generate_key, generate_temp_password
import datetime as dt
from app.utilities.util import Loggers as log


def get_db():
    db = sqlite3.connect(
        current_app.config['DATABASE'],
        detect_types=sqlite3.PARSE_DECLTYPES
    )

    return db


def close_db(e=None):
    db = g.db
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
                    'e_config': False, 'admin': True}
    console_perms = {'start': False, 'stop': False,
                     'admin': True, 'cmd': False}
    create_user("admin", pwd, console_perms, plugin_perms, user_perms)


def init_app(app):
    app.teardown_appcontext(close_db)


def get_user(username):
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE username = ?',
                      (username,)).fetchone()
    if user is not None:
        uid = user[0]
        username = user[1]
        valid = yn_to_boolean(user[3])
        fl = yn_to_boolean(user[4])
        return ((uid, username, valid, fl))
    else:
        return None


def check_user(usr, pwd):
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (usr,)).fetchone()
    if user is None:
        return 1
    if (user[3] == 'Y'):
        if (pwd == user[2]):
            if (user[4] == 'Y'):
                return -1
            else:
                return 0
        else:
            return 3
    else:
        return 2


def create_user(user, password, console_perms, plugin_perms, user_perms):
    db = get_db()
    try:
        db.execute('INSERT INTO user (username, password, valid, first_login) VALUES (?,?,?,?)',
                   (user, password, 'Y', 'Y'))
        db.commit()
        set_console_permissions(
            user=user, db=db, start=console_perms['start'], stop=console_perms['stop'], admin=console_perms['admin'], cmd=console_perms['cmd'])
        set_plugin_permissions(user=user, db=db, upload=plugin_perms['upload'], remove=plugin_perms['remove'],
                               e_config=plugin_perms['e_config'], admin=plugin_perms['admin'])
        set_user_permissions(user=user, db=db, create=user_perms['create'], assign=user_perms['assign'], change=user_perms['change'],
                             remove=user_perms['remove'], reset=user_perms['reset'], view=user_perms['view'], pause=user_perms['pause'], admin=user_perms['admin'])
        db.commit()
        if 'username' in session:
            log.Main.info(user + ' created by:' + session['username'])
        else:
            log.Main.info(user + ' was created')
    except Exception as e:
        log.Debug.debug(e)
        return False
    return True


def update_password(user, password):
    db = get_db()
    user_id = get_user(user)[0]
    if user_id is None:
        return False
    try:
        db.execute('UPDATE user SET password = ?, first_login = ? WHERE id = ?',
                   (password, 'N', user_id))
        db.commit()
        db.close()
        log.Main.info("Password has changed for user: " + user +
                      " from ip address: " + '[ ' + request.remote_addr + ' ]')
    except Exception as e:
        log.Debug.debug(e)
        return False
    return True


def get_console_permissions():
    user = session['username']
    return get_console_permissions_user(user)


def get_console_permissions_user(user):
    db = get_db()
    user_id = get_user(user)[0]
    if user_id is None:
        return False
    perms = db.execute(
        'SELECT * FROM console_permissions WHERE user_id=?', (user_id,)).fetchone()
    stop = yn_to_boolean(perms[1])
    start = yn_to_boolean(perms[2])
    cmd = yn_to_boolean(perms[3])
    admin = yn_to_boolean(perms[4])
    session['console'] = {
        'admin': admin,
        'stop': stop,
        'start': start,
        'cmd': cmd
    }
    return ((admin, stop, start, cmd))


def get_plugin_permissions():
    user = session['username']
    return get_plugin_permissions_user(user)


def get_plugin_permissions_user(user):
    db = get_db()
    c = db.cursor()
    user_id = get_user(user)[0]
    if user_id is None:
        return False
    perms = c.execute(
        'SELECT * FROM plugins_permissions WHERE user_id=?', (user_id,)).fetchone()

    upload = yn_to_boolean(perms[1])
    remove = yn_to_boolean(perms[2])
    e_config = yn_to_boolean(perms[3])
    admin = yn_to_boolean(perms[4])
    session['plugin'] = {
        'admin': admin,
        'upload': upload,
        'remove': remove,
        'edit_configs': e_config
    }

    return ((admin, upload, remove, e_config))


def get_user_permissions():
    user = session['username']
    return get_user_permissions_user(user)


def get_user_permissions_user(user):
    db = get_db()
    c = db.cursor()
    user_id = get_user(user)[0]
    if user_id is None:
        return False
    perms = c.execute(
        'SELECT * FROM user_permissions WHERE user_id=?', (user_id,)).fetchone()

    create = yn_to_boolean(perms[1])
    assign = yn_to_boolean(perms[2])
    change = yn_to_boolean(perms[3])
    remove = yn_to_boolean(perms[4])
    reset = yn_to_boolean(perms[5])
    view = yn_to_boolean(perms[6])
    pause = yn_to_boolean(perms[7])
    admin = yn_to_boolean(perms[8])
    session['user'] = {
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


def set_user_permissions(user, db, create=False, assign=False, change=False, remove=False, reset=False, view=False, pause=False, admin=False):
    create = boolean_to_yn(create)
    change = boolean_to_yn(change)
    remove = boolean_to_yn(remove)
    reset = boolean_to_yn(reset)
    view = boolean_to_yn(view)
    pause = boolean_to_yn(pause)
    admin = boolean_to_yn(admin)
    assign = boolean_to_yn(assign)
    user_id = get_user(user)[0]
    if user_id is None:
        return False
    try:
        db.execute("INSERT INTO user_permissions (user_id, create_user, assign_perms, change_perms, remove_user, reset_pwd, view_users, pause_user, admin) VALUES (?,?,?,?,?,?,?,?,?)",
                   (user_id, create, assign, change, remove, reset, view, pause, admin,))

        db.commit()
    except Exception as e:
        log.Debug.debug(e)
        return False
    return True


def set_plugin_permissions(user, db, upload=False, remove=False, e_config=False, admin=False):
    upload = boolean_to_yn(upload)
    e_config = boolean_to_yn(e_config)
    remove = boolean_to_yn(remove)
    admin = boolean_to_yn(admin)
    user_id = get_user(user)[0]
    if user_id is None:
        return False
    try:
        db.execute("INSERT INTO plugins_permissions (user_id, upload, remove, edit_config_files, admin) VALUES (?,?,?,?,?)",
                   (user_id, upload, remove, e_config, admin,))

        db.commit()
        # db.close()
    except Exception as e:
        log.Debug.debug(e)
        return False
    return True


def set_console_permissions(user, db, start=False, stop=False, admin=False, cmd=False):
    start = boolean_to_yn(start)
    stop = boolean_to_yn(stop)
    cmd = boolean_to_yn(cmd)
    admin = boolean_to_yn(admin)
    user_id = get_user(user)[0]
    if user_id is None:
        return False
    try:
        db.execute("INSERT INTO console_permissions (user_id, stop_perm, start_perm, execute_cmd, admin) VALUES (?,?,?,?,?)",
                   (user_id, stop, start, cmd, admin,))

        db.commit()
        # db.close()
    except Exception as e:
        log.Debug.debug(e)
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


def getTableDump():
    conn = get_db()
    cu = conn.cursor()
    users = 'Users\n------\n'
    usersp = 'Users Perms\n------\n'
    pluginp = 'Plugin Perms\n------\n'
    consolep = 'Console Perms\n------\n'
    keys = 'Keys\n------\n'
    print(users)
    for row in cu.execute('SELECT * FROM user'):
        print(row)
    print(usersp)
    for row in cu.execute('SELECT * FROM user_permissions'):
        print(row)
    print(pluginp)
    for row in cu.execute('SELECT * FROM plugins_permissions'):
        print(row)
    print(consolep)
    for row in cu.execute('SELECT * FROM console_permissions'):
        print(row)
    print(keys)
    for row in cu.execute('SELECT * FROM valid_keys'):
        print(row)

    conn.commit()
    return users + consolep + pluginp + usersp


def check_key(key, user):
    user_id = get_user(user)[0]
    db = get_db()
    c = db.execute(
        "SELECT expiration_date FROM valid_keys WHERE (user_key=? and id=?)", (key, user_id,)).fetchone()
    if c is None:
        return False
    expire = dt.datetime.fromisoformat(c[0])
    if dt.datetime.now(dt.timezone.utc) < expire:
        return True
    else:
        return False


def submit_key(user):
    key = generate_key()
    creation = dt.datetime.now(dt.timezone.utc)
    expiration = creation + dt.timedelta(minutes=30)
    db = get_db()
    user_id = get_user(user)[0]
    db.execute("INSERT INTO valid_keys (id, user_key, creation_date, expiration_date) VALUES (?,?,?,?)",
               (user_id, key, creation, expiration,))
    db.commit()
    return key


def list_users():
    db = get_db()
    try:
        users_sql = db.execute('SELECT username,valid FROM user ')
        users = []
        for user in users_sql:
            users.append((user[0], not yn_to_boolean(user[1])))
    except sqlite3.OperationalError as e:
        log.Error.error(e)
        users = False

    return users
