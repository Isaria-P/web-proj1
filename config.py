from os import getcwd, path


# testing, and production configuration.
class Config:
    DATABASE_PATH = path.join(getcwd(), "instance", "db.sqlite")