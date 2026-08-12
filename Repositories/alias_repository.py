from models import TrackAlias, CarAlias

class TrackAliasRepository:
    def __init__(self, db_service):
            self.db = db_service
    
    def add(self, alias: TrackAlias) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO track_aliases (alias, name, layout)
                VALUES (?, ?, ?)
                """,
                (alias.alias, alias.name, alias.layout)
            )

            conn.commit()

            return cursor.lastrowid

    def get_all(self) -> list[TrackAlias]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, alias, name, layout
                FROM track_aliases
                ORDER BY name, layout
                """
            ).fetchall()

        return [
            TrackAlias(
                id=row[0],
                alias=row[1],
                name=row[2],
                layout=row[3]
            )
            for row in rows
        ]

    def get_by_id(self, id: int) -> TrackAlias | None:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
    
                row = cursor.execute(
                    """
                    SELECT id, alias, name, layout
                    FROM track_aliases
                    WHERE id = ?
                    """,
                    (id,)
                ).fetchone()
    
            if row is None:
                return None
    
            return TrackAlias(
                    id=row[0],
                    alias=row[1],
                    name=row[2],
                    layout=row[3]
                )

    def update(self, alias: TrackAlias) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                
                UPDATE track_aliases
                SET alias = ?,
                    name = ?,
                    layout = ?
                WHERE id = ?
                """,
                (
                    alias.alias,
                    alias.name,
                    alias.layout,
                    alias.id
                ))
            conn.commit()

    def delete(self, alias_id: int) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM track_aliases
                WHERE id = ?
                """,
                (alias_id,)
            )

            conn.commit()

    def exists(self, alias: str) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT 1
                FROM track_aliases
                WHERE LOWER(alias) = LOWER(?)
                LIMIT 1
                """,
                (alias,)
            ).fetchone()

        return row is not None

    def get_by_alias(self, alias: str) -> TrackAlias | None:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
    
                row = cursor.execute(
                    """
                    SELECT id, alias, name, layout
                    FROM track_aliases
                    WHERE LOWER(alias) = LOWER(?)
                    LIMIT 1
                    """,
                    (alias,)
                ).fetchone()

            if row is None:
                return None
    
            return TrackAlias(
                    id=row[0],
                    alias = row[1],
                    name=row[2],
                    layout=row[3]
                )

class CarAliasRepository:
    def __init__(self, db_service):
            self.db = db_service
    
    def add(self, alias: CarAlias) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO car_aliases (alias, name)
                VALUES (?, ?)
                """,
                (alias.alias, alias.name)
            )

            conn.commit()

            return cursor.lastrowid

    def get_all(self) -> list[CarAlias]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, alias, name
                FROM car_aliases
                ORDER BY name
                """
            ).fetchall()

        return [
            CarAlias(
                id=row[0],
                alias=row[1],
                name=row[2]
            )
            for row in rows
        ]

    def get_by_id(self, id: int) -> CarAlias | None:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
    
                row = cursor.execute(
                    """
                    SELECT id, alias, name
                    FROM car_aliases
                    WHERE id = ?
                    """,
                    (id,)
                ).fetchone()
    
            if row is None:
                return None
    
            return CarAlias(
                    id=row[0],
                    alias=row[1],
                    name=row[2]
                )

    def update(self, alias: CarAlias) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                
                UPDATE car_aliases
                SET alias = ?,
                    name = ?
                WHERE id = ?
                """,
                (
                    alias.alias,
                    alias.name,
                    alias.id
                ))
            conn.commit()

    def delete(self, alias_id: int) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM car_aliases
                WHERE id = ?
                """,
                (alias_id,)
            )

            conn.commit()

    def exists(self, alias: str) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT 1
                FROM car_aliases
                WHERE LOWER(alias) = LOWER(?)
                LIMIT 1
                """,
                (alias,)
            ).fetchone()

        return row is not None

    def get_by_alias(self, alias: str) -> CarAlias | None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT id, alias, name
                FROM car_aliases
                WHERE LOWER(alias) = LOWER(?)
                LIMIT 1
                """,
                (alias,)
            ).fetchone()

        if row is None:
             return None

        return CarAlias(
                id=row[0],
                alias = row[1],
                name=row[2]
            )

    def get_by_name(self, name: str) -> list[CarAlias] | None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, alias, name
                FROM car_aliases
                WHERE LOWER(name) = LOWER(?)
                LIMIT 1
                """,
                (name,)
            ).fetchall()

        if rows is None:
                return None

        return [CarAlias(
                id=row[0],
                alias = row[1],
                name=row[2]
            )
            for row in rows]