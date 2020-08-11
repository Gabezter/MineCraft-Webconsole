"""App Init File"""
from flask import Flask
from app.admin import admin_bp

def app():
    app = Flask(__name__)

    app.register_blueprint(admin_bp)

    return app
