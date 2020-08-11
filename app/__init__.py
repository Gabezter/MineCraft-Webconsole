"""App Init File."""
from flask import Flask
from app.admin import admin_bp

def app():
    app = Flask(__name__)
    app.config.from_pyfile('application.cfg')
    app.register_blueprint(admin_bp)

    return app
