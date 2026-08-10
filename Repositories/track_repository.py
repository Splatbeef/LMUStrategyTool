#import sqlite3
from models import Track

class TrackRepository:

    def __init__(self, db_service):
        self.db = db_service

    def add(self, track: Track) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO tracks (name, layout)
                VALUES (?, ?)
                """,
                (track.name,track.layout)
            )

            conn.commit()

            return cursor.lastrowid

    def get_all(self) -> list:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, name, layout
                FROM tracks
                ORDER BY name
                """
            ).fetchall()

        return [
            Track(
                id=row[0],
                name=row[1],
                layout=row[2]
            )
            for row in rows
        ]

    def get_all_layouts(self, name: str) -> list:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
    
                rows = cursor.execute(
                    """
                    SELECT layout
                    FROM tracks
                    WHERE name = ?
                    ORDER BY layout
                    """,
                    (name,)
                ).fetchall()
    
            return [row[0] for row in rows]

    def get_by_id(self, id: int) -> Track | None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT id, name, layout
                FROM tracks
                WHERE id = ?
                """,
                (id,)
            ).fetchone()

        if row is None:
            return None

        return Track(
                id=row[0],
                name=row[1],
                layout=row[2]
            )

    def update(self, track: Track) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                
                UPDATE tracks
                SET name = ?,
                    layout = ?
                WHERE id = ?
                """,
                (
                    track.name,
                    track.layout,
                    track.id
                ))
            conn.commit()

    def delete(self, track_id: int) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM tracks
                WHERE id = ?
                """,
                (track_id,)
            )

            conn.commit()

    def exists(self, name: str, layout: str) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT 1
                FROM tracks
                WHERE LOWER(name) = LOWER(?) AND LOWER(layout) = LOWER(?)
                LIMIT 1
                """,
                (name,layout)
            ).fetchone()

        return row is not None

    def get_by_name(self, name: str) -> list[Track]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, name, layout
                FROM tracks
                WHERE name = ?
                """,
                (name,)
            ).fetchall()

        return [
            Track(
                id=row[0],
                name=row[1],
                layout=row[2]
            )
            for row in rows
        ]