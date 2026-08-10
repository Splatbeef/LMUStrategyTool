#import sqlite3
from models import FuelUsage

class FuelRepository:

    def __init__(self, db_service):
        self.db = db_service

    def add(self, usage: FuelUsage) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO fuelusage (track_id, car_id, fuel_usage, ve_usage)
                VALUES (?, ?, ?, ?)
                """,
                (usage.track_id, usage.car_id, usage.fuel_usage, usage.ve_usage)
            )

            conn.commit()

            return cursor.lastrowid

    def get_all(self) -> list[FuelUsage]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, track_id, car_id, fuel_usage, ve_usage
                FROM fuelusage
                ORDER BY car_id, track_id
                """
            ).fetchall()

        return [
            FuelUsage(
                id=row[0],
                track_id=row[1],
                car_id=row[2],
                fuel_usage=row[3],
                ve_usage=row[4]
            )
            for row in rows
        ]

    def get_by_id(self, id: int) -> FuelUsage | None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT id, track_id, car_id, fuel_usage, ve_usage
                FROM fuelusage
                WHERE id = ?
                """,
                (id,)
            ).fetchone()

        if row is None:
            return None

        return FuelUsage(
                        id=row[0],
                        track_id=row[1],
                        car_id=row[2],
                        fuel_usage=row[3],
                        ve_usage=row[4]
                    )

    def update(self, usage: FuelUsage) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                
                UPDATE fuelusage
                SET track_id = ?,
                    car_id = ?,
                    fuel_usage = ?,
                    ve_usage = ?
                WHERE id = ?
                """,
                (usage.track_id, 
                 usage.car_id, 
                 usage.fuel_usage, 
                 usage.ve_usage, 
                 usage.id))
            conn.commit()

    def delete(self, id: int) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM fuelusage
                WHERE id = ?
                """,
                (id,)
            )

            conn.commit()

    def exists(self, track_id: int, car_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT 1
                FROM fuelusage
                WHERE track_id = ? AND car_id = ?
                LIMIT 1
                """,
                (track_id, car_id)
            ).fetchone()

        return row is not None

    def get_by_track(self, track_id: int) -> list[FuelUsage]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, track_id, car_id, fuel_usage, ve_usage
                FROM fuelusage
                WHERE track_id = ?
                """,
                (track_id,)
            ).fetchall()

        return [
            FuelUsage(
                            id=row[0],
                            track_id=row[1],
                            car_id=row[2],
                            fuel_usage=row[3],
                            ve_usage=row[4]
                        )
            for row in rows
        ]

    def get_by_car(self, car_id: int) -> list[FuelUsage]:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
    
                rows = cursor.execute(
                    """
                    SELECT id, track_id, car_id, fuel_usage, ve_usage
                    FROM fuelusage
                    WHERE car_id = ?
                    """,
                    (car_id,)
                ).fetchall()
    
            return [
                FuelUsage(
                                id=row[0],
                                track_id=row[1],
                                car_id=row[2],
                                fuel_usage=row[3],
                                ve_usage=row[4]
                            )
                for row in rows
            ]

    def get_by_track_car(self, track_id: int, car_id: int) -> FuelUsage | None:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
    
                row = cursor.execute(
                    """
                    SELECT id, track_id, car_id, fuel_usage, ve_usage
                    FROM fuelusage
                    WHERE track_id = ? AND car_id = ?
                    """,
                    (track_id,car_id)
                ).fetchone()
    
            return FuelUsage(
                                id=row[0],
                                track_id=row[1],
                                car_id=row[2],
                                fuel_usage=row[3],
                                ve_usage=row[4]
                            )