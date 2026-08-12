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
        self.content.content = ReferenceView(self.repos.reference, self.repos.track, self.repos.classes, self.repos.car, self.repos.trackalias, self.repos.caralias)
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
        
        hypercars=["Ferrari 499P", "Toyota GR010/TR010", "Porsche 963", "Genesis GMR001", "Peugeot 9X8 EVO", "Peugeot 9X8","Isotta Fraschini Tipo 6","Aston Martin Valkyrie LMH","Cadillac V-Series.R", "Alpine A424","Lamborghini SC63","BMW M Hybrid V8 EVO","Glickenhaus SCG 007","Vanwall Vandervell 680"]
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
        carname="Oreca 07 Gibson (ELMS)"
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

        carname="Oreca 07 Gibson (WEC)"
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
        lmp3s=["Ligier JS P325","Duqueine D09","Ginetta-G61-LT-P325-Evo","Adess AD25"]
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
        gt3s=["Porsche 911 GT3 R LMGT3","Mercedes-AMG LMGT3","Lamborghini Huracan LMGT3 EVO2","Lexus RC-F LMGT3","Aston Martin Vantage AMR LMGT3","Ford Mustang LMGT3","Ferrari 296 LMGT3","McLaren 720s LMGT3 EVO","Chevrolet Corvette Z06 LMGT3.R","BMW M4 LMGT3"]
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
        gtes={"Porsche 911 RSR-19 GTE":100,"Ferrari 488 GTE EVO":86,"Chevrolet Corvette C8.R GTE":91,"Aston Martin Vantage AMR GTE":97}
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

    def seed_car_aliases():
        names=["Aston Martin Vantage AMR LMGT3", "Aston Martin Valkyrie LMH", "Ferrari 499P", "Porsche 963", "Genesis GMR001", "Peugeot 9X8 EVO", "Peugeot 9X8","Isotta Fraschini Tipo 6", "Alpine A424","Lamborghini SC63","BMW M Hybrid V8 EVO","Glickenhaus SCG 007", "Vanwall Vandervell 680","Lexus RC-F LMGT3","McLaren 720s LMGT3 EVO","BMW M4 LMGT3","Ferrari 488 GTE EVO","Chevrolet Corvette C8.R GTE","Aston Martin Vantage AMR GTE", "Ferrari 296 LMGT3", "Ford Mustang LMGT3"]
        for name in names:
            if not repos.caralias.exists(name):
                repos.caralias.add(CarAlias(
                    id=None,
                    alias=name,
                    name=name
                ))
        name="BMW M Hybrid V8"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="BMW M Hybrid V8 EVO"
            ))
        name="Toyota GR010"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Toyota GR010/TR010"
            ))
        name="Cadillac V Series.R"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Cadillac V-Series.R"
            ))
        name="AMR Valkyrie LMH"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Aston Martin Valkyrie LMH"
            ))        
        name="Oreca 07 Gibson ELMS"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Oreca 07 Gibson (ELMS)"
            ))
        name="Oreca 07 ELMS"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Oreca 07 Gibson (ELMS)"
            ))
        name="Oreca 07 Gibson 2024"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Oreca 07 Gibson (WEC)"
            ))
        name="Oreca 07 2024"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Oreca 07 Gibson (WEC)"
            ))
        name="Ginetta G61 P325 LMP3"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Ginetta G61-LT-P325-Evo"
            ))
        name="Ginetta G61 LT P325 EVO"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Ginetta G61-LT-P325-Evo"
            ))
        name="Ligier JS P325 LMP3"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Ligier JS P325"
            ))
        name="Duqueine D09 P3"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Duqueine D09"
            ))
        name="Adess AD25 LMP3"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Adess AD25"
            ))
        name="Porsche 992 LMGT3 EVO"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Porsche 911 GT3 R LMGT3"
            ))
        name="Porsche 992 LMGT3"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Porsche 911 GT3 R LMGT3"
            ))
        name="Mercedes AMG LMGT3"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Mercedes-AMG LMGT3"
            ))
        name="Huracan EVO2 LMGT3"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Lamborghini Huracan LMGT3 EVO2"
            ))
        name="Lamborghini Huracan EVO2 LMGT3"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Lamborghini Huracan LMGT3 EVO2"
            ))
        name="AMR Vantage LMGT3"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Aston Martin Vantage AMR LMGT3"
            ))
        name="Ford Mustang LMGT3 EVO"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Ford Mustang LMGT3"
            ))
        name="Ferrari 296 LMGT3 EVO"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Ferrari 296 LMGT3"
            ))
        name="Chevrolet Corvette Z06 LMGT3"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Chevrolet Corvette Z06 LMGT3.R"
            ))
        name="Porsche 911 RSR GTE"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Porsche 911 RSR-19 GTE"
            ))
        name="Porsche 911 RSR 19 GTE"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Porsche 911 RSR-19 GTE"
            ))
        name="Chevrolet Corvette C8R GTE"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Chevrolet Corvette C8.R GTE"
            ))
        name="Lexus RCF LMGT3"
        if not repos.caralias.exists(name):
            repos.caralias.add(CarAlias(
                id=None,
                alias=name,
                name="Lexus RC-F LMGT3"
            ))
        
    seed_car_aliases()

    def seed_track_aliases():
        aliases={'Silverstone International': ("Silverstone", "International"),
 'Monza Curva Grande': ("Monza", "Curva Grande"),
 'Laguna Seca': ("Laguna Seca", ""),
 'Le Mans Mulsanne': ("Le Mans","Mulsanne"),
 'Silverstone National': ("Silverstone","National"),
 'Barcelona': ("Barcelona",""),
 'Interlagos': ("Interlagos",""),
 'Bahrain International': ("Bahrain",""),
 'Spa Francorchamps': ("Spa-Francorchamps",""),
 'Paul Ricard ELMS': ("Paul Ricard",""),
 'Bahrain Outer': ("Bahrain","Outer"),
 'Fuji Classic': ("Fuji","Classic"),
 'Bahrain Paddock': ("Bahrain","Paddock"),
 'Bahrain Endurance': ("Bahrain","Endurance"),
 'Silverstone WEC': ("Silverstone",""),
 'Paul Ricard 1A V2': ("Paul Ricard","1A-V2"),
 'Paul Ricard 1A': ("Paul Ricard","1A"),
 'Le Mans': ("Le Mans",""),
 'Monza': ("Monza",""),
 'Portimao': ("Portimao",""),
 'Paul Ricard 3A': ("Paul Ricard","3A"),
 'COTA': ("CotA",""),
 'Sebring': ("Sebring",""),
 'Qatar': ("Qatar",""),
 'Sebring School': ("Sebring","School"),
 'Imola': ("Imola",""),
 'Paul Ricard 1A V2 Short': ("Paul Ricard","1A-V2-Short"),
 'Daytona': ("Daytona",""),
 'COTA National': ("CotA","National"),
 'Qatar Short': ("Qatar","Short"),
 'Fuji': ("Fuji","")}
        for alias, names in aliases.items():
            name = names[0]
            layout = names[1]
            if not repos.trackalias.exists(alias):
                repos.trackalias.add(TrackAlias(
                    id=None,
                    alias=alias,
                    name=name,
                    layout=layout
                ))
    seed_track_aliases()

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