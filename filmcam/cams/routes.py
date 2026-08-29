from flask import  redirect, render_template, url_for, request, flash, abort, current_app, session

from filmcam.cams import blueprint, forms
from filmcam.cams.forms import CamCreateForm
from filmcam.cams.models import CamModel, CommentModel
from filmcam.accounts.models import AccountModel

from filmcam.utils import db
from filmcam.utils.forms import Field

import os 
from werkzeug.utils import secure_filename

@blueprint.get("/")
def index():
    """Show all the cams in currently in the db."""
    conn = db.get_connection()
    cams_model = CamModel(conn)
    accounts_model = AccountModel(conn)

    # Get all stories, newest first
    all_cams = cams_model.latest()

    # Attach author usernames for display
    # for cam in all_cams:
    #     author = accounts_model.get(cam.author_id)
    #     cam.author_username = author.username
    
    return render_template("/cams/index.jinja", cams=all_cams)

@blueprint.post('/')
def upload_file():
    img_file = request.files["img"]

    if img_file.filename == "":
        flash("Please select an image.")
        return redirect(url_for('cam.index'))
    return redirect(url_for("cams.index"))

@blueprint.get("/create")
def create():
    """Users who are not logged in can not be able to create a cam"""
    if session.get("account_id") is None:
        flash("You must be logged in to create a cam post.")
        return redirect(url_for("accounts.login"))
    form = forms.CamCreateForm()
    return render_template("/cams/create.jinja", form=form)

@blueprint.post("/create")
def create_submit():
    """Handle cam creation from submission."""
    account_id = session.get("account_id")
    if account_id is None:
        flash("You must be logged in to create a cam.")
        return redirect(url_for("accounts.login"))

    # get data
    title = request.form["title"]
    content = request.form["content"]
    img = request.files["img"]
    category = request.form["category"]

    print("CATEGORY FROM FORM:", category)
    
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

    # update path
    img.save(upload_path)

    # path that can be stored in db => uploads/OlympusOM-1OM-1n.jpg
    img_path = secure_img

    # insert cam
    cams = CamModel(db.get_connection())

    cams.insert(form.title, form.content, img_path, form.category, account_id) 

    # print("UPLOAD FOLDER:", current_app.config["UPLOAD_FOLDER"])
    # print("FOLDER EXISTS:", os.path.exists(current_app.config["UPLOAD_FOLDER"]))

    flash("Cam Post was successfully created!")
    return redirect(url_for("home"))

@blueprint.route("/view/<int:cam_id>", methods=["GET", "POST"])
def view(cam_id):
    """Show a cam with title, content, img, category."""
    cams = CamModel(db.get_connection())
    comments_model = CommentModel(db.get_connection())
    cam = cams.get_with_author(cam_id)

    if cam is None:
        flash("Cam Post not found.")
        return redirect(url_for("cams.index"))

    # handle comment submission
    if request.method == "POST":
        account_id = session.get("account_id")
        if account_id is None:
            flash("You must be logged in to comment")
            return redirect(url_for("accounts.login"))
        body = request.form.get("body", "").strip()
        if not body:
            flash("Comment cannot be blank.")
        elif len(body) > 10000:
            flash("Comment cannot exceed 10,000 characters.")
        else:
            comments_model.insert(
                body,
                cam_id,
                account_id
            )
            flash("Comment added successfully!!!")
            return redirect(url_for("cams.view", cam_id=cam_id))
    comments = comments_model.for_cam(cam_id)
    return render_template("cams/view.jinja", cam=cam, comments=comments)

@blueprint.get("/edit/<int:cam_id>")
def edit(cam_id):

    account_id = session.get("account_id")
    if account_id is None:
        flash("You must be logged in to edit a cam post.")
        return redirect(url_for("accounts.login"))
    cams = CamModel(db.get_connection())
    cam = cams.get_with_author(cam_id)

    return render_template("cams/edit.jinja", cam=cam)

@blueprint.post("/edit/<int:cam_id>")
def edit_submit(cam_id):
    # check login
    account_id = session.get("account_id")

    if account_id is None:
        flash("You must be logged in to create a cam post.")
        return redirect(url_for("accounts.login"))

    # get cam db connection
    cams = CamModel(db.get_connection())
    cam = cams.get_with_author(cam_id)

    # conditional does cam exist?
    if cam is None:
        abort(404)

    if cam.author_id != account_id:
        print("❌ USER DOES NOT OWN THIS POST")
        abort(403)
        
    # get form data
    title = request.form["title"]
    content = request.form["content"]
    category = request.form["category"]

    # get image
    img = request.files.get("img")  

    # orgignal img
    img_path = cam.img

    # conditional if an img gets selected
    if img and img.filename:

        secure_img = secure_filename(img.filename)
        upload_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            secure_img
        )

        img.save(upload_path)
        img_path = secure_img
    else:
        img_path = cam.img
    
    # update db
    cams.update(cam_id, title, content, category, img_path)

    flash("Cam post updated successfully!!!")

    return redirect(url_for("cams.view", cam_id=cam_id))


@blueprint.post("/delete/<int:cam_id>")
def delete(cam_id):
    account_id = session.get("account_id")
    
    if account_id is None:
        flash("You must be logged in to delete a cam post.")
        return redirect(url_for("accounts.login"))

    cams = CamModel(db.get_connection())
    cam = cams.get(cam_id)

    # Cam doesn't exist
    if cam is None:
        flash("Cam post not found.")
        return redirect(url_for(
            "accounts.profile",
            account_id=account_id
        ))

    # Check that the logged-in user owns the post
    if cam.author_id != account_id:
        flash("You can only delete your own cam posts.")
        return redirect(url_for(
            "accounts.profile",
            account_id=account_id
        ))

    # Delete  post
    cams.delete(cam_id)

    flash("Cam post deleted successfully!")

    return redirect(url_for(
        "accounts.profile",
        account_id=account_id
    ))


@blueprint.get("/category/<category>")
def category(category):
    cams = CamModel(db.get_connection())

    category_cam = cams.get_by_category(category)

    return render_template(
        "cams/category.jinja", 
        cams=category_cam,
        category=category
    )

@blueprint.get("/comment/edit/<int:comment_id>")
def comment_edit(comment_id):

    # Check login
    account_id = session.get("account_id")

    if account_id is None:
        flash("You must be logged in to edit a comment")
        return redirect(url_for("accounts.login"))

    # get comment
    comments_model = CommentModel(db.get_connection())
    comment = comments_model.get_with_author(comment_id)

    if comment is None:
        abort(404)

    # condidional check if user logged in owns comment
    if comment.author_id != account_id:
        abort(401)

    return render_template(
        "cams/comment_edit.jinja", comment=comment
    )


@blueprint.post("/comment/edit/<int:comment_id>")
def comment_edit_submit(comment_id):
    account_id = session.get("account_id")

    if account_id is None:
        flash("You must be logged in to edit post")
        return redirect(url_for("accounts.login"))

    comments_model = CommentModel(db.get_connection())
    comment = comments_model.get_with_author(comment_id)

    if comment is None:
        abort(404)

    # condidional check if user logged in owns comment
    if comment.author_id != account_id:
        abort(403)

    # get new comment 
    body = request.form["body"]

    if not body.strip():
        flash("Comment cannot be empty.")
        return render_template("cams/comment_edit.jinja", comment=comment), 422

    comments_model.update_comment(comment_id, body)
    flash("Commment update successfully!")

    return redirect(url_for(
        "cams.view", cam_id=comment.cam_id
    ))
    
@blueprint.post("/comment/delete/<int:comment_id>")
def comment_delete(comment_id):

    account_id = session.get("account_id")
    if account_id is None:
        flash("You must be logged in to delete a comment.")
        return redirect(url_for("accounts.login"))

    comments_model = CommentModel(db.get_connection())
    comment = comments_model.get_with_author(comment_id)

    if comment is None:
        abort(404)

    # Make sure the logged-in user owns the comment
    if comment.author_id != account_id:
        abort(403)

    comments_model.delete_comment(comment_id)
    flash("Comment deleted successfully!")

    return redirect(url_for(
        "cams.view",
        cam_id=comment.cam_id
    ))


