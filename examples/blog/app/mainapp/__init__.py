import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
import flask.ext.migrate
from werkzeug import SharedDataMiddleware
import os

def configure(configObj):

    global app
    global db

    app = Flask(__name__)
    app.config.from_object(configObj)

    db = SQLAlchemy(app)

    handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.logger.info('App configured for environment: ' + app.config['ENV_NAME'])

    from mainapp import views, models

def upgradeDB():
    Migrate(app, db)
    with app.app_context():
        flask.ext.migrate.upgrade()

def runApp():
    app.logger.info('App started')
    app.run()
    