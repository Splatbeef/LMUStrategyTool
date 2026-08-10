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
        self.content.content = StrategyView()
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