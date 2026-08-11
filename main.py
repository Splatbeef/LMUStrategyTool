import datetime as dt
import pandas as pd
import flet as ft

from models import *
from Repositories.repositories import *
from Repositories.carclass_repository import *

from services.database_service import *

from views.strategyview import *
from views.carsview import *
from views.tracksview import *
from views.fuelusageview import *
from views.referenceview import *


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
                    icon=ft.Icons.ROUTE,
                    label="Tracks"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.DIRECTIONS_CAR,
                    label="Cars"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.LOCAL_GAS_STATION,
                    label="Fuel"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.TIMER,
                    label="Reference Times"
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
                self.show_tracks()

            case 3:
                self.show_cars()

            case 4:
                self.show_fuel()

            case 5:
                self.show_reference_times()

    def show_home(self):
        self.content.content = ft.Text("Home")
        self.page.update()

    def show_strategy(self):
        self.content.content = StrategyView(self.repos)
        self.page.update()

    def show_tracks(self):
        self.content.content = TracksView(self.repos.track)
        self.page.update()

    def show_cars(self):
        self.content.content = CarsView(self.repos.car, self.repos.classes)
        self.page.update()

    def show_fuel(self):
        self.content.content = FuelUsageView(self.repos.car, self.repos.classes, self.repos.fuel, self.repos.track)
        self.page.update()

    def show_reference_times(self):
        self.content.content = ReferenceView(self.repos.reference, self.repos.track, self.repos.classes, self.repos.car)
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

    def seed_cars():
        
        hypercars=["Ferrari 499P", "Toyota GR010", "Porsche 963", "Genesis GMR001", "Peugeot 9X8 EVO", "Peugeot 9X8","Isotta Fraschini Tipo 6","AMR Valkyrie LMH","Cadillac V Series.R", "Alpine A424","Lamborghini SC63","BMW M Hybrid V8 EVO","Glickenhaus SGC 007"]
        class_id = repos.classes.get_by_name("Hypercar").id
        for carname in hypercars:
            if not repos.car.exists(carname):
                repos.car.add(
                    Car(
                        id=None,
                        name=carname,
                        carclass_id = class_id,
                        fuel_capacity = 110,
                        ve=True
                    )
                )
        carname="Oreca 07 Gibson ELMS"
        class_id = repos.classes.get_by_name("LMP2 (ELMS)").id
        if not repos.car.exists(carname):
            repos.car.add(
                Car(
                    id=None,
                    name=carname,
                    carclass_id = class_id,
                    fuel_capacity = 75,
                    ve=False
                )
            )

        carname="Oreca 07 Gibson 2024"
        class_id = repos.classes.get_by_name("LMP2 (WEC)").id
        if not repos.car.exists(carname):
            repos.car.add(
                Car(
                    id=None,
                    name=carname,
                    carclass_id = class_id,
                    fuel_capacity = 63,
                    ve=False
                )
            )
        lmp3s=["Ligier JS P325 LMP3","Duqueine D09 LMP3","Ginetta G61 P325 LMP3","Adess AD25 LMP3"]
        class_id = repos.classes.get_by_name("LMP3").id
        for carname in lmp3s:
            if not repos.car.exists(carname):
                        repos.car.add(
                            Car(
                                id=None,
                                name=carname,
                                carclass_id = class_id,
                                fuel_capacity = 100,
                                ve=False
                            )
                        )
        gt3s=["Porsche 992 LMGT3 EVO","Mercedes AMG LMGT3","Huracan EVO2 LMGT3","Lexus RC-F LMGT3","AMR Vantage LMGT3","Ford Mustang LMGT3 EVO","Ferrari 296 LMGT3 EVO","McLaren 720s LMGT3 EVO","Corvette Z06 LMGT3","BMW M4 LMGT3"]
        class_id = repos.classes.get_by_name("LMGT3").id
        for carname in gt3s:
            if not repos.car.exists(carname):
                        repos.car.add(
                            Car(
                                id=None,
                                name=carname,
                                carclass_id = class_id,
                                fuel_capacity = 120,
                                ve=True
                            )
                        )
        class_id = repos.classes.get_by_name("LMGTE").id
        gtes={"Porsche 911 RSR GTE":100,"Ferrari 488 GTE EVO":86,"Corvette C8.R GTE":91,"Aston Martin Vantage AMR GTE":97}
        for carname, capacity in gtes.items():
            if not repos.car.exists(carname):
                        repos.car.add(
                            Car(
                                id=None,
                                name=carname,
                                carclass_id = class_id,
                                fuel_capacity = capacity,
                                ve=False
                            )
                        )
    seed_cars()


def main(page: ft.Page):
    page.title="LMU Strategy Tool"

    db=DatabaseService()
    repos = Repositories(db)

    seed_database(repos)

    MainApp(
        page=page,
        repos=repos)

if __name__ == "__main__":
    ft.run(main)