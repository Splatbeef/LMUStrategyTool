#import sqlite3
from models import LapTime
import datetime as dt

class LapTimeRepository:

    def __init__(self, db_service):
        self.db = db_service

    def add(self, laptime: LapTime) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO laptimes (track_id, car_id, laptime, date_set, sessiontype)
                VALUES (?, ?, ?, ?, ?)
                """,
                (laptime.track_id, laptime.car_id, laptime.laptime, laptime.date_set.isoformat(), laptime.sessiontype)
            )

            conn.commit()

            return cursor.lastrowid

    def get_all(self) -> list[LapTime]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, track_id, car_id, laptime, date_set, sessiontype
                FROM laptimes
                ORDER BY car_id
                """
            ).fetchall()

        return [
            LapTime(
                id=row[0],
                track_id=row[1],
                car_id=row[2],
                laptime=row[3],
                date_set=dt.date.fromisoformat(row[4]),
                sessiontype=row[5]
            )
            for row in rows
        ]

    def get_by_id(self, id: int) -> LapTime | None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT id, track_id, car_id, laptime, date_set, sessiontype
                FROM laptimes
                WHERE id = ?
                """,
                (id,)
            ).fetchone()

        if row is None:
            return None

        return LapTime(
                        id=row[0],
                        track_id=row[1],
                        car_id=row[2],
                        laptime=row[3],
                        date_set=dt.date.fromisoformat(row[4]),
                        sessiontype=row[5]
                    )

    def update(self, laptime: LapTime) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                
                UPDATE laptimes
                SET track_id = ?,
                    car_id = ?,
                    laptime = ?,
                    date_set = ?,
                    sessiontype = ?
                WHERE id = ?
                """,
                (
                    laptime.track_id, 
                    laptime.car_id, 
                    laptime.laptime, 
                    laptime.date_set.isoformat(), 
                    laptime.sessiontype,
                    laptime.id
                ))
            conn.commit()

    def delete(self, laptime_id: int) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM laptimes
                WHERE id = ?
                """,
                (laptime_id,)
            )

            conn.commit()

    def exists(
    self,
    track_id: int,
    car_id: int,
    laptime: float
    ) -> bool:

        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT 1
                FROM laptimes
                WHERE track_id = ?
                AND car_id = ?
                AND laptime = ?
                LIMIT 1
                """,
                (track_id, car_id, laptime)
            ).fetchone()

        return row is not None

    def get_by_track(self, track_id: int) -> list:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, track_id, car_id, laptime, date_set, sessiontype
                FROM laptimes
                WHERE track_id = ?
                ORDER BY car_id
                """,
                (track_id,)
            ).fetchall()

        return [
            LapTime(
                id=row[0],
                track_id=row[1],
                car_id=row[2],
                laptime=row[3],
                date_set=dt.date.fromisoformat(row[4]),
                sessiontype=row[5]
            )
            for row in rows
        ]

    def get_by_car(self, car_id: int) -> list:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, track_id, car_id, laptime, date_set, sessiontype
                FROM laptimes
                WHERE car_id = ?
                ORDER BY track_id
                """,
                (car_id,)
            ).fetchall()

        return [
            LapTime(
                id=row[0],
                track_id=row[1],
                car_id=row[2],
                laptime=row[3],
                date_set=dt.date.fromisoformat(row[4]),
                sessiontype=row[5]
            )
            for row in rows
        ]

    def get_by_session(self, session: str) -> list:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, track_id, car_id, laptime, date_set, sessiontype
                FROM laptimes
                WHERE sessiontype = ?
                ORDER BY car_id
                """,
                (session,)
            ).fetchall()

        return [
            LapTime(
                id=row[0],
                track_id=row[1],
                car_id=row[2],
                laptime=row[3],
                date_set=dt.date.fromisoformat(row[4]),
                sessiontype=row[5]
            )
            for row in rows
        ]

    def get_by_track_car(
        self,
        track_id: int,
        car_id: int
    ) -> list[LapTime]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, track_id, car_id, laptime, date_set, sessiontype
                FROM laptimes
                WHERE track_id = ?
                AND car_id = ?
                ORDER BY laptime
                """,
                (track_id, car_id)
            ).fetchall()

        return [
            LapTime(
                id=row[0],
                track_id=row[1],
                car_id=row[2],
                laptime=row[3],
                date_set=dt.date.fromisoformat(row[4]),
                sessiontype=row[5]
            )
            for row in rows
        ]

    def get_by_track_session(
        self,
        track_id: int,
        session: str
    ) -> list[LapTime]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, track_id, car_id, laptime, date_set, sessiontype
                FROM laptimes
                WHERE track_id = ?
                AND sessiontype = ?
                ORDER BY car_id
                """,
                (track_id, session)
            ).fetchall()

        return [
            LapTime(
                id=row[0],
                track_id=row[1],
                car_id=row[2],
                laptime=row[3],
                date_set=dt.date.fromisoformat(row[4]),
                sessiontype=row[5]
            )
            for row in rows
        ]

    def get_by_car_session(
        self,
        car_id: int,
        session: str
    ) -> list[LapTime]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, track_id, car_id, laptime, date_set, sessiontype
                FROM laptimes
                WHERE car_id = ?
                AND sessiontype = ?
                ORDER BY track_id
                """,
                (car_id, session)
            ).fetchall()

        return [
            LapTime(
                id=row[0],
                track_id=row[1],
                car_id=row[2],
                laptime=row[3],
                date_set=dt.date.fromisoformat(row[4]),
                sessiontype=row[5]
            )
            for row in rows
        ]

    def get_by_track_car_session(
            self,
            track_id: int,
            car_id: int,
            sessiontype: str
        ) -> LapTime | None:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
    
                row = cursor.execute(
                    """
                    SELECT id, track_id, car_id, laptime, date_set, sessiontype
                    FROM laptimes
                    WHERE track_id = ?
                    AND car_id = ?
                    AND sessiontype = ?
                    ORDER BY laptime
                    """,
                    (track_id, car_id, sessiontype)
                ).fetchone()
            if row is None:
                return None
    
            return LapTime(
                    id=row[0],
                    track_id=row[1],
                    car_id=row[2],
                    laptime=row[3],
                    date_set=dt.date.fromisoformat(row[4]),
                    sessiontype=row[5]
                )

    def get_best_lap(
        self,
        track_id: int,
        car_id: int
    ) -> LapTime | None:

        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT id, track_id, car_id, laptime, date_set, sessiontype
                FROM laptimes
                WHERE track_id = ?
                AND car_id = ?
                ORDER BY laptime ASC
                LIMIT 1
                """,
                (track_id, car_id)
            ).fetchone()

        if row is None:
            return None

        return LapTime(
            id=row[0],
            track_id=row[1],
            car_id=row[2],
            laptime=row[3],
            date_set=dt.date.fromisoformat(row[4]),
            sessiontype=row[5]
        )