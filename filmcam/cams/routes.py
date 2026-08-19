from flask import  redirect, render_template, url_for, request, flash, abort, current_app, session

from filmcam.cams import blueprint, forms
from filmcam.cams.forms import CamCreateForm
from filmcam.cams.models import CamModel
from filmcam.utils import db
from filmcam.utils.forms import Field

import os 
from werkzeug.utils import secure_filename

@blueprint.get("/")
def index():
    """Show all the cams in currently in the db."""
    cams = CamModel(db.get_connection())
    latest_cams = cams.latest()
    
    return render_template("/cams/index.jinja", cams=latest_cams)

@blueprint.post('/')
def upload_file():
    img_file = request.files["img"]

    if img_file.filename == "":
        flash("Please select an image.")
        return redirect(url_for('cam.index'))
    
    # filename = secure_filename(img_file.filename)

    # upload_path = os.path.join(
    #     current_app.config["UPLOAD_FOLDER"],
    #     filename
    # )
    # img_file.save(upload_file)

    return redirect(url_for("cams.index"))

@blueprint.get("/create")
def create():
    """Users who are not logged in can not be able to create a cam"""
    if session.get("account_id") is None:
        return redirect(url_for("accounts.login"))
    form = forms.CamCreateForm()
    return render_template("/cams/create.jinja", form=form)

@blueprint.post("/create")
def create_submit():
    """Handle cam creation from submission."""
    
    account_id = session.get("account_id")
    
    if account_id is None:
        return redirect(url_for("accounts.login"))

    # get data
    title = request.form["title"]
    content = request.form["content"]
    img = request.files["img"]
    category = request.form["category"]

    # make file safe 
    secure_img = secure_filename(img.filename)    

    # screate the form object
    form = forms.CamCreateForm(title, content, secure_img, category)

    # validate from the ".get("/create")"
    form.check_field(
        Field.not_blank(form.title), "title", "This field cannot be blank"
    )
    form.check_field(
        Field.max_chars(form.title, 100),
        "title",
        "This field cannot be more than 100 characters long",
    )
    form.check_field(
        Field.not_blank(form.content),
        "content",
        "This field cannot be blank",
    )
    form.check_field(
        Field.not_blank(form.img), "img", "This field cannot be blank"
    )
    form.check_field(
        Field.permitted_value(form.category, ["35 mm", "medium format", "large format"]),
        "category",
        "This field must be 35mm, medium format or large format",
    )
    # stop if validatefails
    if not form.is_valid:
        return render_template("cams/create.jinja", form=form), 422

    #  save Image
    #---------------------------
    # where image is stored  
    upload_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        secure_img
    )
    # url_path = upload_path.replace("\\", "/")

    # update path
    img.save(upload_path)

    # path that can be stored in db => uploads/OlympusOM-1OM-1n.jpg
    img_path = f"uploads/{secure_img}"

    cams = CamModel(db.get_connection())
    cams.insert(form.title, form.content, img_path, form.category, account_id) 

    # print("UPLOAD FOLDER:", current_app.config["UPLOAD_FOLDER"])
    # print("FOLDER EXISTS:", os.path.exists(current_app.config["UPLOAD_FOLDER"]))

    flash("Cam Post was successfully created!")
    return redirect(url_for("home"))

@blueprint.get("/view/<int:cam_id>")
def view(cam_id):
    """Show a cam with title, content, img, category."""
    cams = CamModel(db.get_connection())
    cam = cams.get_with_author(cam_id)
    if cam is None:
        flash("Cam Post not found.")
        return redirect(url_for("cams.index"))
    return render_template("cams/view.jinja", cam=cam)

@blueprint.get("/account/profile")
def account_profile():
    """Show only cams created by current user logged in."""
    account_cams = []

    account_id = session.get("account_id")

    if account_id is not None:
        cams = CamModel(db.get_connection())
        account_cams = cams.account_cams(account_id)
    cams = CamModel(db.get_connection())

        


