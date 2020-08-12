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
            g.user = username
            if db.get_console_permissions() and db.get_plugin_permissions and db.get_user_permissions:
                return redirect(url_for('admin.Console'))
            else:
                return redirect(url_for('admin.Logout'))
    return page('login')


@admin_bp.route('/console')
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


@admin_bp.route('/logout')
def Logout():
    session.clear()
    return redirect(url_for('admin.Login'))


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
    if(request.path != '/admin/login' and current_app.config['DEBUG'] is not True):
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
            return redirect(url_for('admin.Login'))
        else:
            g.user = db.get_user(user_id)

# TODO Set permissions

def page(page):
    url_for("static", filename='header.css')
    url_for("static", filename='footer.css')
    if page == 'login':
        url_for("static", filename='login.css')
        return make_response(render_template('login.html', error=False, logout=False))
    elif page == 'console':
        url_for("static", filename='console.css')
        return make_response(render_template('console.html', console_execute=False))
    elif page == 'users':
        return make_response(render_template('users.html'))
    elif page == 'plugins':
        return make_response(render_template('plugins.html'))
    elif page == 'configs':
        return make_response(render_template('configs.html'))
    elif page == 'e_login':
        url_for("static", filename='login.css')
        return make_response(render_template('login.html', error=True, logout=False))
    elif page == 'logout_login':
        url_for("static", filename='login.css')
        return make_response(render_template('login.html', error=False, logout=True))
    elif page == 'first_login':
        url_for("static", filename='first_login.css')
        password_type = get_password_type()
        return make_response(render_template('first_login.html', not_match=False, strict=password_type[2], tight=password_type[1], loose=password_type[0]))
    elif page == 'e_first_login':
        url_for("static", filename='first_login.css')
        password_type = get_password_type()
        return make_response(render_template('first_login.html', error=True, not_match=False, strict=password_type[2], tight=password_type[1], loose=password_type[0]))
    elif page == 'e_nm_first_login':
        url_for("static", filename='first_login.css')
        password_type = get_password_type()
        return make_response(render_template('first_login.html', error=True, not_match=True, strict=password_type[2], tight=password_type[1], loose=password_type[0]))
    elif page == 'invalid_user':
        url_for("static", filename='login.css')
        return make_response(render_template('login.html', error=True, logout=False, invalid=True))
