"""App Init File."""
from flask import Flask, redirect, url_for, render_template
from app.admin import admin_bp
import app.data_base as db
import os
from logging.config import dictConfig
from app.utilities.util import RequestFormatter


def app():
    app = Flask(__name__)
    app.config.from_pyfile('application.conf')
    app.register_blueprint(admin_bp)

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

    setup_logging(app)

    return app


def setup_logging(app):
    if app.config['LOGGING']:
        try:
            os.mkdir(app.config['LOG_LOCATION'], mode=0o666)
            os.mkdir(os.path.join(
                app.config['LOG_LOCATION'], 'main'), mode=0o666)
            os.mkdir(os.path.join(
                app.config['LOG_LOCATION'], 'debug'), mode=0o666)
            os.mkdir(os.path.join(
                app.config['LOG_LOCATION'], 'error'), mode=0o666)
        except FileExistsError as e:
            pass
        except Exception as e:
            print(e)

    dictConfig({
        'version': 1,
        'formatters': {
            'error': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
            'default': {
                'format': '[%(asctime)s] %(levelname)s: %(message)s',
            },
            'request': {
                '()': RequestFormatter('[%(asctime)s] %(remote_addr)s requested %(url)s')
            }
        },
        'handlers': {
            'debug': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'default',
                'filename': os.path.join(app.config['LOG_LOCATION'], 'debug/debug.log'),
                'propagate': 0,
                'when': 'midnight'
            },
            'main': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'default',
                'filename': os.path.join(app.config['LOG_LOCATION'], 'main/main.log'),
                'propagate': 0,
                'when': 'midnight'
            },
            'request': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'default',
                'filename': os.path.join(app.config['LOG_LOCATION'], 'main/reqest.log'),
                'propagate': 0,
                'when': 'midnight'
            },
            'error': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'default',
                'filename': os.path.join(app.config['LOG_LOCATION'], 'error/error.log'),
                'propagate': 0,
                'when': 'midnight'
            }
        },
        'loggers': {
            '': {
                'level': 'INFO',
                'handlers': ['main']
            },
            'debug': {
                'level': 'DEBUG',
                'handlers': ['debug']
            },
            'request': {
                'level': 'INFO',
                'handlers': ['request']
            },
            'error': {
                'level': 'ERROR',
                'handlers': ['error']
            }
        }
    })
