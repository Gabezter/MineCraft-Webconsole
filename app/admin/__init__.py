"""Blueprint file for admin."""
from flask import Blueprint, url_for, render_template, make_response, redirect, session, g, request, current_app
import app.data_base as db
from app.util import hashify, get_password_type, check_password_strength

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['GET', 'POST'])
def Login():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        valid = db.check_user(username, hashify(password))
        if valid == 1 or valid == 3:
            return page('e_login')
        elif valid == -1:
            session['username'] = username
            return redirect(url_for('admin.First_Login'))
        elif valid == 2:
            return page('invalid_user')
        else:
            session['username'] = username
            if db.get_console_permissions() and db.get_plugin_permissions and db.get_user_permissions:
                return redirect(url_for('admin.Console'))
            else:
                return redirect(url_for('admin.Logout'))
    return page('login')


@admin_bp.route('/console')
@admin_bp.route('/')
def Console():
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


@admin_bp.route('/user', methods=['GET','POST'])
def User():
    return page('user', user=session['username'])


@admin_bp.route('/logout')
def Logout():
    session.clear()
    return redirect(url_for('admin.Login'))


@admin_bp.route('/pwd-update', methods=['POST'])
def Update():
    return redirect(url_for('admin.User', username=session['username']))


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
        return redirect(url_for('admin.Console'))

    return page('first_login')


@admin_bp.before_app_request
def load_logged_in_user():
    if(request.path != '/admin/login'):
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


def console_page():
    url_for("static", filename='console.css')
    if (current_app.config['DEBUG'] != True and session['permissions'] is not None):
        m_start = session['permissions']['console']['stop']
        m_stop = session['permissions']['console']['start']
        m_console_execute = session['permissions']['console']['cmd']
        m_admin = session['permissions']['console']['admin']
    else:
        m_start = True
        m_stop = True
        m_console_execute = True
        m_admin = True
    if 'username' not in session:
        username = 'debug'
    else:
        username = session['username']
    return make_response(render_template('console.html', console_execute=m_console_execute, start=m_start, stop=m_stop, admin=m_admin, username=username))


def plugins_page():
    url_for("static", filename='plugins.css')
    if (current_app.config['DEBUG'] != True and session['permissions'] is not None):
        m_admin = session['permissions']['plugins']['admin']
        m_upload = session['permissions']['plugins']['upload']
        m_remove = session['permissions']['plugins']['remove']
        m_edit_configs = session['permissions']['plugins']['edit_configs']
    else:
        m_admin = True
        m_upload = True
        m_remove = True
        m_edit_configs = True
    return make_response(render_template('plugins.html', admin=m_admin, upload=m_upload, remove=m_remove, edit=m_edit_configs, username=session['username']))


def configs_page():
    url_for("static", filename='configs.css')
    if (current_app.config['DEBUG'] != True and session['permissions'] is not None):
        m_admin = session['permissions']['plugins']['admin']
        m_edit_configs = session['permissions']['plugins']['edit_configs']
    else:
        m_admin = True
        m_edit_configs = True

    return make_response(render_template('configs.html', admin=m_admin, edit=m_edit_configs, username=session['username']))


def users_page():
    url_for("static", filename='users.css')
    if (current_app.config['DEBUG'] != True and session['permissions'] is not None):
        m_admin = session['permissions']['user']['admin']
        m_create = session['permissions']['user']['create']
        m_assign = session['permissions']['user']['assign']
        m_change = session['permissions']['user']['change']
        m_remove = session['permissions']['user']['remove']
        m_reset = session['permissions']['user']['reset']
        m_view = session['permissions']['user']['view']
        m_pause = session['permissions']['user']['pause']
    else:
        m_admin = True
        m_create = True
        m_assign = True
        m_change = True
        m_remove = True
        m_reset = True
        m_view = True
        m_pause = True
    return make_response(render_template('users.html', admin=m_admin, create=m_create, assign=m_assign, change=m_change, remove=m_remove, reset=m_reset, view=m_view, pause=m_pause, username=session['username']))


def user_page(p_username):
    url_for("static", filename='user.css')
    return make_response(render_template('user.html', username=session['username']))


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
