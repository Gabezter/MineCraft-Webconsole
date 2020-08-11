from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='admin')

@admin_bp.route('/login')
def login():
    return ''

@admin_bp.route('/console')
def console():
    return ''

@admin_bp.route('/plugins')
def plugins():
    return ''

@admin_bp.route('/users')
def users():
    return ''

@admin_bp.route('/logout')
def logout():
    return ''
