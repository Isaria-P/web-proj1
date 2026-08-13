from flask import Blueprint

blueprint = Blueprint("cams", __name__, url_prefix="/cams")

from filmcam.cams import routes

