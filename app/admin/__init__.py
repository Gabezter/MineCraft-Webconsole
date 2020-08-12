"""Blueprint file for admin."""
from flask import Blueprint, url_for, render_template, make_response, redirect, session, g, request, current_app
import app.data_base as db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['GET', 'POST'])
def Login():
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


@admin_bp.before_app_request
def load_logged_in_user():
    if(request.path != '/admin/login' and current_app.config['DEBUG'] is not True):
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
            return redirect(url_for('admin.Login'))
        else:
            g.user = db.get_user(user_id)


def page(page):
    url_for("static", filename='header.css')
    url_for("static", filename='footer.css')
    if page == 'login':
        url_for("static", filename='login.css')
        return make_response(render_template('login.html', error=True, logout=True))
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
        return make_response(render_template('login.html', error=True, logout=False) )
    elif page == 'logout_login':
        url_for("static", filename='login.css')
        return make_response(render_template('login.html', error=False, logout=True) )
