#import sqlite3
from models import Car

class CarRepository:

    def __init__(self, db_service):
        self.db = db_service

    def add(self, car: Car) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO cars (name, carclass_id, fuel_capacity, ve)
                VALUES (?, ?, ?, ?)
                """,
                (car.name, car.carclass_id,car.fuel_capacity,car.ve)
            )

            conn.commit()

            return cursor.lastrowid

    def get_all(self) -> list[Car]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, name, carclass_id, fuel_capacity, ve
                FROM cars
                ORDER BY carclass_id, name
                """
            ).fetchall()

        return [
            Car(
                id=row[0],
                name=row[1],
                carclass_id=row[2],
                fuel_capacity=row[3],
                ve=bool(row[4])
            )
            for row in rows
        ]

    def get_by_id(self, id: int) -> Car | None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT id, name, carclass_id, fuel_capacity, ve
                FROM cars
                WHERE id = ?
                """,
                (id,)
            ).fetchone()

        if row is None:
            return None

        return Car(
                        id=row[0],
                        name=row[1],
                        carclass_id=row[2],
                        fuel_capacity=row[3],
                        ve=bool(row[4])
                    )

    def update(self, car: Car) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                
                UPDATE cars
                SET name = ?,
                    carclass_id = ?,
                    fuel_capacity = ?,
                    ve = ?
                WHERE id = ?
                """,
                (
                    car.name,
                    car.carclass_id,
                    car.fuel_capacity,
                    car.ve,
                    car.id
                ))
            conn.commit()

    def delete(self, car_id: int) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM cars
                WHERE id = ?
                """,
                (car_id,)
            )

            conn.commit()

    def exists(self, name: str) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT 1
                FROM cars
                WHERE LOWER(name) = LOWER(?)
                LIMIT 1
                """,
                (name,)
            ).fetchone()

        return row is not None

    def get_by_name(self, name: str) -> Car:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT id, name, carclass_id, fuel_capacity, ve
                FROM cars
                WHERE name = ?
                """,
                (name,)
            ).fetchone()

        if row is None:
            print(name)

        return Car(
                id=row[0],
                name=row[1],
                carclass_id=row[2],
                fuel_capacity=row[3],
                ve=bool(row[4])
            )