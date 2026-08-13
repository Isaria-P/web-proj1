from flask import render_template, request, redirect, url_for, flash, session


from filmcam.accounts import blueprint, forms
from filmcam.accounts.models import AccountModel, InvalidCredentialsError
from filmcam.utils.forms import Field
from filmcam.utils import db


@blueprint.get("/create")
def create():
    form = forms.AccountCreateForm()
    return render_template("accounts/create.jinja", form=form)

@blueprint.post("/create")
def create_submit():
    email = request.form["email"]
    password = request.form["password"]
    form = forms.AccountCreateForm(email=email, password=password)
    accounts = AccountModel(db.get_connection())

    form.check_field(
        Field.not_blank(form.email), "email", "This field cannot be blank"
    )
    form.check_field(
        Field.is_valid_email(form.email), "email", "This is not a valid email"
    )
    form.check_field(
        not accounts.email_exists(form.email),
        "email",
        "This email already exists",
    )
    form.check_field(
        Field.not_blank(form.password), "password", "This field cannot be blank"
    )
    form.check_field(
        Field.min_chars(form.password, 8),
        "password",
        "This field cannot be less than 8 characters long",
    )

    if not form.is_valid:
        return render_template("accounts/create.jinja", form=form), 422

    accounts = AccountModel(db.get_connection())
    accounts.insert(form.email, form.password)

    flash("Account successfully created!")

    return redirect(url_for("accounts.login"))

@blueprint.get("/login")
def login(): 
    form = forms.LoginForm()
    return render_template("accounts/login.jinja", form=form)

@blueprint.post("/login")
def login_submit(): 
    email = request.form["email"]
    password = request.form["password"]

    form = forms.LoginForm(email, password)
    accounts = AccountModel(db.get_connection())

    try:
        account = accounts.authenticate(form.email, form.password)
    except InvalidCredentialsError:
        form.add_non_field_error("Email or password is incorrect")
        return render_template("accounts/login.jinja", form=form)
    
    session["account_id"] = account.id
    # testing below 
    print("SESSION AFTER LOGIN:", session)
    print("ACCOUNT ID:", account.id)
    
    flash("You've successfully logged in!")
    return redirect(url_for("home"))

@blueprint.get("/logout")
def logout(): 
    """Remove the user's account id from its session."""
    session.pop("account_id", None)
    flash("You've successfully logged out!")
    return redirect(url_for("home"))
