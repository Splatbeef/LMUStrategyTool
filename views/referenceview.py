import flet as ft
import datetime as dt

from models import Car, Track, ReferenceTime
from Repositories.referencetime_repository import ReferenceTimeRepository
from Repositories.car_repository import CarRepository
from Repositories.carclass_repository import CarClassRepository
from Repositories.track_repository import TrackRepository
from services.referenceservice import *

class ReferenceView(ft.Container):
    def __init__(self, reference_repo: ReferenceTimeRepository, track_repo: TrackRepository, class_repo: CarClassRepository, car_repo: CarRepository):
        self.class_repo = class_repo
        self.track_repo = track_repo
        self.reference_repo = reference_repo
        self.referenceservice = ReferenceService(track_repo, car_repo, reference_repo)

        self.sync_button = ft.Button(content="Sync Laptimes", on_click=self.sync_clicked)
        self.clear_button = ft.Button(content="Clear Laptimes", on_click=self.clear_clicked)

        self.times_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Track")),
                ft.DataColumn(ft.Text("Class")),
                ft.DataColumn(ft.Text("Laptime")),
                ft.DataColumn(ft.Text("Date Updated"))
            ],
            rows=[]
        )

        self.refresh_table()

        super().__init__(
            expand=True,
            content=ft.Column([
                ft.Text(
                    "Reference Times",
                    size=28,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Row([
                    self.sync_button,
                    self.clear_button
                ]),
                ft.Divider(),
                self.times_table
            ])
        )

    def sync_clicked(self, e):
        self.referenceservice.sync()
        self.refresh_table()
        self.update()

    def clear_clicked(self, e):
        self.reference_repo.clear()
        self.refresh_table()
        self.update()



    def refresh_table(self):
        times = self.reference_repo.get_all()

        self.times_table.rows.clear()

        for t in times:
            carclass = self.class_repo.get_by_id(t.carclass_id)
            track = self.track_repo.get_by_id(t.track_id)
            if len(track.layout) > 0:
                trackstr = f"{track.name} ({track.layout})"
            else:
                trackstr = track.name
            laptime = t.laptime
            laptimestr = self.referenceservice.text_from_laptime(laptime)

            self.times_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(trackstr)),
                        ft.DataCell(ft.Text(carclass.name)),
                        ft.DataCell(ft.Text(laptimestr)),
                        ft.DataCell(ft.Text(str(t.date_set)))
                    ]
                )
            )