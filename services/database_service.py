import sqlite3
from pathlib import Path


class DatabaseService:

    def __init__(self):
        db_path = Path("data/lmu_strategy.db")

        db_path.parent.mkdir(exist_ok=True)

        self.db_path = db_path

        self.create_tables()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_tables(self):
        with self.get_connection() as conn:
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS car_classes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS tracks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    layout TEXT
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS cars (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    carclass_id INTEGER NOT NULL,
                    fuel_capacity INTEGER,
                    ve INTEGER
                    FOREIGN KEY (carclass_id) REFERENCES car_classes(id)
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS laptimes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    track_id INTEGER NOT NULL,
                    car_id INTEGER NOT NULL,
                    laptime REAL NOT NULL,
                    date_set TEXT,
                    sessiontype TEXT NOT NULL,
                    FOREIGN KEY (car_id) REFERENCES cars(id),
                    FOREIGN KEY (track_id) REFERENCES tracks(id)
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS referencetimes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    track_id INTEGER NOT NULL,
                    carclass_id INTEGER NOT NULL,
                    laptime REAL NOT NULL,
                    date_set TEXT,
                    source TEXT,
                    FOREIGN KEY (carclass_id) REFERENCES car_classes(id),
                    FOREIGN KEY (track_id) REFERENCES tracks(id)
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS fuelusage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    track_id INTEGER NOT NULL,
                    car_id INTEGER NOT NULL,
                    fuel_usage REAL NOT NULL,
                    ve_usage REAL DEFAULT NULL,
                    UNIQUE(track_id, car_id)
                    FOREIGN KEY (car_id) REFERENCES cars(id),
                    FOREIGN KEY (track_id) REFERENCES tracks(id)
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS strategies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    track_id INTEGER NOT NULL,
                    car_id INTEGER NOT NULL,
                    race_minutes INTEGER NOT NULL,
                    laptime_override REAL,
                    laps_override INTEGER,
                    usage_multiplier INTEGER,
                    fuel_capacity_override INTEGER,
                    ve_capacity_override INTEGER,
                    FOREIGN KEY (car_id) REFERENCES cars(id),
                    FOREIGN KEY (track_id) REFERENCES tracks(id)
                )
            """)

