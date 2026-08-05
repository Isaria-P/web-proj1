from flask import  redirect, render_template, url_for

# from sqlite3 import connect

from filmcam.cams import blueprint
from filmcam.cams.models import CamModel
from filmcam.utils import db

@blueprint.get("/")
def index():
    cams = CamModel(db.get_connection())
    # return render_template("WELCOME")
    return render_template("/cams/index.jinja", cams=cams.latest())

@blueprint.post("/create")
def create():
    title = "O snail"
    content = "O snail\nClimb Mount Fuji,\nBut slowly, slowly!"
    img = "#.#"
    category = "Medium format"
    author = "Star Bright"
    cams = CamModel(db.get_connection())
    cams.insert(title, content, img, category, author, created)
    return redirect(url_for("home"))


