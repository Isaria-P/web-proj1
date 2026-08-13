from flask import Blueprint

blueprint = Blueprint("accounts", __name__, url_prefix="/accounts")


from filmcam.accounts import routes

