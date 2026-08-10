import flet as ft

class StrategyView(ft.Container):
    def __init__(self):

        self.track_dropdown = ft.Dropdown(label="Track")

        self.car_dropdown = ft.Dropdown(label="Car")

        self.race_minutes = ft.TextField(label="Race Minutes", value="60")

        self.laptime_override = ft.TextField(label="Laptime Override")

        self.laps_override = ft.TextField(label="Laps Override")

        self.multiplier = ft.TextField(label="Fuel Usage Multiplier", value="1")

        self.fuel_capacity = ft.TextField(label="Fuel Capacity Limit")

        self.ve_capacity = ft.TextField(label="VE Capacity Limit")

        self.calculate_button = ft.Button(content="Calculate")

        self.results=ft.Column()

        super().__init__(
            expand=True,
            content=ft.Column(
                [
                    ft.Text("Strategy Calculator", size=28, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    self.track_dropdown,
                                    self.car_dropdown,
                                    self.race_minutes,
                                ]
                            ),
                            ft.Column(
                                [
                                    self.multiplier,
                                    self.fuel_capacity,
                                    self.ve_capacity
                                ]
                            ),
                            ft.Column(
                                [
                                    self.laptime_override,
                                    self.laps_override,
                                ]
                            )
                        ]
                    ),                   
                    self.calculate_button,
                    ft.Divider(),
                    self.results
                ]
            )
        )