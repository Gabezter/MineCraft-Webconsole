"""App Init File."""
from flask import Flask, redirect, url_for, render_template, request
from app.admin import admin_bp
import app.data_base as db
import os
from logging.config import dictConfig
from app.utilities.util import Loggers as log


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

    @app.before_request
    def log_request():
        log.Request.info(request.remote_addr +
                         ' [' + request.method + '] requested ' + request.path)

    def not_found(e):
        return render_template('not_found.html'), 404

    def internal_error(e):
        log.Error.error(e.get_response())
        print(e)
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
                app.config['LOG_LOCATION'], 'details'), mode=0o666)
            os.mkdir(os.path.join(
                app.config['LOG_LOCATION'], 'details/main'), mode=0o666)
            os.mkdir(os.path.join(
                app.config['LOG_LOCATION'], 'details/debug'), mode=0o666)
            os.mkdir(os.path.join(
                app.config['LOG_LOCATION'], 'details/error'), mode=0o666)
            os.mkdir(os.path.join(
                app.config['LOG_LOCATION'], 'details/requests'), mode=0o666)

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
                    'format': '[%(asctime)s]: REQUEST: %(message)s'
                }
            },
            'handlers': {
                'default': {
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'formatter': 'default',
                    'filename': os.path.join(app.config['LOG_LOCATION'], 'full.log'),
                    'when': 'midnight'
                },
                'debug': {
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'formatter': 'default',
                    'filename': os.path.join(app.config['LOG_LOCATION'], 'details/debug/debug.log'),
                    'when': 'midnight'
                },
                'main': {
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'formatter': 'default',
                    'filename': os.path.join(app.config['LOG_LOCATION'], 'details/main/main.log'),
                    'when': 'midnight'
                },
                'request': {
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'formatter': 'default',
                    'filename': os.path.join(app.config['LOG_LOCATION'], 'details/requests/request.log'),
                    'when': 'midnight'
                },
                'error': {
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'formatter': 'request',
                    'filename': os.path.join(app.config['LOG_LOCATION'], 'details/error/error.log'),
                    'when': 'midnight'
                }
            },
            'loggers': {
                '': {
                    'level': 'DEBUG',
                    'handlers': ['default']
                },
                'main': {
                    'level': 'INFO',
                    'handlers': ['main', 'debug']
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
                    'handlers': ['error', 'main', 'debug']
                }
            }
        })
