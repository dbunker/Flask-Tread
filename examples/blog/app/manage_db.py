import flask
from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

# only use for migrate
if __name__ == '__main__':
    curconfig = 'config.DevConfig'

    import mainapp
    mainapp.configure(curconfig)

    from mainapp import app
    from mainapp import db

    migrate = Migrate(app, db)

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    manager.run()
