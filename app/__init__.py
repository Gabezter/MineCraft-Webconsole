from flask import Flask
from app.admin import admin_bp

'''
Basic File
'''


def app():
    app = Flask(__name__)
    from flask import Blueprint

    admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

    @admin_bp.route('/login', methods=['GET','POST'])
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

    @admin_bp.route('/logout', methods=['POST'])
    def logout():
        return ''

    app.register_blueprint(admin_bp)

    return app
