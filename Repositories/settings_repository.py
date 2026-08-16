from models import Setting

class SettingsRepository:
    def __init__(self, db_service):
        self.db = db_service

    def add(self, setting: Setting) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO settings (key, value_str, value_bool, value_int, value_float)
                VALUES (?, ?, ?, ?, ?)
                """,
                (setting.key, setting.value_str, setting.value_bool, setting.value_int, setting.value_float)
            )

            conn.commit()

            return cursor.lastrowid
        
    def update(self, setting: Setting) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                
                UPDATE settings
                SET key = ?,
                    value_str = ?,
                    value_bool = ?,
                    value_int = ?,
                    value_float = ?
                WHERE id = ?
                """,
                (
                    setting.key,
                    setting.value_str, 
                    setting.value_bool, 
                    setting.value_int, 
                    setting.value_float,
                    setting.id
                ))
            conn.commit()

    def delete(self, setting_id: int) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM settings
                WHERE id = ?
                """,
                (setting_id,)
            )

            conn.commit()

    def exists(self, key: str) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT 1
                FROM settings
                WHERE LOWER(key) = LOWER(?)
                LIMIT 1
                """,
                (key,)
            ).fetchone()

        return row is not None

    def get_all(self) -> list[Setting]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            rows = cursor.execute(
                """
                SELECT id, key, value_str, value_bool, value_int, value_float
                FROM settings
                ORDER BY key
                """
            ).fetchall()

        return [
            Setting(
                id=row[0],
                key=row[1],
                value_str=row[2],
                value_bool=bool(row[3]),
                value_int=row[4],
                value_float=row[5]
            )
            for row in rows
        ]

    def get_by_id(self, id: int) -> Setting | None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT id, key, value_str, value_bool, value_int, value_float
                FROM settings
                WHERE id = ?
                """,
                (id,)
            ).fetchone()

        if row is None:
            return None

        return Setting(
                    id=row[0],
                    key=row[1],
                    value_str=row[2],
                    value_bool=bool(row[3]),
                    value_int=row[4],
                    value_float=row[5]
                )

    def get_by_key(self, key: str) -> Setting | None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            row = cursor.execute(
                """
                SELECT id, key, value_str, value_bool, value_int, value_float
                FROM settings
                WHERE key = ?
                """,
                (key,)
            ).fetchone()

        if row is None:
            return None

        return Setting(
                    id=row[0],
                    key=row[1],
                    value_str=row[2],
                    value_bool=bool(row[3]),
                    value_int=row[4],
                    value_float=row[5]
                )