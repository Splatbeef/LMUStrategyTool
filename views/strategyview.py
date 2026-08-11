import flet as ft
from Repositories.repositories import *
from models import *

class StrategyView(ft.Container):
    def __init__(self, repos: Repositories):
        self.repos = repos
        self.strat_repo = repos.strategy
        self.car_repo = repos.car
        self.track_repo = repos.track
        self.class_repo = repos.classes

        self.content_area = ft.Container(expand=True)

        self.strategy_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Track")),
                ft.DataColumn(ft.Text("Car")),
                ft.DataColumn(ft.Text("Race Length")),
            ],
            rows=[]
        )

        
        super().__init__(
            expand=True,
            content=self.content_area
        )

        self.show_library()
        

    def refresh_library(self):
        self.strategy_table.rows.clear()
        strategies = self.strat_repo.get_all()

        for strategy in strategies:
            car = self.car_repo.get_by_id(strategy.car_id)
            track = self.track_repo.get_by_id(strategy.track_id)
            if track is None:
                trackstr = ""
            elif len(track.layout) > 1:
                trackstr = f"{track.name} ({track.layout})"
            else:
                trackstr = track.name
            self.strategy_table.rows.append(
                    ft.DataRow(
                        on_select_change=lambda e, s=strategy: self.show_editor(s),
                        cells=[
                            ft.DataCell(ft.Text(strategy.name)),
                            ft.DataCell(ft.Text(trackstr)),
                            ft.DataCell(ft.Text(car.name)),
                            ft.DataCell(ft.Text(f"{strategy.race_minutes} minutes"))
                        ]
                    )
                )
        #self.update()

    def show_library(self):
        self.refresh_library()
        
        self.content_area.content = ft.Column([
            ft.Row([
                ft.Text("Strategies", size=28, weight=ft.FontWeight.BOLD),
                ft.Button(content="New Strategy", on_click=lambda e: self.show_editor(None))
            ]),

            self.strategy_table
        ])
        # if self.page:
        #     self.update()

    def show_editor(self, strategy:Strategy = None):

        self.current_strategy = strategy

        self.strategy_name = ft.TextField(
            label="Strategy Name",
            value="" if strategy is None else strategy.name
        )

        self.track_dropdown = ft.Dropdown(
            label="Track"
        )

        self.car_dropdown = ft.Dropdown(
            label="Car"
        )

        self.race_minutes = ft.TextField(
            label="Race Length (minutes)",
            value="" if strategy is None else str(strategy.race_minutes)
        )

        self.qual_minutes = ft.TextField(
            label="Qualifying Length (minutes)",
            value="" if strategy is None else str(strategy.qual_minutes)
        )

        self.tire_limit = ft.TextField(
            label="Tire Limit",
            value="" if strategy is None else str(strategy.tire_limit)
        )

        self.multiplier = ft.TextField(
            label="Fuel Usage Multiplier",
            value="1" if strategy is None else str(strategy.usage_multiplier)
        )

        self.fuel_capacity = ft.TextField(
            label="Fuel Capacity Override",
            value = "" if strategy is None else str(strategy.fuel_capacity_override)
        )

        self.ve_capacity = ft.TextField(
            label="VE Capacity Override",
            value = "" if strategy is None else str(strategy.ve_capacity_override)
        )

        self.laptime_override = ft.TextField(
            label="Laptime Override (s)",
            value = "" if strategy is None else str(strategy.laptime_override)
        )

        self.laps_override = ft.TextField(
            label="Laps Override",
            value = "" if strategy is None else str(strategy.laps_override)
        )

        self.calculate_button = ft.Button(content="Calculate")
        self.save_button = ft.Button(content="Save")
        self.delete_button = ft.Button(content="Delete")

        self.load_tracks()
        self.load_cars()

        self.results = ft.Column()

        self.content_area.content = ft.Column([
            ft.Row([
                ft.Button(
                    content="← Back",
                    on_click=lambda e: self.show_library()
                ),

                ft.Text(
                    "Strategy Editor",
                    size=28,
                    weight=ft.FontWeight.BOLD
                )
            ]),

            ft.Divider(),

            ft.Row([
                ft.Column([
                    self.strategy_name,
                    self.race_minutes,
                    self.qual_minutes
                ]),
                ft.Column([
                    self.track_dropdown,
                    self.car_dropdown
                ]),
                ft.Column([
                    self.tire_limit,
                    self.multiplier,
                    self.fuel_capacity
                ]),
                ft.Column([
                    self.laptime_override,
                    self.laps_override
                ])
            ]),

            ft.Row([
                self.calculate_button,
                self.save_button,
                self.delete_button
            ]),

            ft.Divider()
        ])

    def load_cars(self):
        self.car_dropdown.options = []

        cars = sorted(
            self.car_repo.get_all(),
            key=lambda c: (
                self.class_repo.get_by_id(c.carclass_id).name,
                c.name.lower()
            )
        )
        
        for c in cars:
            self.car_dropdown.options.append(
            ft.dropdown.Option(
                key=str(c.id),
                text=f"{c.name}"
            ) )

    def load_tracks(self):
        tracks = sorted(
            self.track_repo.get_all(),
            key=lambda t: (t.name.lower(), t.layout.lower())
        )
        for c in tracks:
            if len(c.layout)>0:
                trackstr=f"{c.name} ({c.layout})"
            else:
                trackstr=c.name
            self.track_dropdown.options.append(
                ft.dropdown.Option(
                    key=str(c.id),
                    text=trackstr
                ) 
            )
