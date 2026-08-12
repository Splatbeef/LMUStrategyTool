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
    qual_minutes: int
    laptime_override: float | None
    laps_override: int | None
    usage_multiplier: int
    fuel_capacity_override: int | None
    ve_capacity_override: int | None
    tire_limit: int | None

@dataclass
class TireChange:
    changed_wheels: set[str]
    compound: str | None
    new_tires: bool | None

@dataclass
class Stint:
    stint_number: int
    laps: int
    start_lap: int
    end_lap: int
    fuel_per_lap: float
    fuel_used: int
    ve_per_lap: float | None
    ve_used: int | None
    stint_time: float
    tire_change: TireChange
    fuel_ratio: float | None

@dataclass
class RacePlan:
    name: str
    race_laps: int
    pit_stops: int
    make_home_lap: int | None #Pitting at the end of this lap for full tank will get you home
    stints: list[Stint]

@dataclass
class QualiPlan:
    fuel_needed: int
    fuel_usage: float
    fuel_ratio: float | None
    laps: int

@dataclass
class StrategyResult:
    quali_plan: QualiPlan
    raceplan_presets: list[RacePlan]

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

@dataclass
class TrackAlias:
    id: int | None
    alias: str
    name: str
    layout: str

@dataclass
class CarAlias:
    id: int | None
    alias: str
    name: str

