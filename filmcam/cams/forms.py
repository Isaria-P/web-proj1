from dataclasses import dataclass

from filmcam.utils.forms import Form


@dataclass
class SnippetCreateForm(Form):
    # define the form's fields and their default value.
    title: str = ""
    content: str = ""
    img: str = ""
    category: str = ""
