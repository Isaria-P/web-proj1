from dataclasses import dataclass
from datetime import datetime

from filmcam.utils.db import Model

@dataclass
class Cam:
    id: int
    title: str
    content: str
    img: str
    category: str
    created: datetime
    author_id: int
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
        created = datetime.now()
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

    def get(self, cam_id: int) -> Cam:
        id, title, content, img, category, created = self.db.execute(
            """
            SELECT id, title, content, img, category, created
            FROM Cams
            WHERE id = ?
            """,
            (cam_id,)
        ).fetchone()
        return Cam(id, title, content, img, category, created )

    # newer
    # get cam with author id
    def get_with_author(self, cam_id: int):
        row = self.db.execute(
            """
            SELECT 
                c.id,
                c.title, 
                c.content, 
                c.img, 
                c.category, 
                c.author,
                c.created,
                a.email AS author
            FROM Cams c
            JOIN Accounts a ON c.author_id = a.id
            WHERE c.id = ?
            """,
            (cam_id,)
        ).fetchone()
        if not row:
            return None
        print(row)
        return dict(zip(("id", "title", "content", "img", "category", "author_id", "created", "author"), row))
 
    
    def account_cams(self, account_id: int) -> list[Cam]:
        cams = self.db.execute(
            """
            SELECT c.id, c.title, c.content, c.img, c.category, c.created, c.author

            FROM Cams c
            WHERE author = ?
            """,
            (account_id,),
        ).fetchall()
        return [Cam(*c) for c in cams]

    def latest(self) -> list[Cam]:
        rows = self.db.execute(
            """
            SELECT id, title, content, img, category, created, author
            FROM Cams
            ORDER BY created DESC
            """
        ).fetchall()
        return [Cam(*row) for row in rows]

    # get comments w/ author username
    def get_comments_with_authors(self, cam_id: int):
        rows = self.db.execute(
            """
                SELECT c.id, c.body, c.created, c.author_id, c.story_id, a.username
                FROM Comments c
                JOIN Accounts a ON c.author_id = a.id
                WHERE c.cam_id
                ORDER BY c.created ASC
            """,
            (cam_id,)
        ).fetchall()
        comment = []
        for row in rows:
            comments.append({
                "id": row[0],
                "body": row[1],
                "created": row[2],
                "author_id": row[3],
                "story_id": row[4],
                "author_username": row[5],
            })
        return comments

    #add comment
    def add_comment(self, cam_id: int, author_id: int, body: str) -> int:
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

class CommentModel(Model):
    def insert(self, body: str, cam_id: int, author_id: int) -> int:
        """Insert a new comment and return its ID."""
        create = datetime.utcnow()
        cursor = self.db.execute(
                """
                INSERT INTO Comments (body, cam_id, author_id, created)
                VALUES (?, ?, ?, ?)
                """,
                (body, cam_id, author_id, created)
            )
        self.db.commit()
        return cursor.lastrowid
    
    def for_cam(self, cam_id: int) -> list[Comment]:
        """Return all comments for a specific cam, oldest first."""
        rows = self.db.execute(
            """
            SELECT id, body, created, author_id, cam_id
            FROM Comments
            WHERE cam_id = ?
            ORDER BY created ASC
            """,
            (cam_id,)
        ).fetchall()
        return [Comment(*row) for row in rows]

    def account_comments(self, account_id: int) -> list[Comment]:
        """Return all comments by a specific account."""
        rows = self.db.execute(
            """
            SELECT id, body, created, author_id, cam_id
            FROM Comments
            WHERE author_id = ?
            ORDER BY created DESC
            """,
            (account_id,)
        ).fetchall()
        return [Comment(*row) for row in rows]
