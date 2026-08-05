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
    author: str
    created: datetime


class CamModel(Model):
    def insert(self, title: str, content: str, img: str, category: str, author: str) -> int:
        created = datetime.now()
        cursor = self.db.execute(
            """
            INSERT INTO Cams (title, content, img, category, author, created)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title, content, img, category, author, created),
        )
        self.db.commit()

        cam_id = cursor.lastrowid
        if not cam_id:
            raise RuntimeError("insert failed: no lastrowid")
        return cam_id

    def get(self, cam_id: int) -> Cam:
        cam_id, title, content, img, category, author, created = self.db.execute(
            """
            SELECT id, title, content, img, category, author, created
            FROM Cams
            WHERE id = ?
            """,
            (cam_id,),
        ).fetchone()
        return Cam(cam_id, title, content, img, category, author, created)

    def latest(self) -> list[Cam]:
        rows = self.db.execute(
            """
            SELECT id, title, content, img, category, author, created
            FROM Cams
            ORDER BY created DESC
            """
        ).fetchall()
        print(rows)
        return [Cam(*row) for row in rows]