from Repositories.carclass_repository import CarClassRepository
from Repositories.track_repository import TrackRepository
from Repositories.car_repository import CarRepository
from Repositories.laptime_repository import LapTimeRepository
from Repositories.referencetime_repository import ReferenceTimeRepository
from Repositories.fuel_repository import FuelRepository
from Repositories.strategy_repository import StrategyRepository
from Repositories.alias_repository import *

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