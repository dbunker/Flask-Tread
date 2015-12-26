import mainapp
import flask
import app_setup

if __name__ == '__main__':

    curconfig = app_setup.get_config()
    mainapp.configure(curconfig)
    mainapp.runApp()
