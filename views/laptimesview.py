import flet as ft
import datetime as dt
import math
from Repositories.repositories import *
from models import *
from services.strategy_service import *
from services.referenceservice import *
from controls.laptime_perc import *

class LapTimesView(ft.Container):
    def __init__(self, repos: Repositories):
        self.repo_times = repos.laptime
        self.repo_reference = repos.reference
        self.repo_car = repos.car
        self.repo_class = repos.classes
        self.repo_track = repos.track

        self.input_column = self.make_input_fields()
        self.selected_laptime = None

        self.laptimes_table=ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Car")),
                ft.DataColumn(ft.Text("Class")),
                ft.DataColumn(ft.Text("Track")),
                ft.DataColumn(ft.Text("Session")),
                ft.DataColumn(ft.Text("Laptime"))
            ]
        )
        self.refresh_table()

        super().__init__(
            expand=True,
            content=ft.Column([
                ft.Text(
                    "Personal Best Laptimes",
                    size=28,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Row([
                    ft.Column(
                        controls=[self.laptimes_table],
                        expand=True,
                        scroll = ft.ScrollMode.AUTO
                    ),
                    ft.VerticalDivider(),
                    self.input_column
                ],
                expand=True)
            ])
        )

    def make_input_fields(self) -> ft.Column:
        self.car_field = ft.Dropdown(label="Car")
        self.track_field = ft.Dropdown(label="Track")
        self.time_field = ft.TextField(label="Laptime (00:00.000)")
        self.session_field = ft.Dropdown(label="Session", options=[
            ft.dropdown.Option("Race"),
            ft.dropdown.Option("Qualifying")
        ])
        #Check settings for practice laptime option!

        self.save_button = ft.Button(content="Save", on_click=self.save_laptime)
        self.delete_button = ft.Button(content="Delete", on_click=self.delete_laptime)
        self.clear_button = ft.Button(content="Clear", on_click=self.clear_form)

        self.load_cars()
        self.load_tracks()

        col = ft.Column([
            self.car_field,
            self.track_field,
            self.time_field,
            self.session_field,
            ft.Row([
                self.save_button,
                self.delete_button,
                self.clear_button
            ])
        ])

        return col

    def load_cars(self):
        self.car_field.options = []

        cars = sorted(
            self.repo_car.get_all(),
            key=lambda c: (
                c.name.lower()
            )
        )
        
        for c in cars:
            carclass = self.repo_class.get_by_id(c.carclass_id)
            self.car_field.options.append(
            ft.dropdown.Option(
                key=str(c.id),
                text=f"{c.name} ({carclass.name})"
            ) )

    def load_tracks(self):
        tracks = sorted(
            self.repo_track.get_all(),
            key=lambda t: (t.name.lower(), t.layout.lower())
        )
        for c in tracks:
            if len(c.layout)>0:
                trackstr=f"{c.name} ({c.layout})"
            else:
                trackstr=c.name
            self.track_field.options.append(
                ft.dropdown.Option(
                    key=str(c.id),
                    text=trackstr
                ) 
            )

    def refresh_table(self):
        laptimes = self.repo_times.get_all()
        self.laptimes_table.rows.clear()

        for laptime in laptimes:
            car = self.repo_car.get_by_id(laptime.car_id)
            carclass = self.repo_class.get_by_id(car.carclass_id)
            track = self.repo_track.get_by_id(laptime.track_id)
            trackstr = track.name if track.layout == "" else f"{track.name} ({track.layout})"
            reference = self.repo_reference.get_best_reference(laptime.track_id, car.carclass_id)
            if reference is None:
                dialog = ft.AlertDialog(
                    modal=False,
                    alignment=ft.Alignment.CENTER,
                    title=ft.Text(f"Missing Reference"),
                    title_padding = ft.Padding.all(25),
                    content=ft.Text(f"Missing reference for {carclass.name} on {trackstr}. Please update references")
                )
                self.page.show_dialog(dialog)
                self.page.update()
                return
            perc = LapTimePerc(laptime.laptime, reference.laptime)
            laptimerow = ft.Row(
                [
                    ft.Text(self.text_from_laptime(laptime.laptime)),
                    perc
                ]
            )

            self.laptimes_table.rows.append(
                ft.DataRow(
                    on_select_change=lambda e, laptime=laptime: self.select_laptime(laptime),
                    cells=[
                        ft.DataCell(ft.Text(car.name)),
                        ft.DataCell(ft.Text(carclass.name)),
                        ft.DataCell(ft.Text(trackstr)),
                        ft.DataCell(ft.Text(laptime.sessiontype)),
                        ft.DataCell(laptimerow)
                    ]
                )
            )

    def save_laptime(self, e=None):
        if not self.checks():
            return
        if self.selected_laptime is not None:
            id = self.selected_laptime.id
        else:
            id=None
        car = self.repo_car.get_by_id(int(self.car_field.value))
        track = self.repo_track.get_by_id(int(self.track_field.value))
        time = self.parse_laptime(self.time_field.value)
        session = self.session_field.value
        today = dt.date.today()

        laptime = LapTime(
            id=id,
            track_id = track.id,
            car_id = car.id,
            laptime=time,
            date_set = today,
            sessiontype = session
        )

        if self.selected_laptime is not None:
            self.repo_times.update(laptime)
        else:
            self.repo_times.add(laptime)

        self.clear_form()
        self.refresh_table()
        self.update()

    def delete_laptime(self, e=None):
        if self.selected_laptime is not None:
            self.repo_times.delete(self.selected_laptime.id)

            self.clear_form()
            self.refresh_table()
            self.update()

    def checks(self):
        try:
            self.repo_car.get_by_id(int(self.car_field.value))
        except:
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"No Car Selected"),
                title_padding = ft.Padding.all(25),
                content=ft.Text("Please select a car")
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return False
        try:
            self.repo_track.get_by_id(int(self.track_field.value))
        except:
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"No Track Selected"),
                title_padding = ft.Padding.all(25),
                content=ft.Text("Please select a track")
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return False
        if self.parse_laptime(self.time_field.value) is None:
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"No Valid Laptime"),
                title_padding = ft.Padding.all(25),
                content=ft.Text("Please input a valid laptime as 00:00.000 or 00.000")
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return False
        if not self.session_field.value:
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"No Session Type Selected"),
                title_padding = ft.Padding.all(25),
                content=ft.Text("Please select a session type")
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return False

        return True

    def parse_laptime(self, time: str) -> float | None:
        if time is None or time.strip() == "":
            return None
        time=time.strip()
        if ":" in time:
            minutes = int(time.split(":")[0])
            seconds = float(time.split(":")[1])
            time=60*minutes+seconds
        try:
            return float(time)
        except:
            return None

    def text_from_laptime(self, laptime):
        if laptime < 60:
            return f"{laptime:.3f}"
        minutes = math.floor(laptime/60)
        seconds = laptime % 60
        return f"{minutes}:{seconds:06.3f}" 

    def select_laptime(self, laptime: LapTime):
        self.selected_laptime=laptime
        self.car_field.value = str(laptime.car_id)
        self.track_field.value= str(laptime.track_id)
        self.time_field.value = self.text_from_laptime(laptime.laptime)
        self.session_field.value = laptime.sessiontype
        self.update()

    def clear_form(self, e=None):
        self.car_field.value=""
        self.track_field.value=""
        self.time_field.value=""
        self.session_field.value=""
        self.selected_laptime=None
        self.update()