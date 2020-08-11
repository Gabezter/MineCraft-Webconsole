from flask import Flask, url_for
from app.admin import admin_bp

'''
Basic File
'''


def app():
    app = Flask(__name__)

    app.register_blueprint(admin_bp)

    return app
