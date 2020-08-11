"""Blueprint file for admin"""
from flask import Blueprint, url_for, render_template, make_response

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['GET', 'POST'])
def Login():
    url_for("static", filename='login.css')
    return make_response(render_template('login.html'))

@admin_bp.route('/console')
def Console():
    url_for("static", filename='console.css')
    url_for("static", filename='header.css')
    url_for("static", filename='footer.css')
    return make_response(render_template('console.html'))

@admin_bp.route('/plugins')
def Plugins():
    return make_response(render_template('plugins.html'))

@admin_bp.route('/users')
def Users():
    return make_response(render_template('users.html'))

@admin_bp.route('/logout')
def Logout():  
    return make_response(render_template('logout.html'))

class Responses:
    @staticmethod
    def get_header(self):
        return render_template('header.html')
    @staticmethod
    def get_footer(self):
        return render_template('footer.html')

    @staticmethod
    def login(self):
        login = make_response(render_template('login.html'))
        return login 
