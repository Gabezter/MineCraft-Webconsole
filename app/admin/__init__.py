'''
Blueprint file for admin 
'''
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login')
class Login:
    def get(self):
        return ''
    def post(self):
        return ''

@admin_bp.route('/console')
class Console:
    def get(self):
        return ''

@admin_bp.route('/plugins')
class Plugins:
    def get(self):
        return ''

@admin_bp.route('/users')
class Users:
    def get(self):
        return ''

@admin_bp.route('/logout')
class Logout:
    def post(self):    
        return ''
