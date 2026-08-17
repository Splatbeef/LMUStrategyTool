from models import *
import pandas as pd
import numpy as np
import datetime as dt
import math
import requests

from repositories.repositories import *


class ReferenceService:
    def __init__(self, repos: Repositories):
        self.url = "https://gosetups.gg/wp-json/gosetups/v1/laptimes"
        self.track_repo = repos.track
        self.car_repo = repos.car
        self.reference_repo = repos.reference
        self.trackalias_repo = repos.trackalias
        self.caralias_repo = repos.caralias
        self.settings_repo = repos.settings

    def sync(self):
        response = requests.get(self.url, timeout=30)
        response.raise_for_status()

        data = response.json()
        lmu_rows = [
        row
        for row in data["laptimes"]
        if row["game"] == "lmu"
        ]

        missing_track_aliases=[]
        missing_car_aliases=[]
        for row in lmu_rows:
            car_name = row["car_name"]
            alias = self.caralias_repo.get_by_alias(car_name)
            if alias is None:
                if car_name not in missing_car_aliases:
                    missing_car_aliases.append(car_name)
                continue
            else:
                car = self.car_repo.get_by_name(alias.name)

            track_name = row["track_name"]
            alias = self.trackalias_repo.get_by_alias(track_name)
            if alias is None:
                if track_name not in missing_track_aliases:
                    missing_track_aliases.append(track_name)
                continue
            else:
                trackname = alias.name
                layout = alias.layout

                
            if not self.track_repo.exists(trackname, layout):
                track = Track(
                    id=None,
                    name=trackname,
                    layout=layout
                )
                self.track_repo.add(track)
            track = self.track_repo.get_by_name_layout(trackname, layout)

            laptime_ms = row["laptime_ms"]
            if laptime_ms is None:
                continue
            laptime = laptime_ms/1000
            laptime *= self.settings_repo.get_by_key("Laptime Multiplier").value_float
            class_id = car.carclass_id

            if self.reference_repo.exists(track.id, class_id):
                best = self.reference_repo.get_best_reference(track.id, class_id)
                if laptime < best.laptime:
                    newlaptime = ReferenceTime(
                        id = best.id,
                        track_id = track.id,
                        carclass_id = class_id,
                        laptime = laptime,
                        date_set = dt.date.today(),
                        source="GO Setups"
                    )
                    self.reference_repo.update(newlaptime)
            else:
                newlaptime = ReferenceTime(
                        id = None,
                        track_id = track.id,
                        carclass_id = class_id,
                        laptime = laptime,
                        date_set = dt.date.today(),
                        source="GO Setups"
                    )
                self.reference_repo.add(newlaptime)
        return {
            "tracks": sorted(missing_track_aliases),
            "cars": sorted(missing_car_aliases)
        }

    def parse_laptime(self, time) -> float:
        if pd.isna(time):
            return None
        time = str(time)
        if time == "":
            return None
        time = time.strip()
        parts = time.split(".")
        if len(parts) == 3:
            time = f"{parts[0]}:{parts[1]}.{parts[2]}"
        try:
            if ":" in time:
                parts = time.split(":")
                value = (60*int(parts[0]))+float(parts[1])
            else:
                value=float(time)
            return value
        except ValueError:
            print(f"Could not parse laptime: {time}")
            return None

    def text_from_laptime(self, laptime):
        if laptime < 60:
            return f"{laptime:.3f}"
        minutes = math.floor(laptime/60)
        seconds = laptime % 60
        return f"{minutes}:{seconds:06.3f}"   

    def save_track_alias(self, alias, name, layout):
        self.trackalias_repo.add(
            TrackAlias(
                id = None,
                alias = alias,
                name = name,
                layout = layout
            ))

    def save_car_alias(self, alias, name):
        self.caralias_repo.add(
            CarAlias(
                id = None,
                alias = alias,
                name = name,
            ))