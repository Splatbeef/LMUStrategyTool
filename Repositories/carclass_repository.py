#import sqlite3
from models import CarClass

class CarClassRepository:

    def __init__(self, db_service):
        self.db = db_service

    def add(self, car_class: CarClass) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO car_classes (name)
                VALUES (?)
                """,
                (car_class.name,)
            )

            conn.commit()

            return cursor.lastrowid

    def get_all(self) -> list[CarClass]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, name
                FROM car_classes
                ORDER BY name
                """
            ).fetchall()

        return [
            CarClass(
                id=row[0],
                name=row[1]
            )
            for row in rows
        ]

    def get_by_id(self, id: int) -> CarClass | None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT id, name
                FROM car_classes
                WHERE id = ?
                """,
                (id,)
            ).fetchone()

        return CarClass(
                id=row[0],
                name=row[1]
            )

    def update(self, car_class: CarClass) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                
                UPDATE car_classes
                SET name = ?
                WHERE id = ?
                """,
                (
                    car_class.name,
                    car_class.id
                ))
            conn.commit()

    def delete(self, car_class_id: int) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM car_classes
                WHERE id = ?
                """,
                (car_class_id,)
            )

            conn.commit()

    def exists(self, name: str) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT 1
                FROM car_classes
                WHERE LOWER(name) = LOWER(?)
                LIMIT 1
                """,
                (name,)
            ).fetchone()

        return row is not None

    def get_by_name(self, name: str) -> CarClass | None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT id, name
                FROM car_classes
                WHERE name = ?
                """,
                (name,)
            ).fetchone()

        if row is None:
            return None

        return CarClass(
            id=row[0],
            name=row[1]
        )