from flask import  redirect, render_template, url_for, request, flash, session

from filmcam.cams import blueprint, forms
from filmcam.cams.forms import CamCreateForm
from filmcam.cams.models import CamModel
from filmcam.utils import db
from filmcam.utils.forms import Field

@blueprint.get("/")
def index():
    """show only snippets created by the user who is currently logged in"""
    account_cams = []
    account_id = session.get("account_id")
    if account_id is not None:
        cams = CamModel(db.get_connection())
        account_cams = cams.account_cams(account_id)
    return render_template("/cams/index.jinja", cams=account_cams)

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

    title = request.form["title"]
    content = request.form["content"]

    img = request.files["img"]
    category = request.form["category"]
    
    # store the values received from the client into the form object.
    form = forms.CamCreateForm(title, content, img.filename, category)

    # See the Form definition in "filmcam/utils/forms.py".
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
    if not form.is_valid:
        return render_template("cams/create.jinja", form=form), 422

    cams = CamModel(db.get_connection())
    cams.insert(form.title, form.content, form.img, form.category, account_id) 

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

        


