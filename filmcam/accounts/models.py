from dataclasses import dataclass

from werkzeug.security import generate_password_hash, check_password_hash

from filmcam.utils.db import Model
from filmcam.cams.models import Cam, CamModel

@dataclass
class Account:
    id: int
    email: str
    password: str
    cams: list[Cam]

class InvalidCredentialsError(Exception):
    pass 

class AccountModel(Model):
    def insert(self, email: str, password: str) -> int:
        
        cursor = self.db.execute(
            """
            INSERT INTO Accounts (email, password)
                VALUES (?, ?)
            """,
            (email, generate_password_hash(password)),
        )
        self.db.commit()

        id = cursor.lastrowid
        if not id:
            raise RuntimeError("insert failed: no lastrowid")
        return id

    def get(self, id: int) -> Account:
            email, password = self.db.execute(
                "SELECT email, password FROM Accounts WHERE id = ?", (id,)
            ).fetchone()
            cams = CamModel(self.db)
            return Account(id, email, password, cams.account_cams(id))
    
    def authenticate(self, email: str, password: str) -> Account:
        account = self.db.execute(
            "SELECT id, email, password FROM Accounts WHERE email = ?",   
        (email,),
        ).fetchone()

        # testing 
        print("DATABASE ACCOUNT:", account)

        if account is None or not check_password_hash(account[2], password):
            raise InvalidCredentialsError()
        
        id, email, password = account

        # testing 
        print("ACCOUNT ID FROM DATABASE:", id)

        cams = CamModel(self.db)
        return Account(id, email, password, cams.account_cams(id))

    def email_exists(self, email: str) -> bool:
        """Does the email exists."""
        account = self.db.execute(
            "SELECT * FROM Accounts WHERE email = ?", (email,)
        ).fetchone()
        return account is not None