from Repositories.repositories import Repositories
from models import *
import math

class StrategyService:

    def __init__(
        self,
        repos: Repositories
    ):
        self.repos = repos
        self.car_repo = repos.car
        self.reference_repo = repos.reference
        self.fuel_repo = repos.fuel
        self.strategy_repo = repos.strategy
        self.class_repo = repos.classes
        self.track_repo = repos.track

    def get_laptime(self, strategy: Strategy) -> float:
        if strategy.laptime_override is not None:
            return strategy.laptime_override
        else:
            track_id = strategy.track_id
            car_id = strategy.car_id
            car = self.car_repo.get_by_id(car_id)
            if car is None:
                raise ValueError(f"Car {strategy.car_id} not found")
            class_id = car.carclass_id
            reference = self.reference_repo.get_best_reference(track_id, class_id)
            if reference is None:
                raise ValueError(f"Reference laptime not found")
            return reference.laptime

    def get_race_laps(self, strategy: Strategy) -> int:
        if strategy.laps_override is not None:
            return strategy.laps_override
        else:
            laptime = self.get_laptime(strategy)
            length = strategy.race_minutes
            length_seconds = length*60
            laps_raw = length_seconds / laptime
            laps = math.ceil(laps_raw)
            return laps

    def get_qual_laps(self, strategy: Strategy) -> int:
        laptime = self.get_laptime(strategy)
        length = strategy.qual_minutes
        length_seconds = length*60
        laps_raw = length_seconds / laptime
        laps = math.ceil(laps_raw)
        return laps

    def get_fuel_usage(self, strategy: Strategy) -> float:
        car_id = strategy.car_id
        track_id = strategy.track_id
        usage = self.fuel_repo.get_by_track_car(track_id, car_id)
        if usage is None:
            raise ValueError(f"Fuel usage not found")
        realusage = usage.fuel_usage * strategy.usage_multiplier
        return realusage

    def get_fuel_capacity(self, strategy: Strategy) -> int:
        if strategy.fuel_capacity_override is not None:
            return strategy.fuel_capacity_override
        else:
            car = self.car_repo.get_by_id(strategy.car_id)
            if car is None:
               raise ValueError(f"Car {strategy.car_id} not found")
            if (self.class_repo.get_by_id(car.carclass_id) == "LMP2 (WEC)") and (self.track_repo.get_by_id(strategy.track_id).name == "Le Mans"):
                return 75
            return car.fuel_capacity

    def get_ve_usage(self, strategy: Strategy) -> float | None:
            car_id = strategy.car_id
            track_id = strategy.track_id
            usage = self.fuel_repo.get_by_track_car(track_id, car_id)
            if (usage is None):
                raise ValueError(f"VE usage not found")
            if (usage.ve_usage is None):
                return None
            realusage = usage.ve_usage * strategy.usage_multiplier
            factor = self.get_ve_capacity_factor(strategy)

            return realusage * factor
    
    def get_ve_capacity_factor(self, strategy: Strategy) -> float:
        if strategy.ve_capacity_override is None:
            return 1
        else:
            return 100/strategy.ve_capacity_override

    def get_fuel_stint_laps(self, strategy: Strategy) -> float:
        capacity = self.get_fuel_capacity(strategy)
        usage = self.get_fuel_usage(strategy)
        laps = capacity/usage
        return laps

    def get_ve_stint_laps(self, strategy: Strategy) -> float | None:
        capacity = 100
        usage = self.get_ve_usage(strategy)
        if (capacity is None) or (usage is None):
            return None
        laps = capacity/usage
        return laps

    def get_limiting_stint_laps(self, strategy: Strategy) -> float:
        fuel_laps = self.get_fuel_stint_laps(strategy)
        ve_laps = self.get_ve_stint_laps(strategy)

        if ve_laps is None:
            return fuel_laps
        laps = min(fuel_laps, ve_laps)
        return laps

    def get_limiting_factor(self, strategy: Strategy) -> str:
        fuel_laps = self.get_fuel_stint_laps(strategy)
        ve_laps = self.get_ve_stint_laps(strategy)

        if ve_laps is None:
            return "Fuel"
        if fuel_laps < ve_laps:
            return "Fuel"
        else:
            return "VE"

    def get_stints_required(self, strategy: Strategy) -> float:
        race_laps = self.get_race_laps(strategy)
        stint_length = self.get_limiting_stint_laps(strategy)
        return race_laps/stint_length

    def build_stints_from_length(
    self,
    race_laps: int,
    stint_length: int
    ) -> list[int]:
        if stint_length <= 0:
            raise ValueError("Stint length must be greater than 0")

        stints = []
        laps_remaining = race_laps

        while laps_remaining > 0:
            laps = min(stint_length, laps_remaining)
            stints.append(laps)
            laps_remaining -= laps

        return stints

    def build_push_stint_lengths(self, strategy: Strategy) -> list[int]:
        race_laps = self.get_race_laps(strategy)
        stint_length = math.floor(self.get_limiting_stint_laps(strategy))
        return self.build_stints_from_length(race_laps, stint_length)

    def build_plus_stint_lengths(self, strategy: Strategy) -> list[int]:
            race_laps = self.get_race_laps(strategy)
            stint_length = math.floor(self.get_limiting_stint_laps(strategy))+1
            return self.build_stints_from_length(race_laps, stint_length)

    def build_save_stint_lengths(self, strategy: Strategy) -> list[int] | None:
        race_laps = self.get_race_laps(strategy)
        push_stints = len(self.build_push_stint_lengths(strategy))
        stints_required = push_stints-1
        if stints_required <= 0:
            return None
        stint_length = math.floor(race_laps/stints_required)
        leftovers = race_laps-(stints_required*stint_length)
        stints = []
        laps_remaining = race_laps
        while laps_remaining > 0:
            if len(stints)==0:
                stints.append(stint_length)
                laps_remaining -= stint_length
            else:
                if leftovers > 0:
                    stints.append(stint_length+1)
                    laps_remaining -= (stint_length+1)
                    leftovers -= 1 
                else:
                    stints.append(stint_length)
                    laps_remaining -= stint_length
        return stints
        

    def get_stint_fuel_usage(self, strategy: Strategy, stint_length: int) -> float:
        capacity = self.get_fuel_capacity(strategy)
        laps_cap = self.get_fuel_stint_laps(strategy)
        if stint_length > laps_cap:
            return capacity/stint_length
        return self.get_fuel_usage(strategy)        

    def get_stint_ve_usage(self, strategy: Strategy, stint_length: int) -> float | None:
        capacity = 100
        usage = self.get_ve_usage(strategy)
        if usage is None:
            return None
        laps_cap = self.get_ve_stint_laps(strategy)
        if stint_length > laps_cap:
            return capacity/stint_length
        return usage

    def build_stints(self, strategy: Strategy, stint_lengths: list[int], target_stint_length: int | None = None) -> list[Stint]:
        stints=[]
        laptime = self.get_laptime(strategy)
        laps_done = 0
        for i, laps in enumerate(stint_lengths, start=1):
            target_length = target_stint_length if target_stint_length is not None else laps

            fuel_usage = self.get_stint_fuel_usage(strategy, target_length)
            fuel_capacity = self.get_fuel_capacity(strategy)
            fuel = math.ceil(min(laps * fuel_usage, fuel_capacity))
            fuel_usage_real = fuel/laps

            ve_usage = self.get_stint_ve_usage(strategy, target_length)
            if ve_usage is not None:
                ve = math.ceil(min(laps * ve_usage, 100))
                ve_usage_real = ve/laps
                fr = fuel/ve
            else:
                ve = None
                ve_usage_real = None
                fr = None

            #Placeholder
            tirechange = TireChange(changed_wheels=set(), compound=None, new_tires=None)

            start_lap = laps_done+1
            laps_done += laps

            stints.append(
                Stint(
                    stint_number=i,
                    laps = laps,
                    start_lap=start_lap,
                    end_lap = laps_done,
                    fuel_per_lap = fuel_usage_real,
                    fuel_used = fuel,
                    ve_per_lap = ve_usage_real,
                    ve_used = ve,
                    stint_time = laps*laptime,
                    tire_change=tirechange,
                    fuel_ratio = fr
                )
            )
        return stints

    def build_push_plan(self, strategy: Strategy) -> RacePlan:
        target_length = math.floor(self.get_limiting_stint_laps(strategy))
        stint_lengths = self.build_push_stint_lengths(strategy)
        race_laps = self.get_race_laps(strategy)
        make_home = race_laps - target_length

        stints = self.build_stints(
            strategy=strategy,
            stint_lengths=stint_lengths,
            target_stint_length=target_length
        )
        return RacePlan(
            name = "Push Plan",
            race_laps = race_laps,
            pit_stops = len(stints) - 1,
            make_home_lap=make_home,
            stints = stints
        )

    def build_plus_plan(self, strategy: Strategy) -> RacePlan:
        target_length = math.floor(self.get_limiting_stint_laps(strategy))+1
        stint_lengths = self.build_plus_stint_lengths(strategy)
        race_laps = self.get_race_laps(strategy)
        make_home = race_laps - (target_length-1)

        stints = self.build_stints(
            strategy=strategy,
            stint_lengths=stint_lengths,
            target_stint_length=target_length
        )
        return RacePlan(
            name = "Plus One Plan",
            race_laps = race_laps,
            pit_stops = len(stints) - 1,
            make_home_lap=make_home,
            stints = stints
        )

    def build_save_plan(self, strategy: Strategy) -> RacePlan | None:
        stint_lengths = self.build_save_stint_lengths(strategy)
        race_laps = self.get_race_laps(strategy)
        push_stint = math.floor(self.get_limiting_stint_laps(strategy))
        make_home = race_laps - push_stint

        if stint_lengths is None:
            return None

        stints = self.build_stints(
            strategy=strategy,
            stint_lengths=stint_lengths
        )
        return RacePlan(
            name = "Save Plan",
            race_laps = race_laps,
            pit_stops = len(stints)-1,
            make_home_lap=make_home,
            stints = stints
        )

    def build_quali_plan(self, strategy: Strategy) -> QualiPlan:
        qual_laps = self.get_qual_laps(strategy)
        fuel_usage = self.get_fuel_usage(strategy)+0.2
        fuel_needed = math.ceil(fuel_usage * qual_laps)
        car = self.car_repo.get_by_id(strategy.car_id)
        if car.ve:
            fuel_ratio = fuel_needed/100
        else:
            fuel_ratio=None

        return QualiPlan(
            fuel_needed=fuel_needed,
            fuel_usage = fuel_usage,
            fuel_ratio=fuel_ratio,
            laps=qual_laps
        )

    def calculate(self, strategy: Strategy) -> StrategyResult:
        race_laps = self.get_race_laps(strategy)
        qualplan = self.build_quali_plan(strategy)
        plans=[]
        plans.append(self.build_push_plan(strategy))
        plans.append(self.build_plus_plan(strategy))
        save_plan = self.build_save_plan(strategy)
        if save_plan is not None:
            plans.append(save_plan)
        
        return StrategyResult(
            race_laps=race_laps,
            quali_plan=qualplan,
            raceplan_presets = plans
        )