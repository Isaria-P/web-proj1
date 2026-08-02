# from flask import Blueprint

# blueprint = Blueprint("cams", __name__, url_prefix="/cams")


# from filmcam.cams import routes

from flask import Flask

from filmcam import cams

# @app.get("/")
# def index():
#     # get data
#     #render template
#     return "Hello"
# register blueprints
def create_app():
    app = Flask(__name__)
    app.register_blueprint(cams.blueprint)
    app.add_url_rule("/", endpoint="home", view_func=cams.routes.index)
    return app

    