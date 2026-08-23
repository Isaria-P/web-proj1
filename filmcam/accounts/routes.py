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
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    form = forms.AccountCreateForm(username=username, email=email, password=password)
    accounts = AccountModel(db.get_connection())


    # username validation
    form.check_field(
        Field.not_blank(username), "username", "This field cannot be blank"
        )
    form.check_field(
        Field.max_chars(username, 50), "username", "Username cannot exceed 50 characters"
        )
    form.check_field(
        " " not in username, "username", "Username cannot contain whitespace"
        )
    form.check_field(
        not accounts.username_exists(username), "username", "Username already exists"
        )

    # Email validation
    form.check_field(
        Field.not_blank(email), "email", "This field cannot be blank"
    )
    form.check_field(
        Field.is_valid_email(email), "email", "This is not a valid email"
    )
    form.check_field(
        not accounts.email_exists(email),
        "email",
        "This email already exists",
    )

    # Password validation
    form.check_field(
        Field.not_blank(password), "password", "This field cannot be blank"
    )
    form.check_field(
        Field.min_chars(password, 8),
        "password",
        "This field cannot be less than 8 characters long",
    )
    form.check_field(
        Field.max_chars(password, 20),
        "password",
        "Password cannot exceed 20 characters"
        )
    form.check_field(
        any(c.isupper() for c in password), 
        "password", 
        "Password must contain at least one uppercase letter"
        )
    form.check_field(
        any(c.isdigit() for c in password), 
        "password", 
        "Password must contain at least one digit"
        )

    if not form.is_valid:
        return render_template("accounts/create.jinja", form=form), 422

    accounts = AccountModel(db.get_connection())
    accounts.insert(username, email, password)

    flash("Account successfully created!")

    return redirect(url_for("accounts.login"))

@blueprint.get("/login")
def login(): 
    form = forms.LoginForm()
    return render_template("accounts/login.jinja", form=form)

@blueprint.post("/login")
def login_submit(): 
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    form = forms.LoginForm(email=email, password=password)
    accounts = AccountModel(db.get_connection())

    try:
        account = accounts.authenticate(form.email, form.password)
    except InvalidCredentialsError:
        form.add_non_field_error("Email or password is incorrect")
        return render_template("accounts/login.jinja", form=form)
    

    session["account_id"] = account.id
    flash("You've successfully logged in!")
    return redirect(url_for("home"))

@blueprint.get("/logout")
def logout(): 
    """Remove the user's account id from its session."""
    session.pop("account_id", None)
    flash("You've successfully logged out!")
    return redirect(url_for("home"))

@blueprint.get("/profile/<int:account_id>")
def profile(account_id):
    """Show a user's profile with their cams and comments."""
    account_id = session.get("account_id")

    if account_id is None:
        flash("You must be logged in to view yor profile.")
        return redirect(url_for("account.login"))

    account = AccountModel(db.get_connection()).get(account_id)

    return render_template("accounts/profile.jinja", account=account)

@blueprint.get("/account/profile")
def account_profile():
    """Show only cams created by current user logged in."""
    account_cams = []

    account_id = session.get("account_id")

    if account_id is not None:
        cams = CamModel(db.get_connection())
        account_cams = cams.account_cams(account_id)
    cams = CamModel(db.get_connection())

