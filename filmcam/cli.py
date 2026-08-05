import os

import click
from flask import current_app

from filmcam.utils.db import get_connection

@click.command 
def init() -> None:
    """Initialize the app (create database, etc.)"""

    os.makedirs(current_app.instance_path, exist_ok=True)
    open(current_app.config["DATABASE_PATH"], "a").close()

    with current_app.open_resource("schema.sql") as file:
        schema = file.read().decode("utf8")
        db = get_connection()
        db.executescript(schema)
    