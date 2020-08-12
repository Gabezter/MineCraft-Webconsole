"""App Init File."""
from flask import Flask, redirect, url_for
from app.admin import admin_bp
import app.data_base as db


def app():
    app = Flask(__name__)
    app.config.from_pyfile('application.conf')
    app.register_blueprint(admin_bp)
    db.init_app(app)

    @app.route('/init')
    def init():
        db.init()
        return redirect(url_for('admin.Login'))

    return app
