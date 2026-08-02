from flask import Blueprint

blueprint = Blueprint("cams", __name__, url_prefix="/cams")
# every route for this blueprint starts with snippets
# /cams/<id>
# /cams - for all 
# /cams/create
# /cams/delete

from filmcam.cams import routes

