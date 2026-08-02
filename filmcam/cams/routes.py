from flask import render_template

from filmcam.cams import blueprint

@blueprint.get("/")
def index():
    return render_template("/cams/index.jinja")
