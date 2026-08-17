from repositories.carclass_repository import CarClassRepository
from repositories.track_repository import TrackRepository
from repositories.car_repository import CarRepository
from repositories.laptime_repository import LapTimeRepository
from repositories.referencetime_repository import ReferenceTimeRepository
from repositories.fuel_repository import FuelRepository
from repositories.strategy_repository import StrategyRepository
from repositories.alias_repository import *
from repositories.settings_repository import SettingsRepository

class Repositories:

    def __init__(self, db):
        self.classes = CarClassRepository(db)
        self.car = CarRepository(db)
        self.fuel = FuelRepository(db)
        self.reference = ReferenceTimeRepository(db)
        self.strategy = StrategyRepository(db)
        self.track = TrackRepository(db)
        self.laptime = LapTimeRepository(db)
        self.trackalias = TrackAliasRepository(db)
        self.caralias = CarAliasRepository(db)
        self.settings = SettingsRepository(db)