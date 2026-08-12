import flet as ft
from Repositories.repositories import *
from models import *
from services.strategy_service import *

class StrategyView(ft.Container):
    def __init__(self, repos: Repositories):
        self.repos = repos
        self.strat_repo = repos.strategy
        self.car_repo = repos.car
        self.track_repo = repos.track
        self.class_repo = repos.classes
        self.fuel_repo = repos.fuel
        self.stratservice = StrategyService(repos)

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
            ft.Row([
                ft.Column([
                        self.strategy_table
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO)
            ],
            expand=True)
        ])

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
            value="" if strategy is None or strategy.tire_limit is None else str(strategy.tire_limit)
        )

        self.multiplier = ft.TextField(
            label="Fuel Usage Multiplier",
            value="1" if strategy is None else str(strategy.usage_multiplier)
        )

        self.fuel_capacity = ft.TextField(
            label="Fuel Capacity Override",
            value = "" if strategy is None or strategy.fuel_capacity_override is None else str(strategy.fuel_capacity_override)
        )

        self.ve_capacity = ft.TextField(
            label="VE Capacity Override",
            value = "" if strategy is None or strategy.ve_capacity_override is None else str(strategy.ve_capacity_override)
        )

        self.laptime_override = ft.TextField(
            label="Laptime Override (s)",
            value = "" if strategy is None or strategy.laptime_override is None else str(strategy.laptime_override)
        )

        self.laps_override = ft.TextField(
            label="Laps Override",
            value = "" if strategy is None or strategy.laps_override is None else str(strategy.laps_override)
        )

        self.calculate_button = ft.Button(content="Calculate", on_click=self.calculate_pressed)
        self.save_button = ft.Button(content="Save", on_click=self.save_pressed)
        self.delete_button = ft.Button(content="Delete")

        self.load_tracks()
        self.load_cars()

        if self.current_strategy is not None:
            self.track_dropdown.value = str(self.current_strategy.track_id)
            self.car_dropdown.value = str(self.current_strategy.car_id)

        self.plan_presets = ft.Row(
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        self.details = ft.Column(expand=1, spacing=20)

        self.bottomside=ft.Row([
                self.details,
                ft.VerticalDivider(),
                ft.Column([
                    ft.Text("Plan Presets",size=20,weight=ft.FontWeight.BOLD),
                    self.plan_presets,
                    # ft.Divider()
                    # self.plan_builts
                    ],
                    expand=5)
                ],
                expand=True)
                


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
                    self.car_dropdown,
                    self.tire_limit
                ]),
                ft.Column([
                    self.multiplier,
                    self.fuel_capacity,
                    self.ve_capacity
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

            ft.Divider(),

            self.bottomside
        ])

        if strategy is not None:
            self.calculate_pressed()

    def show_plan(self, plan):
        pass

    def create_plan_card(self, plan: RacePlan) -> ft.Card:
        return ft.Card(
            content=ft.Container(
                padding=15,
                width=250,
                on_click=lambda e: self.show_plan(plan),
                content=ft.Column([
                    ft.Text(plan.name,
                            size=20,
                            weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            ft.Text(f"{len(plan.stints)} Stints"),
                            ft.Text(f"{plan.pit_stops} Pit Stops")
                ])
            )
        )

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

    def checks(self):
        if self.strategy_name.value == "":
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"No Name Found"),
                title_padding = ft.Padding.all(25),
                content=ft.Text("Enter a strategy name")
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return False
        try:
            trackid = int(self.track_dropdown.value)
        except:
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"No Track Found"),
                title_padding = ft.Padding.all(25),
                content=ft.Text("No track selected")
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return False
        
        try:
            carid = int(self.car_dropdown.value)
        except:
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"No Car Found"),
                title_padding = ft.Padding.all(25),
                content=ft.Text("No car selected")
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return False
        
        if not self.fuel_repo.exists(trackid, carid):
            track = self.track_repo.get_by_id(trackid)
            trackstr = f"{track.name}" if track.layout is None else f"{track.name} ({track.layout})"
            car = self.car_repo.get_by_id(carid)
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"No Fuel Usage Found"),
                title_padding = ft.Padding.all(25),
                content=ft.Column([
                    ft.Text(f"No fuel usage found for {car.name} on {trackstr}"),
                    ft.Text("Please add the fuel usage first, before calculating the strategy")
                ],
                expand=False)
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return False

        try:
            self.parse_racetime(self.race_minutes.value)
        except:
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"No Race Length Found"),
                title_padding = ft.Padding.all(25),
                content=ft.Text("No race length selected")
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return False
        try:
            self.parse_racetime(self.qual_minutes.value)
        except:
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"No Qualifying Length Found"),
                title_padding = ft.Padding.all(25),
                content=ft.Text("No qualifying length selected")
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return False
        try:
            int(self.multiplier.value)
        except:
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"No Valid Multipliet Found"),
                title_padding = ft.Padding.all(25),
                content=ft.Text("No valid fuel multiplier selected. This value must be integer.")
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return False
        
        return True

    def calculate_pressed(self, e=None):
        
        if not self.checks():
            return
        trackid = int(self.track_dropdown.value)
        carid = int(self.car_dropdown.value)

        if self.current_strategy is not None:
            id=self.current_strategy.id
        else:
            id=None
        try:
            strategy=Strategy(
                id=id,
                name = self.strategy_name.value,
                track_id = trackid,
                car_id = carid,
                race_minutes = self.parse_racetime(self.race_minutes.value),
                qual_minutes = self.parse_racetime(self.qual_minutes.value),
                laptime_override = self.parse_laptime(self.laptime_override.value),
                laps_override = self.parse_int(self.laps_override.value),
                usage_multiplier = int(self.multiplier.value),
                fuel_capacity_override = self.parse_int(self.fuel_capacity.value),
                ve_capacity_override = self.parse_int(self.ve_capacity.value),
                tire_limit = self.parse_int(self.tire_limit.value)
            )
        except Exception as ex:
            print(f"Strategy making failed: {ex}")
            return
        self.current_strategy=strategy
        result = self.stratservice.calculate(self.current_strategy)
        self.plan_presets.controls=[]
        for plan in result.raceplan_presets:
            self.plan_presets.controls.append(self.create_plan_card(plan))

        details=[]
        details.append(ft.Text("Laptimes",size=20,weight=ft.FontWeight.BOLD))
        #Reference Lap
        #PBs
        details.append(ft.Divider())
        details.append(ft.Text("Qualifying",size=20,weight=ft.FontWeight.BOLD))
        details.append(ft.Text(f"{result.quali_plan.laps} Laps"))
        details.append(ft.Text(f"Fuel Usage: {result.quali_plan.fuel_usage}L per lap"))
        details.append(ft.Text(f"Fuel Needed: {result.quali_plan.fuel_needed}L"))
        if result.quali_plan.fuel_ratio is not None:
            details.append(ft.Text(f"Fuel Ratio: {result.quali_plan.fuel_ratio} with 100% VE"))
        details.append(ft.Divider())
        details.append(ft.Text("Race",size=20,weight=ft.FontWeight.BOLD))
        details.append(ft.Text(f"{result.race_laps} Laps"))
        self.details.controls=details
        
        self.update()

    def save_pressed(self, e):
        if not self.checks():
            return
        trackid = int(self.track_dropdown.value)
        carid = int(self.car_dropdown.value)

        if self.current_strategy is not None:
            id=self.current_strategy.id
        else:
            id=None
        try:
            strategy=Strategy(
                id=id,
                name = self.strategy_name.value,
                track_id = trackid,
                car_id = carid,
                race_minutes = self.parse_racetime(self.race_minutes.value),
                qual_minutes = self.parse_racetime(self.qual_minutes.value),
                laptime_override = self.parse_laptime(self.laptime_override.value),
                laps_override = self.parse_int(self.laps_override.value),
                usage_multiplier = int(self.multiplier.value),
                fuel_capacity_override = self.parse_int(self.fuel_capacity.value),
                ve_capacity_override = self.parse_int(self.ve_capacity.value),
                tire_limit = self.parse_int(self.tire_limit.value)
            )
        except Exception as ex:
            print(f"Strategy making failed: {ex}")
            return
        if id is not None:
            self.strat_repo.update(strategy)
        else:
            self.strat_repo.add(strategy)

        self.current_strategy=strategy
        dialog = ft.AlertDialog(
            modal=False,
            alignment=ft.Alignment.CENTER,
            title=ft.Text(f"Saving Succesful"),
            title_padding = ft.Padding.all(25),
            content=ft.Text(f"Strategy was saved as {self.strategy_name.value}")
        )
        self.page.show_dialog(dialog)
        self.page.update()
        return

    def parse_laptime(self, time: str) -> float | None:
        if time is None or time.strip() == "":
            return None
        time=time.strip()
        if ":" in time:
            minutes = int(time.split(":")[0])
            seconds = float(time.split(":")[1])
            time=60*minutes+seconds
        return float(time)

    def parse_racetime(self, time: str) -> int:
        if ":" in time:
            hours=int(time.split(":")[0])
            minutes=int(time.split(":")[1])
            time = 60*hours+minutes
        return int(time)

    def parse_int(self, value: str) -> int | None:
        if value is None or value.strip() == "":
            return None
        return int(value)

    
