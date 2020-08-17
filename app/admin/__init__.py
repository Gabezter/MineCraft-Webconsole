"""Blueprint file for admin."""
from flask import Blueprint, url_for, render_template, make_response, redirect, session, request, current_app
import app.data_base as db
from app.utilities.util import hashify, get_password_type, check_password_strength
from app.utilities.util import Loggers as log
import app.utilities.plugins as plugins
import asyncio

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['GET', 'POST'])
def Login():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        valid = db.check_user(username, hashify(password))
        if valid == 1 or valid == 3:
            log.Main.error(username + " had a failed login attempt.")
            return page('e_login')
        elif valid == -1:
            session['username'] = username
            log.Main.info(username + " logged in for the first time.")
            return redirect(url_for('admin.First_Login'))
        elif valid == 2:
            log.Main.error(
                username + " tried to login, but account was paused at the time.")
            return page('invalid_user')
        else:
            session['username'] = username
            if db.get_console_permissions() and db.get_plugin_permissions() and db.get_user_permissions():
                log.Main.info(username + " successfully logged in.")
                return redirect(url_for('admin.Console'))
            else:
                session.clear()
                log.Main.error(
                    username + " tried to log in but an error occured with the permissions")
                return page('e_login')
    return page('login')


@admin_bp.route('/console')
@admin_bp.route('/')
def Console():
    if '/admin/login' in request.referrer:
        db.get_console_permissions()
        db.get_plugin_permissions()
        db.get_user_permissions()
    return page('console')


@admin_bp.route('/plugins')
def Plugins():
    return page('plugins')


@admin_bp.route('/configs')
def Configuration():
    return page('configs')


@admin_bp.route('/users')
def Users():
    return page('users')


@admin_bp.route('/user', methods=['GET', 'POST'])
def User():
    return page('user', user=session['username'])


@admin_bp.route('/logout')
def Logout():
    log.Main.info(session['username'] + " has succesfully logged out.")
    session.clear()
    return redirect(url_for('admin.Login'))


@admin_bp.route('/pwd-update', methods=['POST'])
def Update():
    if 'username' not in session:
        username = 'debug'
    else:
        username = session['username']
    if 'key' not in session:
        key = '33284'
    else:
        key = session['key']
    return redirect(url_for('admin.User', username=username))


@admin_bp.route('/first-login', methods=['GET', 'POST'])
def First_Login():
    if(request.method == 'POST'):
        pwd1 = hashify(request.form['password1'])
        pwd2 = hashify(request.form['password2'])
        if (pwd1 != pwd2):
            return page('e_nm_first_login')
        if (check_password_strength(request.form['password1']) == False):
            return page('e_first_login')
        db.update_password(session['username'], pwd1)
        if db.get_console_permissions() and db.get_plugin_permissions() and db.get_user_permissions():
            session['key'] = db.submit_key(session['username'])
            return redirect(url_for('admin.Console'))
        else:
            session.clear()
            return page('e_login')

    return page('first_login')


@admin_bp.route('/util/console/<string:command>', methods=['POST'])
def util_console(command):
    error = False
    if(command == 'start' or command == 'stop' or command == 'restart' or command == 'command'):
        if(request.json is not None):
            data = request.get_json()
            if "key" in data:
                key = data['key']
            else:
                error = True
            if "user" in data:
                user = data['user']
            else:
                error = True
            permission = db.get_console_permissions_user(user)
            if db.check_key(key=key, user=user) == False:
                return "logout"

            if command == 'start' and (permission[2] or permission[0]) and error == False:
                log.Main.info(user + ' just started the server!')
                return "Staring Server"
            else:
                if error:
                    log.Main.error(
                        user + ' just attempted to start the server. The start was blocked because there was an error. They were instructed to try again.')
                elif not (permission[2] or permission[0]):
                    log.Main.error(
                        user + ' just attempted to start the server. The start was blocked because they do not have permission.')
            if command == 'stop' and (permission[1] or permission[0]) and error == False:
                log.Main.info(user + ' just stopped the server!')
                return "Stopping Server"
            else:
                if error:
                    log.Main.error(
                        user + ' just attempted to stop the server. The stop was blocked because there was an error. They were instructed to try again.')
                elif not (permission[1] or permission[0]):
                    log.Main.error(
                        user + ' just attempted to stop the server. The stop was blocked because they do not have permission.')
            if command == 'restart' and ((permission[2] and permission[1]) or permission[0]) and error == False:
                log.Main.info(user + ' just restarted the server!')
                return "Restarting Server"
            else:
                if error:
                    log.Main.error(
                        user + ' just attempted to restart the server. The restart was blocked because there was an error. They were instructed to try again.')
                elif not ((permission[2] and permission[1]) or permission[0]):
                    log.Main.error(
                        user + ' just attempted to restart the server. The restart was blocked because they do not have permission.')
            if command == 'command' and (permission[3] or permission[0]) and error == False:
                log.Main.info(
                    user + ' just executed the following command: \n\t\t [\t' + data['command'] + '\t]')
                return "Executing Command"
            else:
                if error:
                    log.Main.error(
                        user +
                        ' just attempted to execute the folling command: \n\t\t [\t' +
                        data['command']
                        + '\t]\n The command was blocked because there was an error. They were instructed to try again.')
                elif not (permission[3] or permission[0]):
                    log.Main.error(
                        user +
                        ' just attempted to execute the folling command: \n\t\t [\t' +
                        data['command']
                        + '\t]\n The command was blocked because they do not have permission.')

        else:
            error = True
        if not error:
            return "Error has occured. Please logout and try again"
        else:
            if command == 'start':
                return "Staring Server"
            if command == 'stop':
                return "Stopping Server"
            if command == 'restart':
                return "Restarting Server"
            if command == 'command':
                return "Executing Command"
    return "UNKNOWN COMMAND"


@admin_bp.before_app_request
def load_logged_in_user():
    if(request.path != '/admin/login' and request.path != '/init' and request.path != '/dump'):
        if (current_app.config['DEBUG'] is not True):
            user = session.get('username')
            if user is None:
                session['username'] = None
                return redirect(url_for('admin.Login'))
    else:
        if (current_app.config['DEBUG'] is not True):
            user = session.get('username')
            if user is not None:
                return redirect(url_for("admin.Console"))


def page(page, **kargs):
    url_for("static", filename='header.css')
    url_for("static", filename='footer.css')
    if page == 'login':
        return login_page(p_invalid=False, p_error=False, p_logout=False)
    elif page == 'console':
        return console_page()
    elif page == 'users':
        return users_page()
    elif page == 'user':
        return user_page(kargs.get('user'))
    elif page == 'plugins':
        return plugins_page()
    elif page == 'configs':
        return configs_page()
    elif page == 'e_login':
        return login_page(p_error=True, p_logout=False, p_invalid=False)
    elif page == 'logout_login':
        url_for("static", filename='login.css')
        return login_page(p_error=False, p_logout=True, p_invalid=False)
    elif page == 'first_login':
        return first_login_page(p_not_match=False, p_error=False)
    elif page == 'e_first_login':
        return first_login_page(p_not_match=False, p_error=True)
    elif page == 'e_nm_first_login':
        return first_login_page(p_not_match=True, p_error=True)
    elif page == 'invalid_user':
        return login_page(p_error=True, p_logout=False, p_invalid=True)


@admin_bp.errorhandler(500)
def internal_error(e):
    return render_template('internal_error.html'), 500


def console_page():
    url_for("static", filename='console.css')
    if (current_app.config['DEBUG'] != True):
        m_start = session['console']['stop']
        m_stop = session['console']['start']
        m_console_execute = session['console']['cmd']
        m_admin = session['console']['admin']
    else:
        m_start = True
        m_stop = True
        m_console_execute = True
        m_admin = True
    if 'username' not in session:
        username = 'debug'
    else:
        username = session['username']
    if 'key' not in session:
        key = '33284'
    else:
        key = session['key']
    return make_response(render_template('console.html', console_execute=m_console_execute, start=m_start, stop=m_stop, admin=m_admin, username=username, key=key))


def plugins_page():
    url_for("static", filename='plugins.css')
    plugin_files = asyncio.run(plugins.get_plugins())
    if (current_app.config['DEBUG'] != True):
        m_admin = session['plugins']['admin']
        m_upload = session['plugins']['upload']
        m_remove = session['plugins']['remove']
        m_edit_configs = session['plugins']['edit_configs']
    else:
        m_admin = True
        m_upload = True
        m_remove = True
        m_edit_configs = True

    if 'username' not in session:
        username = 'debug'
    else:
        username = session['username']
    if 'key' not in session:
        key = '33284'
    else:
        key = session['key']
    return make_response(render_template('plugins.html', admin=m_admin, upload=m_upload, remove=m_remove, edit=m_edit_configs, username=username, key=key, plugins=plugin_files))


def configs_page():
    url_for("static", filename='configs.css')
    if (current_app.config['DEBUG'] != True):
        m_admin = session['plugins']['admin']
        m_edit_configs = session['plugins']['edit_configs']
    else:
        m_admin = True
        m_edit_configs = True

    if 'username' not in session:
        username = 'debug'
    else:
        username = session['username']
    if 'key' not in session:
        key = '33284'
    else:
        key = session['key']
    return make_response(render_template('configs.html', admin=m_admin, edit=m_edit_configs, username=username))


def users_page():
    url_for("static", filename='users.css')
    if (current_app.config['DEBUG'] != True):
        m_admin = session['user']['admin']
        m_create = session['user']['create']
        m_assign = session['user']['assign']
        m_change = session['user']['change']
        m_remove = session['user']['remove']
        m_reset = session['user']['reset']
        m_view = session['user']['view']
        m_pause = session['user']['pause']
    else:
        m_admin = True
        m_create = True
        m_assign = True
        m_change = True
        m_remove = True
        m_reset = True
        m_view = True
        m_pause = True
    if 'username' not in session:
        username = 'debug'
    else:
        username = session['username']
    if 'key' not in session:
        key = '33284'
    else:
        key = session['key']
    return make_response(render_template('users.html', admin=m_admin, create=m_create, assign=m_assign, change=m_change, remove=m_remove, reset=m_reset, view=m_view, pause=m_pause, username=username, users=db.list_users()))


def user_page(p_username):
    url_for("static", filename='user.css')
    if 'username' not in session:
        username = 'debug'
    else:
        username = session['username']
    if 'key' not in session:
        key = '33284'
    else:
        key = session['key']
    return make_response(render_template('user.html', username=username))


def login_page(p_error=False, p_logout=False, p_invalid=False):
    url_for("static", filename='login.css')
    return make_response(render_template('login.html', error=p_error, logout=p_logout, invalid=p_invalid))


def first_login_page(p_not_match=False, p_error=False):
    url_for("static", filename='first_login.css')
    password_type = get_password_type()
    m_strict = password_type[2]
    m_tight = password_type[1]
    m_loose = password_type[0]
    return make_response(render_template('first_login.html', error=p_error, not_match=p_error, strict=m_strict, tight=m_tight, loose=m_loose))
