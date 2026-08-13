from dataclasses import dataclass

from filmcam.utils.forms import Form


@dataclass
class LoginForm(Form):
    email: str = ""
    password: str = ""


@dataclass
class AccountCreateForm(Form):
    email: str = ""
    password: str = ""
