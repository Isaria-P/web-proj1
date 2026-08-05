from flask import Flask

from filmcam import cams, cli
from filmcam.utils import db

from config import Config

def create_app():
    # app = Flask(__name__)
    # app.register_blueprint(cams.blueprint)

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.cli.add_command(cli.init)
    app.register_blueprint(cams.blueprint)
    app.add_url_rule("/", endpoint="home", view_func=cams.routes.index)
    app.teardown_appcontext(db.close_connection)

    # app.config["DATABASE_PATH"] = "db.sqlite"
    # app.add_url_rule("/", endpoint="home", view_func=cams.routes.index)
    return app

    