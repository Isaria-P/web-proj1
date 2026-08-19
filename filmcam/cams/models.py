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
            JOIN Accounts a ON c.author = a.id
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
            SELECT Cams.id, title, content, img, category, created 
            FROM Cams
            WHERE author = ?
            """,
            (account_id,),
        ).fetchall()
        return [Cam(*c) for c in cams]

    def latest(self) -> list[Cam]:
        rows = self.db.execute(
            """
            SELECT id, title, content, img, category, created
            FROM Cams
            ORDER BY created DESC
            """
        ).fetchall()
        return [Cam(*row) for row in rows]