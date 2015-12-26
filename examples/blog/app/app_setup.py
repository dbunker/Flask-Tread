import flask
from flask.ext.migrate import Migrate
import argparse
import os

def get_config():

    parser = argparse.ArgumentParser()
    parser.add_argument('env', choices=['prod', 'qa', 'test', 'dev', 'env'])

    args = parser.parse_args()

    if args.env == 'prod':
        curconfig = 'config.ProdConfig'
    elif args.env == 'qa':
        curconfig = 'config.QAConfig'
    elif args.env == 'test':
        curconfig = 'config.TestConfig'
    elif args.env == 'dev':
        curconfig = 'config.DevConfig'
    elif args.env == 'env':
        curconfig = os.getenv('FLASK_ENV_OBJ')
    else:
        raise Exception('Invalid Config')

    if curconfig == None:
        raise Exception('Config cannot be null')

    return curconfig

# only use for migrate
if __name__ == '__main__':

    curconfig = get_config()

    import mainapp
    mainapp.configure(curconfig)

    from mainapp import app
    from mainapp import db

    migrate = Migrate(app, db)

    with app.app_context():
        flask.ext.migrate.upgrade()
