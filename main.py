import datetime as dt
import flet as ft
import datetime as dt
import json
import sys
from pathlib import Path
import requests
from packaging.version import Version
import webbrowser

from models import *
from repositories.repositories import *

from services.database_service import *
from services.reference_service import *

from views.strategyview import *
from views.carsview import *
from views.tracksview import *
from views.fuelusageview import *
from views.referenceview import *
from views.laptimesview import *
from views.settingsview import *
from views.homeview import *


class MainApp:

    def __init__(self, page: ft.Page, repos: Repositories):
        self.repos = repos
        self.page = page

        self.content = ft.Container(expand=True)

        self.nav = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.HOME,
                    label="Home"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.ANALYTICS,
                    label="Strategies"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.TIMER,
                    label="Laptimes"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.LOCAL_GAS_STATION,
                    label="Fuel"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.ROUTE,
                    label="Tracks"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.DIRECTIONS_CAR,
                    label="Cars"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.LEADERBOARD,
                    label="Reference Times"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS,
                    label="Settings"
                )
                
            ],
            on_change=self.nav_changed
        )

        self.page.add(
            ft.Row(
                [
                    self.nav,
                    ft.VerticalDivider(width=1),
                    self.content
                ],
                expand=True
            )
        )

        self.show_home()

    def nav_changed(self, e):

        match e.control.selected_index:

            case 0:
                self.show_home()

            case 1:
                self.show_strategy()

            case 2:
                self.show_laptimes()

            case 3:
                self.show_fuel()

            case 4:
                self.show_tracks()

            case 5:
                self.show_cars()

            case 6:
                self.show_reference_times()

            case 7:
                self.show_settings()

    def show_home(self):
        self.content.content = HomeView(self.repos)
        self.page.update()

    def show_strategy(self):
        self.content.content = StrategyView(self.repos)
        self.page.update()

    def show_laptimes(self):
        self.content.content = LapTimesView(self.repos)
        self.page.update()

    def show_tracks(self):
        self.content.content = TracksView(self.repos.track)
        self.page.update()

    def show_cars(self):
        self.content.content = CarsView(self.repos)
        self.page.update()

    def show_fuel(self):
        self.content.content = FuelUsageView(self.repos)
        self.page.update()

    def show_reference_times(self):
        self.content.content = ReferenceView(self.repos)
        self.page.update()

    def show_settings(self):
        self.content.content = SettingsView(self.repos)
        self.page.update()

def seed_database(repos: Repositories):

    def seed_classes():
        if not repos.classes.exists("Hypercar"):
            repos.classes.add(
                CarClass(
                    id=None,
                    name="Hypercar"
                )
            )

        if not repos.classes.exists("LMGT3"):
            repos.classes.add(
                CarClass(
                    id=None,
                    name="LMGT3"
                )
            )

        if not repos.classes.exists("LMP3"):
            repos.classes.add(
                CarClass(
                    id=None,
                    name="LMP3"
                )
            )

        if not repos.classes.exists("LMP2 (WEC)"):
            repos.classes.add(
                CarClass(
                    id=None,
                    name="LMP2 (WEC)"
                )
            )
        if not repos.classes.exists("LMP2 (ELMS)"):
            repos.classes.add(
                CarClass(
                    id=None,
                    name="LMP2 (ELMS)"
                )
            )
        if not repos.classes.exists("LMGTE"):
            repos.classes.add(
                CarClass(
                    id=None,
                    name="LMGTE"
                )
            )
    seed_classes()

    if getattr(sys, "frozen", False):
        BASE_DIR = Path(sys._MEIPASS)
    else:
        BASE_DIR = Path(__file__).resolve().parent
    SEED_DIR = BASE_DIR / "seeding_data"

    with open(SEED_DIR / 'cars.json', encoding="utf-8") as f:
        dct = json.load(f)
        for classname, cars in dct.items():
            class_id = repos.classes.get_by_name(classname).id
            for car in cars:
                if not repos.car.exists(car["name"]):
                    repos.car.add(
                            Car(
                                id=None,
                                name=car["name"],
                                carclass_id = class_id,
                                fuel_capacity = car["fuel_capacity"],
                                ve=car["ve"]
                            )
                        )

    with open(SEED_DIR / 'caraliases.json', encoding="utf-8") as f:
        dct = json.load(f)
        for name, aliases in dct.items():
            for alias in aliases:
                if not repos.caralias.exists(alias):
                    repos.caralias.add(CarAlias(
                        id=None,
                        alias=alias,
                        name=name
                    ))

    with open(SEED_DIR / 'trackaliases.json', encoding="utf-8") as f:
        dct=json.load(f)
        for alias, details in dct.items():
            name = details["name"]
            layout = details["layout"]
            if not repos.trackalias.exists(alias):
                repos.trackalias.add(TrackAlias(
                    id=None,
                    alias=alias,
                    name=name,
                    layout=layout
                ))

    def seed_settings():
        if not repos.settings.exists("Version"):
            repos.settings.add(
                Setting(
                    id=None,
                    key="Version",
                    value_str = APP_VERSION,
                    value_bool = None,
                    value_int = None,
                    value_float = None
                )
            )
        if not repos.settings.exists("Laptime Sessiontypes"):
            repos.settings.add(
                Setting(
                    id=None,
                    key="Laptime Sessiontypes",
                    value_str = None,
                    value_bool = None,
                    value_int = 1,          #0 - Quali and Race, 1 - Quali, Race, Practice, 2 - Quali, Race, Quali Practice, Race Practice
                    value_float = None
                )
            )
        if not repos.settings.exists("Laptime Multiplier"):
            repos.settings.add(
                Setting(
                    id=None,
                    key="Laptime Multiplier",
                    value_str = None,
                    value_bool = None,
                    value_int = None,
                    value_float = 1.005
                )
            )
        if not repos.settings.exists("Autosync"):
            referenceservice = ReferenceService(repos)
            referenceservice.sync()
            repos.settings.add(
                Setting(
                    id=None,
                    key="Autosync",
                    value_str = dt.date.today(),
                    value_bool = True,
                    value_int = None,
                    value_float = None,
                )
            )
        else:
            sync_setting = repos.settings.get_by_key("Autosync")
            if (sync_setting.value_str != str(dt.date.today())) and sync_setting.value_bool:
                referenceservice = ReferenceService(repos)
                referenceservice.sync()
                repos.settings.update(
                    Setting(
                        id=sync_setting.id,
                        key="Autosync",
                        value_str = dt.date.today(),
                        value_bool = sync_setting.value_bool,
                        value_int = None,
                        value_float = None,
                    )
                )
    seed_settings()

def main(page: ft.Page):
    page.title="LMU Strategy Tool"
    page.window.icon="icon.ico"

    db=DatabaseService()
    repos = Repositories(db)

    seed_database(repos)

    MainApp(
        page=page,
        repos=repos)

if __name__ == "__main__":
    APP_VERSION="1.0.0"
    ft.run(main)