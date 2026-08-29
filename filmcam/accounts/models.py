from dataclasses import dataclass

from werkzeug.security import generate_password_hash, check_password_hash

from filmcam.utils.db import Model
from filmcam.cams.models import Cam, CamModel, CommentModel

@dataclass
class Account:
    id: int
    username: str
    email: str
    password: str
    cams: list[Cam]
    comments: list

class InvalidCredentialsError(Exception):
    """Raised when an account fails authentication due to invalid email or password."""
    pass 

class AccountModel(Model):
    def insert(self,  username: str, email: str, password: str) -> int:
        
        cursor = self.db.execute(
            """
            INSERT INTO Accounts (username, email, password)
                VALUES (?, ?, ?)
            """,
            (username, email, generate_password_hash(password)),
        )
        self.db.commit()

        id = cursor.lastrowid
        if not id:
            raise RuntimeError("insert failed: no lastrowid")
        return id

    def get(self, accounts_id: int) -> Account | None:
            row = self.db.execute(
                """
                SELECT id, username, email, password 
                FROM Accounts 
                WHERE id = ?
                """,
                (accounts_id,)
            ).fetchone()
            if row is None:
                return None

            id, username, email, password = row
            cams = CamModel(self.db).account_cams(id)
            comments = CommentModel(self.db).account_comments(id)
            return Account(id=id, username=username, email=email, password=password, cams=cams, comments=comments)
    
    def authenticate(self, email: str, password: str) -> Account:
        row = self.db.execute(
            "SELECT id, username, email, password FROM Accounts WHERE email = ?",   
        (email, )
        ).fetchone()

        # testing 
        

        if row is None or not check_password_hash(row[3], password):
            raise InvalidCredentialsError()
        
        id, username, email, password = row
        cams = CamModel(self.db).account_cams(id)
        comments = CommentModel(self.db).account_comments(id)
        # testing 
        # print("ACCOUNT ID FROM DATABASE:", id)

        return Account(id, username, email, password, cams, comments)

    def email_exists(self, email: str) -> bool:
        """Does the email exists."""
        account = self.db.execute(
            "SELECT * FROM Accounts WHERE email = ?", (email,)
        ).fetchone()
        return account is not None
    
    def username_exists(self, username: str) -> bool:
        account = self.db.execute(
            "SELECT * FROM Accounts WHERE username = ?", (username,)
        ).fetchone()
        return account is not None