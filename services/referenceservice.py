from models import *
import pandas as pd
import numpy as np
import datetime as dt
import math



class ReferenceService:
    def __init__(self, track_repo, car_repo, reference_repo):
        SHEET_ID = "1uNX-PRtZSxjo6jM848tyLuHawBk0FzWNpVqo9WDYpDI"
        GID = "2029862573"
        self.url = (
            f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export"
            f"?format=csv&gid={GID}"
        )
        self.track_repo = track_repo
        self.car_repo = car_repo
        self.reference_repo = reference_repo

    def sync(self):
        df = self.load_lmu_laptimes()

        cars_all = list(df)[1:]
        cars={}
        for c in cars_all:
            if self.car_repo.exists(c):
                car = self.car_repo.get_by_name(c)
                cars[c]=car


        for name, row in df.iterrows():
            tracktype = row["TrackType"]
            if tracktype == "Track":
                trackname = name
                layout=""
            else:
                trackname, layout = self.find_name_layout(name)

            if not self.track_repo.exists(trackname, layout):
                track = Track(
                    id=None,
                    name=trackname,
                    layout=layout
                )
                self.track_repo.add(track)
            track = self.track_repo.get_by_name_layout(trackname, layout)

            for carname, car in cars.items():
                laptimestr = row[carname]
                laptime = self.parse_laptime(laptimestr)
                if laptime is None:
                    continue
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
        

    def find_name_layout(self, name: str):
        splitname = name.split(" ")
        constructed=""
        layout=""
        found=False
        for txt in splitname:
            if not found:
                constructed+=f" {txt}"
                constructed = constructed.strip()
                if self.track_repo.track_exists(constructed):
                    found=True
                    trackname = constructed
            else:
                layout+=f" {txt}"
                layout = layout.strip()
        return trackname, layout

    def load_lmu_laptimes(self):
        # Load without treating any row as a header
        raw = pd.read_csv(self.url, header=None)

        # Find the row containing "TRACKS & CARS"
        header_row = raw[
            raw.apply(
                lambda row: row.astype(str).str.contains("TRACKS & CARS", case=False, na=False).any(),
                axis=1
            )
        ].index[0]

        # Find the first row containing "Status", this marks the end of useful lap data
        status_matches = raw[
            raw.apply(
                lambda row: row.astype(str).str.strip().eq("Status").any(),
                axis=1
            )
        ]

        if not status_matches.empty:
            end_row = status_matches.index[0]
        else:
            end_row = len(raw)

        # In this sheet, car names start after "TRACKS & CARS"
        header_values = raw.iloc[header_row]

        tracks_cars_col = header_values[
            header_values.astype(str).str.contains("TRACKS & CARS", case=False, na=False)
        ].index[0]

        # Car names are every 3 columns after the TRACKS & CARS column:
        # car name, empty, empty
        # then rows below contain: game version, setup version, laptime
        car_laptime_cols = {}

        col = tracks_cars_col + 1

        while col < raw.shape[1]:
            car_name = raw.iloc[header_row, col]

            if pd.notna(car_name) and str(car_name).strip():       
                car_name = str(car_name).strip()
                laptime_col = col + 2

                if laptime_col < raw.shape[1]:
                    car_laptime_cols[car_name] = laptime_col

            col += 3

        # Track names are usually in either of the two columns before the car data
        possible_track_cols = {"Track": tracks_cars_col - 1, "Layout": tracks_cars_col}

        records = []

        for row_idx in range(header_row + 3, end_row):
            row = raw.iloc[row_idx]

            track = np.nan

            for track_col, index in possible_track_cols.items():
                if index >= 0:
                    value = row.iloc[index]

                    if pd.notna(value) and str(value).strip() != "":
                        track = str(value).strip()
                        tracktype = track_col
                        break

            if pd.isna(track):
                continue

            record = {"Track": track, "TrackType": tracktype}

            for car_name, lap_col in car_laptime_cols.items():
                value = row.iloc[lap_col]

                if pd.isna(value) or str(value).strip() == "":
                    record[car_name] = np.nan
                else:
                    record[car_name] = str(value).strip()

            records.append(record)

        df_laptimes = pd.DataFrame(records)

        if df_laptimes.empty:
            return df_laptimes

        df_laptimes = df_laptimes.set_index("Track")

        return df_laptimes