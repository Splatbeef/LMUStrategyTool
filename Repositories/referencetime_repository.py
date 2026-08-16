#import sqlite3
from models import ReferenceTime
import datetime as dt

class ReferenceTimeRepository:

    def __init__(self, db_service):
        self.db = db_service

    def add(self, laptime: ReferenceTime) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO referencetimes (track_id, carclass_id, laptime, date_set, source)
                VALUES (?, ?, ?, ?, ?)
                """,
                (laptime.track_id, laptime.carclass_id, laptime.laptime, laptime.date_set.isoformat(), laptime.source)
            )

            conn.commit()

            return cursor.lastrowid

    def get_all(self) -> list[ReferenceTime]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, track_id, carclass_id, laptime, date_set, source
                FROM referencetimes
                ORDER BY track_id
                """
            ).fetchall()

        return [
            ReferenceTime(
                id=row[0],
                track_id=row[1],
                carclass_id=row[2],
                laptime=row[3],
                date_set=self.parse_date(row[4]),
                source=row[5]
            )
            for row in rows
        ]

    def get_by_id(self, id: int) -> ReferenceTime | None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT id, track_id, carclass_id, laptime, date_set, source
                FROM referencetimes
                WHERE id = ?
                """,
                (id,)
            ).fetchone()

        if row is None:
            return None

        return ReferenceTime(
                        id=row[0],
                        track_id=row[1],
                        carclass_id=row[2],
                        laptime=row[3],
                        date_set=self.parse_date(row[4]),
                        source=row[5]
                    )

    def update(self, laptime: ReferenceTime) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                
                UPDATE referencetimes
                SET track_id = ?,
                    carclass_id = ?,
                    laptime = ?,
                    date_set = ?,
                    source = ?
                WHERE id = ?
                """,
                (
                    laptime.track_id, 
                    laptime.carclass_id, 
                    laptime.laptime, 
                    laptime.date_set.isoformat(), 
                    laptime.source,
                    laptime.id
                ))
            conn.commit()

    def delete(self, laptime_id: int) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM referencetimes
                WHERE id = ?
                """,
                (laptime_id,)
            )

            conn.commit()

    def exists(
    self,
    track_id: int,
    carclass_id: int,
    ) -> bool:

        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT 1
                FROM referencetimes
                WHERE track_id = ?
                AND carclass_id = ?
                LIMIT 1
                """,
                (track_id, carclass_id)
            ).fetchone()

        return row is not None

    def get_by_track(self, track_id: int) -> list:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, track_id, carclass_id, laptime, date_set, source
                FROM referencetimes
                WHERE track_id = ?
                ORDER BY track_id
                """,
                (track_id,)
            ).fetchall()

        return [
            ReferenceTime(
                            id=row[0],
                            track_id=row[1],
                            carclass_id=row[2],
                            laptime=row[3],
                            date_set=self.parse_date(row[4]),
                            source=row[5]
                        )
            for row in rows
        ]

    def get_by_class(self, carclass_id: int) -> list:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, track_id, carclass_id, laptime, date_set, source
                FROM referencetimes
                WHERE carclass_id = ?
                ORDER BY track_id
                """,
                (carclass_id,)
            ).fetchall()

        return [
            ReferenceTime(
                            id=row[0],
                            track_id=row[1],
                            carclass_id=row[2],
                            laptime=row[3],
                            date_set=self.parse_date(row[4]),
                            source=row[5]
                        )
            for row in rows
        ]

    def get_by_track_class(
        self,
        track_id: int,
        carclass_id: int
    ) -> list[ReferenceTime]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, track_id, carclass_id, laptime, date_set, source
                FROM referencetimes
                WHERE track_id = ?
                AND carclass_id = ?
                ORDER BY laptime
                """,
                (track_id, carclass_id)
            ).fetchall()

        return [
            ReferenceTime(
                            id=row[0],
                            track_id=row[1],
                            carclass_id=row[2],
                            laptime=row[3],
                            date_set=self.parse_date(row[4]),
                            source=row[5]
                        )
            for row in rows
        ]

    def get_best_reference(
    self,
    track_id: int,
    carclass_id: int
) -> ReferenceTime | None:

        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT id, track_id, carclass_id, laptime, date_set, source
                FROM referencetimes
                WHERE track_id = ?
                AND carclass_id = ?
                ORDER BY laptime ASC
                LIMIT 1
                """,
                (track_id, carclass_id)
            ).fetchone()

        if row is None:
            return None

        return ReferenceTime(
            id=row[0],
            track_id=row[1],
            carclass_id=row[2],
            laptime=row[3],
            date_set=self.parse_date(row[4]),
            source=row[5]
        )

    def get_by_source(self, source: str) -> list[ReferenceTime]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
                 
            rows = cursor.execute(
                """
                SELECT id, track_id, carclass_id, laptime, date_set, source
                FROM referencetimes
                WHERE source = ?
                ORDER BY laptime
                """,
                (source,)
            ).fetchall()

        return [
            ReferenceTime(
                id=row[0],
                track_id=row[1],
                carclass_id=row[2],
                laptime=row[3],
                date_set=self.parse_date(row[4]),
                source=row[5]
            )
            for row in rows
        ]

    def parse_date(self, value):
        value = str(value)

        try:
            return dt.date.fromisoformat(value)
        except ValueError:
            return dt.datetime

    def clear(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM referencetimes
            """)

            conn.commit()