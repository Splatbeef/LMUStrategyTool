from dataclasses import dataclass
import datetime as dt

@dataclass
class LapTime:
    id: int | None
    track_id: int
    car_id: int
    laptime: float        #in seconds
    date_set: dt.date
    sessiontype: str

@dataclass
class ReferenceTime:
    id: int | None
    track_id: int
    carclass_id: int
    laptime: float        #in seconds
    date_set: dt.date

@dataclass
class Strategy:
    id: int | None
    track_id: int
    car_id: int
    race_minutes: int
    laptime: float
    stints: float

@dataclass
class Car:
    id: int | None
    name: str
    carclass_id: int
    fuel_capacity: int
    ve: bool

@dataclass
class Track:
    id: int | None
    name: str
    layout: str

@dataclass
class CarClass:
    id: int | None
    name: str

@dataclass
class FuelUsage:
    id: int | None
    car_id: int
    track_id: int
    fuel_usage: float
    ve_usage: float | None
