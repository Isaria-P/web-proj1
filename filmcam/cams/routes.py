from flask import  redirect, render_template, url_for, request

from filmcam.cams import blueprint, forms
from filmcam.cams.models import CamModel
from filmcam.utils import db
from filmcam.utils.forms import Field


@blueprint.get("/")
def index():
    cams = CamModel(db.get_connection())
    # return render_template("WELCOME")
    return render_template("/cams/index.jinja", cams=cams.latest())

@blueprint.get("/create")
def create():
    form = forms.CamCreateForm()
    return render_template("/cams/create.jinja", form=form)


@blueprint.post("/create")
def create_submit():
    
    title = request.form["title"]
    content = request.form["content"]
    img = request.form["img"]
    category = request.form["category"]
    

    # store the values received from the client into the form object.
    # This will allow us to validate each field and to
    # repopulate the form if there are errors.
    form = forms.CamCreateForm(title, content, img, category, author)

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
        Field.permitted_value(form.category, "category", ["35mm"," medium format", "large format"]),
        "format"
        "This field must be 35mm, medium format or large format",
    )
    
    
    if not form.is_valid:
        # The form object contains the errors because we used
        # "check_field" to validate the form. If there are errors, the
        # template will be able to show them.
        return render_template("cams/create.jinja", form=form), 422

    cams = CamModel(db.get_connection())
    cams.insert(form.title, form.content, form.img, form.category)
    return redirect(url_for("home"))