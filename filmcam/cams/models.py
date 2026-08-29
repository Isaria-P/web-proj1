from dataclasses import dataclass
from datetime import datetime, timezone

from filmcam.utils.db import Model

@dataclass
class Cam:
    id: int
    title: str
    content: str
    img: str
    category: str
    author_id: int
    created: datetime
    author_username: str | None = None

@dataclass
class Comment:
    id: int
    body: str
    created: str
    author_id: int
    cam_id: int
    author_username: str | None = None

class CamModel(Model):
    def insert(
            self, title: str, content: str, img: str, category: str, author_id: int
        ) -> int:
        created = datetime.now(timezone.utc)
        cursor = self.db.execute(
            """
            INSERT INTO Cams (title, content, img, category, author, created) 
                VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title, content, img, category, author_id, created),
        )
        self.db.commit()
        cam_id = cursor.lastrowid
        if not cam_id:
            raise RuntimeError("insert failed: no lastrowid")
        return cam_id

    def get(self, cam_id: int) -> Cam | None:
        row = self.db.execute(
            """
            SELECT 
                Cams.id, 
                Cams.title, 
                Cams.content, 
                Cams.img, 
                Cams.category, 
                Cams.author As author_id,
                Cams.created,
                Accounts.username As author_username
            FROM Cams
            JOIN Accounts
                ON Cams.author = Accounts.id
            WHERE Cams.id = ?
            """,
            (cam_id,)
        ).fetchone()
        if not row:
            return None
        return Cam(*row)
    
    def account_cams(self, account_id: int) -> list[Cam]:
        rows = self.db.execute(
            """
            SELECT 
                c.id, 
                c.title, 
                c.content, 
                c.img, 
                c.category, 
                c.author AS author_id,
                c.created,
                a.username AS author_username
            FROM Cams c
            JOIN Accounts a ON c.author = a.id
            WHERE c.author = ?
            ORDER BY c.created DESC
            """,
            (account_id,),
        ).fetchall()
        return [Cam(*rows) for rows in rows]

    def latest(self) -> list[Cam]:
        rows = self.db.execute(
            """
            SELECT 
                Cams.id, 
                Cams.title, 
                Cams.content, 
                Cams.img, 
                Cams.category, 
                Cams.author AS author_id,
                Cams.created, 
                Accounts.username As author_username
            FROM Cams
            JOIN Accounts
                On Cams.author = Accounts.id
            ORDER BY Cams.created DESC
            """
        ).fetchall()
        return [Cam(*row) for row in rows]

    def get_with_author(self, cam_id: int) -> Cam | None:
        """retreive author for edit/delete"""
        row = self.db.execute(
            """
            SELECT 
                c.id,
                c.title, 
                c.content, 
                c.img, 
                c.category, 
                c.author AS author_id,
                c.created,
                a.username AS author_username
            FROM Cams c
            JOIN Accounts a 
                ON c.author = a.id
            WHERE c.id = ?
            """,
            (cam_id,)
        ).fetchone()
        if not row:
            return None
        return Cam(*row) 
    # get comments w/ author username
    # def get_comments_with_authors(self, cam_id: int) -> list[Comment]:
    #     rows = self.db.execute(
    #         """
    #             SELECT 
    #                 c.id, 
    #                 c.body, 
    #                 c.created, 
    #                 c.author_id, 
    #                 c.cam_id, 
    #                 a.username AS author_username
    #             FROM Comments c
    #             JOIN Accounts a 
    #                 ON c.author_id = a.id
    #             WHERE c.cam_id = ?
    #             ORDER BY c.created ASC
    #         """,
    #         (cam_id,)
    #     ).fetchall()
    #     return [Comment(*row) for row in rows]

    #add comment
    # def add_comment(self, cam_id: int, author_id: int, body: str) -> int:
    #     created = datetime.utcnow()
    #     cursor = self.db.execute(
    #         """
    #         INSERT INTO Comments (body, cam_id, author_id, created)
    #         VALUES (?, ?, ?, ?)
    #         """,
    #         (body, cam_id, author_id, created)
    #     )
    #     self.db.commit()
    #     return cursor.lastrowid

    def update(self, cam_id: int, title: str, content: str, category: str, img: str) -> None:
        self.db.execute(
            """
            UPDATE Cams
            SET title = ?,
                content = ?,
                category = ?,
                img = ?
            WHERE id = ?
            """,
            (title, content, category, img, cam_id)
        )
        self.db.commit()

    def delete(self, cam_id: int) -> None:
        self.db.execute(
            """
            DELETE FROM Cams
            WHERE id =?
            """,
            (cam_id,)
        )
        self.db.commit()

    def get_by_category(self, category: str) -> list[Cam]:
        rows = self.db.execute(
            """
            SELECT 
                Cams.id, 
                Cams.title, 
                Cams.content, 
                Cams.img, 
                Cams.category, 
                Cams.author AS author_id,
                Cams.created, 
                Accounts.username AS author_username
            FROM Cams
            JOIN Accounts 
                ON Cams.author = Accounts.id
            WHERE Cams.category = ?
            ORDER BY Cams.created DESC
            """,
            (category,)
        ).fetchall()
        return [Cam(*row) for row in rows]

class CommentModel(Model):
    def insert(self, body: str, cam_id: int, author_id: int) -> int:
        """Insert a new comment and return its ID."""
        created = datetime.utcnow()
        
        cursor = self.db.execute(
                """
                INSERT INTO Comments (body, cam_id, author_id, created)
                VALUES (?, ?, ?, ?)
                """,
                (body, cam_id, author_id, created)
            )
            
        self.db.commit()
        return cursor.lastrowid
    
    # get cam with author id 
    def get_with_author(self, comment_id: int) -> Comment | None:
        """retreive author for edit/delete"""
        row = self.db.execute(
            """
            SELECT 
                c.id,
                c.title, 
                c.content, 
                c.img, 
                c.category, 
                c.author AS author_id,
                c.created,
                a.username AS author_username
            FROM Comments c
            JOIN Accounts a 
                ON c.author = a.id
            WHERE c.id = ?
            """,
            (comment_id,)
        ).fetchone()
        if not row:
            return None
        return Comment(*row) 

    def for_cam(self, cam_id: int) -> list[Comment]:
        """Return all comments for a specific cam, oldest first."""
        rows = self.db.execute(
            """
            SELECT 
                c.id, 
                c.body, 
                c.created, 
                c.author_id, 
                c.cam_id, 
                a.username  AS author_username
            FROM Comments c
            JOIN Accounts a 
                ON c.author_id = a.id
            WHERE c.cam_id = ?
            ORDER BY c.created ASC
            """,
            (cam_id,)
        ).fetchall()
        comments = []

        for row in rows:
            comment = Comment(*row)
            date = datetime.fromisoformat(comment.created)
            comment.created = date.strftime("%b %d, %Y at %I:%M %p")
            comments.append(comment)
        return comments
    
    def account_comments(self, account_id: int) -> list[Comment]:
        """Return all comments by a specific account."""
        rows = self.db.execute(
            """
            SELECT 
                c.id, 
                c.body, 
                c.created, 
                c.author_id, 
                c.cam_id,
                a.username AS author_username 
            FROM Comments c
            JOIN Accounts a ON c.author_id = a.id
            WHERE c.author_id = ?
            ORDER BY c.created DESC
            """,
            (account_id,)
        ).fetchall()
        return [Comment(*row) for row in rows]

    def update_comment(self, comment_id: int, body: str):
        self.db.execute(
            """
            UPDATE Comments
            SET body = ?
            WHERE id = ?
            """,
            (body, comment_id)
        )
        self.db.commit()
    
    def delete_comment(self, comment_id: int) -> None:
        self.db.execute(
            """
            DELETE FROM Comments
            WHERE id =?
            """,
            (comment_id,)
        )
        self.db.commit()