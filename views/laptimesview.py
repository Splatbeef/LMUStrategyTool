import flet as ft
import datetime as dt
import math
from repositories.repositories import *
from models import *
from services.strategy_service import *
from services.reference_service import *
from controls.laptime_perc import *

class LapTimesView(ft.Container):
    def __init__(self, repos: Repositories):
        self.repo_times = repos.laptime
        self.repo_reference = repos.reference
        self.repo_car = repos.car
        self.repo_class = repos.classes
        self.repo_track = repos.track

        self.sessions = ["Qualifying", "Race"]
        setting = repos.settings.get_by_key("Laptime Sessiontypes")
        if setting.value_int==1:
            self.sessions.append("Practice")
        elif setting.value_int==2:
            self.sessions+=["Race Practice", "Qualifying Practice"]

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

        self.filters()
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
                        controls=[self.filter_row, self.laptimes_table],
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
        self.car_field = ft.Dropdown(label="Car", editable=True, enable_filter=True)
        self.track_field = ft.Dropdown(label="Track", editable=True, enable_filter=True)
        self.time_field = ft.TextField(label="Laptime (00:00.000)")
        self.session_field = ft.Dropdown(label="Session", options=[
            ft.dropdown.Option(s) for s in self.sessions
        ])
        #Check settings for practice laptime option!

        self.add_button = ft.Button(content="Add", on_click=self.add_laptime)
        self.save_button = ft.Button(content="Save", on_click=self.save_laptime, disabled=True)
        self.delete_button = ft.Button(content="Delete", on_click=self.delete_laptime, disabled=True)
        self.clear_button = ft.Button(content="Clear", on_click=self.clear_form)

        self.load_cars()
        self.load_tracks()

        col = ft.Column([
            self.car_field,
            self.track_field,
            self.time_field,
            self.session_field,
            ft.Row([
                self.add_button,
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

    def filters(self):
        self.trackfilter = ft.Dropdown(label="Track", on_select=self.refresh_table, editable=True, enable_filter=True)
        tracks = self.repo_track.get_all()
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

        self.carfilter = ft.Dropdown(label="Car", on_select=self.refresh_table, editable=True, enable_filter=True)
        cars = self.repo_car.get_all()
        self.carfilter.options = [
            ft.dropdown.Option(
                key=str(c.id),
                text=c.name
            ) 
            for c in cars
        ]

        # self.classfilter = ft.Dropdown(label="Class", on_select=self.refresh_table, editable=True, enable_search=True)
        # classes = self.class_repo.get_all()
        # self.classfilter.options = [
        #     ft.dropdown.Option(
        #         key=str(c.id),
        #         text=c.name
        #     ) 
        #     for c in classes
        # ]

        self.sessionfilter = ft.Dropdown(label="Session", on_select=self.refresh_table, editable=True, enable_search=True)
        self.sessionfilter.options = [
            ft.dropdown.Option(
                key=c,
                text=c
            ) 
            for c in self.sessions
        ]

        self.clear_filter_button = ft.Button(content="Clear Filters", on_click=self.clear_filters)

        self.filter_row = ft.Row([
            self.clear_filter_button,
            self.carfilter,
            self.trackfilter,
            self.sessionfilter
        ],
        expand=True)

    def clear_filters(self):
        self.trackfilter.value=None
        self.carfilter.value=None
        self.sessionfilter.value=None
        self.refresh_table()

    def refresh_table(self):
        if not self.trackfilter.value and not self.carfilter.value and not self.sessionfilter.value:
            laptimes = self.repo_times.get_all()
        elif not self.carfilter.value and not self.sessionfilter.value:
            laptimes = self.repo_times.get_by_track(self.trackfilter.value)
        elif not self.trackfilter.value and not self.sessionfilter.value:
            laptimes = self.repo_times.get_by_car(self.carfilter.value)
        elif not self.carfilter.value and not self.trackfilter.value:
            laptimes = self.repo_times.get_by_session(self.sessionfilter.value)
        elif not self.carfilter.value:
            laptimes = self.repo_times.get_by_track_session(self.trackfilter.value, self.sessionfilter.value)
        elif not self.trackfilter.value:
            laptimes = self.repo_times.get_by_car_session(self.carfilter.value, self.sessionfilter.value)
        elif not self.sessionfilter.value:
            laptimes = self.repo_times.get_by_track_car(self.trackfilter.value, self.carfilter.value)
        else:
            laptimes = [self.repo_times.get_by_track_car_session(self.trackfilter.value, self.carfilter.value, self.sessionfilter.value)]

        self.laptimes_table.rows.clear()

        for laptime in laptimes:
            car = self.repo_car.get_by_id(laptime.car_id)
            carclass = self.repo_class.get_by_id(car.carclass_id)
            track = self.repo_track.get_by_id(laptime.track_id)
            trackstr = track.name if track.layout == "" else f"{track.name} ({track.layout})"
            reference = self.repo_reference.get_best_reference(laptime.track_id, car.carclass_id)
            if reference is not None:
                perc = LapTimePerc(laptime.laptime, reference.laptime)
                laptimerow = ft.Row(
                    [
                        ft.Text(self.text_from_laptime(laptime.laptime)),
                        perc
                    ]
                )
            else:
                laptimerow = ft.Row(
                    [
                        ft.Text(self.text_from_laptime(laptime.laptime))
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
            return
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

        dialog = ft.AlertDialog(
            modal=False,
            alignment=ft.Alignment.CENTER,
            title=ft.Text(f"Saved Succesfully"),
            title_padding = ft.Padding.all(25),
            content=ft.Text("Laptime saved succesfully!")
        )

        self.repo_times.update(laptime)

        self.clear_form()
        self.refresh_table()
        self.update()
        self.page.show_dialog(dialog)
        self.page.update()

    def add_laptime(self, e=None):
        if not self.checks():
            return
        car = self.repo_car.get_by_id(int(self.car_field.value))
        track = self.repo_track.get_by_id(int(self.track_field.value))
        time = self.parse_laptime(self.time_field.value)
        session = self.session_field.value
        today = dt.date.today()

        laptime = LapTime(
            id=None,
            track_id = track.id,
            car_id = car.id,
            laptime=time,
            date_set = today,
            sessiontype = session
        )

        
        if self.repo_times.get_by_track_car_session(track.id, car.id, session):
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"Already Exists"),
                title_padding = ft.Padding.all(25),
                content=ft.Column([
                    ft.Text("Laptime for this car, track, and session already exists!"),
                    ft.Text("Please select that laptime and update it using 'Save'.")
                ],
                expand=False)
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return

        self.repo_times.add(laptime)

        dialog = ft.AlertDialog(
            modal=False,
            alignment=ft.Alignment.CENTER,
            title=ft.Text(f"Added Succesfully"),
            title_padding = ft.Padding.all(25),
            content=ft.Text("Laptime added succesfully!")
        )

        self.clear_form()
        self.refresh_table()
        self.update()
        self.page.show_dialog(dialog)
        self.page.update()

    def delete_laptime(self, e=None):
        if self.selected_laptime is not None:
            self.repo_times.delete(self.selected_laptime.id)

            self.clear_form()
            self.refresh_table()
            self.update()
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"Deleted Succesfully"),
                title_padding = ft.Padding.all(25),
                content=ft.Text("Laptime deleted succesfully!")
            )
            self.page.show_dialog(dialog)
            self.page.update()

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
        self.delete_button.disabled=False
        self.save_button.disabled=False
        self.update()

    def clear_form(self, e=None):
        self.car_field.value=""
        self.track_field.value=""
        self.time_field.value=""
        self.session_field.value=""
        self.selected_laptime=None
        self.save_button.disabled=True
        self.delete_button.disabled=True
        self.update()