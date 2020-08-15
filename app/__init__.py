"""App Init File."""
from flask import Flask, redirect, url_for, render_template
from app.admin import admin_bp
import app.data_base as db


def app():
    app = Flask(__name__)
    app.config.from_pyfile('application.conf')
    app.register_blueprint(admin_bp)
    # db.init_app(app)

    @app.route('/init')
    def init():
        db.init()
        return redirect(url_for('admin.Login'))

    @app.route('/dump')
    def dump():
        db.getTableDump()
        return "Check Console"

    @app.route('/')
    @app.route('/index')
    @app.route('/login')
    def index():
        return redirect(url_for('admin.Login'))

    def not_found(e):
        return render_template('not_found.html'), 404

    def internal_error(e):
        return render_template('internal_error.html'), 500

    app.register_error_handler(404, not_found)
    app.register_error_handler(500, internal_error)
    admin_bp.register_error_handler(500, internal_error)
    return app
