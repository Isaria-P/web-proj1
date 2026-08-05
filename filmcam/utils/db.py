from sqlite3 import Connection, connect

from flask import current_app, g

class Model:
    def __init__(self, db: Connection):
        self.db = db

def get_connection() -> Connection:
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = connect(current_app.config["DATABASE_PATH"])
    return g.db


def close_connection(_e: BaseException | None = None) -> None:
    """Close the connection if the request is connected to the database."""
    db = g.pop("db", None)
    if db is not None:
        db.close()