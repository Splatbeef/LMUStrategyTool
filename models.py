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
    source: str

@dataclass
class Strategy:
    id: int | None
    name: str
    track_id: int
    car_id: int
    race_minutes: int
    laptime_override: float | None
    laps_override: int | None
    usage_multiplier: int
    fuel_capacity_override: int | None
    ve_capacity_override: int | None

@dataclass
class TireChange:
    changed_wheels: set[str]
    compound: str | None
    new_tires: bool | None

@dataclass
class Stint:
    stint_number: int
    laps: int
    fuel_per_lap: float
    fuel_used: float
    ve_per_lap: float | None
    ve_used: float | None
    stint_time: float
    tire_change: TireChange
    fuel_ratio = float | None

@dataclass
class RacePlan:
    race_laps: int
    pit_stops: int
    stints: list[Stint]

@dataclass
class StrategyResult:
    push_plan: RacePlan
    plus_one_plan: RacePlan
    save_plan: RacePlan | None

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
