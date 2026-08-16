import flet as ft

from models import Car, FuelUsage, Track, CarClass
from Repositories.repositories import *
from Repositories.car_repository import CarRepository
from Repositories.carclass_repository import CarClassRepository
from Repositories.fuel_repository import FuelRepository
from Repositories.track_repository import TrackRepository

class FuelUsageView(ft.Container):
    def __init__(self, repos: Repositories):
        self.car_repo = repos.car
        self.class_repo = repos.classes
        self.fuel_repo = repos.fuel
        self.track_repo = repos.track

        self.name_selected = ft.Dropdown(label="Select Car")
        self.track_selected = ft.Dropdown(label="Select Track")
        self.fuel_field = ft.TextField(label="Fuel Usage")
        self.ve_field = ft.TextField(label="VE Usage")

        self.usage_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Car")),
                ft.DataColumn(ft.Text("Track")),
                ft.DataColumn(ft.Text("Fuel Usage")),
                ft.DataColumn(ft.Text("VE Usage"))
            ],
            rows=[]
        )

        self.add_button = ft.Button(content="Add Usage Data", on_click=self.add_usage)
        self.edit_button = ft.Button(content="Save Changes", on_click=self.save_usage, disabled=True)
        self.clear_button = ft.Button(content="Clear Fields", on_click=self.clear_form)
        self.delete_button = ft.Button(content="Delete Usage Data", on_click=self.delete_usage, disabled=True)

        self.load_cars()
        self.load_tracks()
        self.filters()
        self.refresh_table()

        super().__init__(
            expand=True,
            content=ft.Column(
                [
                    ft.Text(
                        "Fuel/Energy Usage",
                        size=28,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Row([
                        ft.Column([
                            self.filter_row,
                            self.usage_table
                        ],
                        expand=True,
                        scroll=ft.ScrollMode.AUTO),
                        ft.Column([
                            self.name_selected,
                            self.track_selected,
                            self.fuel_field,
                            self.ve_field,

                            ft.Divider(),

                            ft.Column([
                                self.add_button,
                                self.edit_button,
                                self.clear_button,
                                self.delete_button
                            ]),
                        ])
                    ],
                    expand=True)                    
                ]
            )
        )

    def load_cars(self):
        self.name_selected.options = []

        cars = sorted(
            self.car_repo.get_all(),
            key=lambda c: (
                self.class_repo.get_by_id(c.carclass_id).name,
                c.name.lower()
            )
        )
        
        for c in cars:
            carclass = self.class_repo.get_by_id(c.carclass_id)
            self.name_selected.options.append(
            ft.dropdown.Option(
                key=str(c.id),
                text=f"{c.name} ({carclass.name})"
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
            self.track_selected.options.append(
                ft.dropdown.Option(
                    key=str(c.id),
                    text=trackstr
                ) 
            )

    def filters(self):

        self.trackfilter = ft.Dropdown(label="Track", on_select=self.refresh_table, editable=True, enable_search=True)
        tracks = self.track_repo.get_all()
        for c in tracks:
            if len(c.layout)>0:
                trackstr=f"{c.name} ({c.layout})"
            else:
                trackstr=c.name
            self.trackfilter.options.append(
                ft.dropdown.Option(
                    key=str(c.id),
                    text=trackstr
                ) 
            )

        self.carfilter = ft.Dropdown(label="Car", on_select=self.refresh_table, editable=True, enable_search=True)
        cars = self.car_repo.get_all()
        self.carfilter.options = [
            ft.dropdown.Option(
                key=str(c.id),
                text=c.name
            ) 
            for c in cars
        ]

        self.clear_filter_button = ft.Button(content="Clear Filters", on_click=self.clear_filters)

        self.filter_row = ft.Row([
            self.clear_filter_button,
            self.carfilter,
            self.trackfilter
        ],
        expand=True)

    def clear_filters(self):
        self.trackfilter.value=None
        self.carfilter.value=None
        self.refresh_table()

    def refresh_table(self):
        if not self.trackfilter.value and not self.carfilter.value:
            usages = self.fuel_repo.get_all()
        elif not self.trackfilter.value:
            usages = self.fuel_repo.get_by_car(int(self.carfilter.value))
        elif not self.carfilter.value:
            usages = self.fuel_repo.get_by_track(int(self.trackfilter.value))
        else:
            usages = [self.fuel_repo.get_by_track_car(int(self.trackfilter.value), int(self.carfilter.value))]

        self.usage_table.rows.clear()
        
        for u in usages:
            car = self.car_repo.get_by_id(u.car_id)
            track = self.track_repo.get_by_id(u.track_id)
            carclass = self.class_repo.get_by_id(car.carclass_id)
            if track is None:
                trackstr = ""
            elif len(track.layout) > 1:
                trackstr = f"{track.name} ({track.layout})"
            else:
                trackstr = track.name

            self.usage_table.rows.append(
                ft.DataRow(
                    on_select_change=lambda e, u=u: self.edit_usage(u),
                    cells=[
                        ft.DataCell(ft.Text(f"{car.name} ({carclass.name})")),
                        ft.DataCell(ft.Text(trackstr)),
                        ft.DataCell(ft.Text(str(u.fuel_usage))),
                        ft.DataCell(ft.Text(str(u.ve_usage) if u.ve_usage is not None else "No VE"))
                    ]
                )
            )

    def add_usage(self):

        car_id = int(self.name_selected.value)
        car = self.car_repo.get_by_id(car_id)
        track_id=int(self.track_selected.value)

        try:
            fuel_usage = float(self.fuel_field.value)
        except ValueError:
            return
        if car.ve:
            try:
                ve_usage = float(self.ve_field.value)
            except ValueError:
                return

        usage = FuelUsage(
            id=None,
            car_id=car_id,
            track_id=track_id,
            fuel_usage= fuel_usage,
            ve_usage = ve_usage if car.ve else None
        )

        self.fuel_repo.add(usage)

        self.clear_form()

        self.refresh_table()
        self.update()

    def edit_usage(self, usage: FuelUsage):

        self.selected_usage_id = usage.id
        self.car = self.car_repo.get_by_id(usage.car_id)
        self.track = self.track_repo.get_by_id(usage.track_id)

        self.name_selected.value = str(self.car.id)
        self.track_selected.value = str(self.track.id)

        self.fuel_field.value=usage.fuel_usage
        self.ve_field.value=usage.ve_usage if usage.ve_usage is not None else "No VE"

        self.edit_button.disabled = False
        self.delete_button.disabled = False

        self.update()

    def save_usage(self, e):

        if self.selected_usage_id is None:
            return

        car = self.car_repo.get_by_id(int(self.name_selected.value))
        try:
            fuel_usage = float(self.fuel_field.value)
        except ValueError:
            return
        if car.ve:
            try:
                ve_usage = float(self.ve_field.value)
            except ValueError:
                return
            
        usage = FuelUsage(
            id=self.selected_usage_id,
            car_id = int(self.name_selected.value),
            track_id = int(self.track_selected.value),
            fuel_usage = fuel_usage,
            ve_usage = ve_usage if car.ve else None
        )

        self.fuel_repo.update(usage)

        self.clear_form()

        self.refresh_table()

        self.update()

    def clear_form(self):

        self.selected_usage_id = None

        self.name_selected.value = ""
        self.track_selected.value = ""
        self.fuel_field.value = ""
        self.ve_field.value = ""

        self.edit_button.disabled = True
        self.delete_button.disabled=True

    def delete_usage(self, e):
        if self.selected_usage_id is None:
            return

        self.fuel_repo.delete(self.selected_usage_id)

        self.clear_form()
        self.refresh_table()
        self.update()