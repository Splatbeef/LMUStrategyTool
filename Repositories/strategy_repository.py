#import sqlite3
from models import Strategy

class StrategyRepository:

    def __init__(self, db_service):
        self.db = db_service

    def add(self, strat: Strategy) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO strategies (name, track_id, car_id, race_minutes, laptime_override, laps_override, usage_multiplier, fuel_capacity_override, ve_capacity_override)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (strat.name, strat.track_id, strat.car_id, strat.race_minutes, strat.laptime_override, strat.laps_override, strat.usage_multiplier, strat.fuel_capacity_override, strat.ve_capacity_override)
            )

            conn.commit()

            return cursor.lastrowid

    def get_all(self) -> list[Strategy]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, name, track_id, car_id, race_minutes, laptime_override, laps_override, usage_multiplier, fuel_capacity_override, ve_capacity_override
                FROM strategies
                ORDER BY name
                """
            ).fetchall()

        return [
            Strategy(
                id=row[0],
                name=row[1],
                track_id = row[2], 
                car_id = row[3],
                race_minutes = row[4], 
                laptime_override = row[5], 
                laps_override = row[6], 
                usage_multiplier = row[7], 
                fuel_capacity_override = row[8], 
                ve_capacity_override = row[9]
            )
            for row in rows
        ]

    def get_by_id(self, id: int) -> Strategy | None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT id, name, track_id, car_id, race_minutes, laptime_override, laps_override, usage_multiplier, fuel_capacity_override, ve_capacity_override
                FROM cars
                WHERE id = ?
                """,
                (id,)
            ).fetchone()

        if row is None:
            return None

        return Strategy(
                        id=row[0],
                        name=row[1],
                        track_id = row[2], 
                        car_id = row[3],
                        race_minutes = row[4], 
                        laptime_override = row[5], 
                        laps_override = row[6], 
                        usage_multiplier = row[7], 
                        fuel_capacity_override = row[8], 
                        ve_capacity_override = row[9]
                    )

    def update(self, strat: Strategy) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                
                UPDATE strategies
                SET name = ?,
                    track_id = ?, 
                    car_id = ?,
                    race_minutes = ?, 
                    laptime_override = ?, 
                    laps_override = ?, 
                    usage_multiplier = ?, 
                    fuel_capacity_override = ?, 
                    ve_capacity_override = ?
                WHERE id = ?
                """,
                (strat.name, 
                 strat.track_id, 
                 strat.car_id, 
                 strat.race_minutes, 
                 strat.laptime_override, 
                 strat.laps_override, 
                 strat.usage_multiplier, 
                 strat.fuel_capacity_override, 
                 strat.ve_capacity_override, 
                 strat.id))
            conn.commit()

    def delete(self, strat_id: int) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM strategies
                WHERE id = ?
                """,
                (strat_id,)
            )

            conn.commit()

    def exists(self, name: str) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT 1
                FROM strategies
                WHERE LOWER(name) = LOWER(?)
                LIMIT 1
                """,
                (name,)
            ).fetchone()

        return row is not None

    def get_by_name(self, name: str) -> Strategy | None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT id, name, track_id, car_id, race_minutes, laptime_override, laps_override, usage_multiplier, fuel_capacity_override, ve_capacity_override
                FROM strategies
                WHERE name = ?
                """,
                (name,)
            ).fetchone()

        return Strategy(
                            id=row[0],
                            name=row[1],
                            track_id = row[2], 
                            car_id = row[3],
                            race_minutes = row[4], 
                            laptime_override = row[5], 
                            laps_override = row[6], 
                            usage_multiplier = row[7], 
                            fuel_capacity_override = row[8], 
                            ve_capacity_override = row[9]
            )