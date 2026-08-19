from flask import Flask

from filmcam import cams, cli, accounts
from filmcam.utils import db

from config import Config
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_object(Config)



    app.config["UPLOAD_FOLDER"] = "filmcam/static/uploads"
    app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png", ".jpeg"]

    app.cli.add_command(cli.init)

    app.register_blueprint(cams.blueprint)
    app.register_blueprint(accounts.blueprint)
    app.add_url_rule("/", endpoint="home", view_func=cams.routes.index)
    
    app.teardown_appcontext(db.close_connection)

    return app

    