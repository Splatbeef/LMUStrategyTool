import flet as ft
import datetime as dt

from models import Car, Track, ReferenceTime
from Repositories.repositories import *
from services.referenceservice import *

class ReferenceView(ft.Container):
    def __init__(self, repos: Repositories):
        self.class_repo = repos.classes
        self.car_repo = repos.car
        self.track_repo = repos.track
        self.reference_repo = repos.reference
        self.referenceservice = ReferenceService(repos)

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

        self.filters()
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
                ft.Row([
                    ft.Column([
                        self.filter_row,
                        self.times_table
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO)
                ],
                expand=True)
            ])
        )

    def sync_clicked(self, e):
        self.dialog = ft.AlertDialog(
            modal=False,
            alignment=ft.Alignment.CENTER,
            title=ft.Text(f"Syncing"),
            title_padding = ft.Padding.all(25),
            content=ft.Text("Sync successful!")
        )
    
        missing = self.referenceservice.sync()
        if missing["tracks"]:
            self.show_track_alias_dialog(missing["tracks"])
        if missing["cars"]:
            self.show_car_alias_dialog(missing["cars"])
            
        self.refresh_table()
        self.page.show_dialog(self.dialog)
        self.page.update()

    def close_sync_dialog(self, e):
        self.dialog.open = False
        self.page.update()

    def clear_clicked(self, e):
        self.reference_repo.clear()
        self.refresh_table()
        self.update()

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

        self.classfilter = ft.Dropdown(label="Class", on_select=self.refresh_table, editable=True, enable_search=True)
        classes = self.class_repo.get_all()
        self.classfilter.options = [
            ft.dropdown.Option(
                key=str(c.id),
                text=c.name
            ) 
            for c in classes
        ]

        self.clear_filter_button = ft.Button(content="Clear Filters", on_click=self.clear_filters)

        self.filter_row = ft.Row([
            self.clear_filter_button,
            self.trackfilter,
            self.classfilter
        ],
        expand=True)

    def clear_filters(self):
        self.trackfilter.value=None
        self.classfilter.value=None
        self.refresh_table()

    def refresh_table(self):
        if not self.trackfilter.value and not self.classfilter.value:
            times = self.reference_repo.get_all()
        elif not self.trackfilter.value:
            class_id = int(self.classfilter.value)
            times = self.reference_repo.get_by_class(class_id)
        elif not self.classfilter.value:
            track_id = int(self.trackfilter.value)
            times = self.reference_repo.get_by_track(track_id)
        else:
            track_id = int(self.trackfilter.value)
            class_id = int(self.classfilter.value)
            times = self.reference_repo.get_by_track_class(track_id, class_id)

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

    def show_track_alias_dialog(
    self,
    missing_tracks: list,
    ):
        track_alias = missing_tracks[0]

        track_dropdown = ft.Dropdown(
            label="Select Existing Track",
            options=[])
        for t in self.track_repo.get_all():
            if t.layout != "":
                track_dropdown.options.append(ft.dropdown.Option(
                    key=str(t.id),
                    text=f"{t.name} ({t.layout})"
                ))
            else:
                track_dropdown.options.append(ft.dropdown.Option(
                    key=str(t.id),
                    text=f"{t.name}"
                ))

        def save_alias(e):
            if not track_dropdown.value:
                return
            track = self.track_repo.get_by_id(int(track_dropdown.value))
            self.referenceservice.save_track_alias(track_alias, track.name, track.layout)
            dialog.open=False
            self.page.update()
            show_next_track_alias()

        save_button = ft.Button(content="Save Alias", on_click=save_alias)
        
        track_text = ft.TextField(label="Track name")
        layout_text = ft.TextField(label="Layout")

        def add_track(e):
            if not track_text.value:
                return
            name = track_text.value
            layout = layout_text.value
            if not self.track_repo.exists(name, layout):
                self.track_repo.add(Track(
                    id = None,
                    name = name,
                    layout = layout
                ))
            self.referenceservice.save_track_alias(track_alias, name, layout)
            dialog.open=False
            self.page.update()
            show_next_track_alias()
            
        add_button = ft.Button(content="Add Track", on_click=add_track)

        def show_next_track_alias():
            remaining=missing_tracks[1:]

            if remaining:
                self.show_track_alias_dialog(remaining)
            else:
                self.refresh_table()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add Track Alias"),
            content=ft.Column([
                ft.Text(f"Missing track for alias: {track_alias}"),
                ft.Divider(),
                ft.Text("Select Existing Track"),
                track_dropdown,
                save_button,
                ft.Divider(),
                ft.Text("Add New Track"),
                ft.Row([
                    track_text,
                    layout_text,
            ]),
                add_button
            ])
        )

        self.page.show_dialog(dialog)
        self.page.update()

    def show_car_alias_dialog(
        self,
        missing_cars: list,
        ):
            car_alias = missing_cars[0]
    
            car_dropdown = ft.Dropdown(
                label="Select Existing Car",
                options=[])
            for c in sorted(self.car_repo.get_all(), key=lambda car: car.name.lower()):
                car_dropdown.options.append(ft.dropdown.Option(
                    key=str(c.id),
                    text=f"{c.name}"
                ))
    
            def save_alias(e):
                if not car_dropdown.value:
                    return
                car = self.car_repo.get_by_id(int(car_dropdown.value))
                self.referenceservice.save_car_alias(car_alias, car.name)
                dialog.open=False
                self.page.update()
                show_next_car_alias()
            save_button = ft.Button(content="Save Alias", on_click=save_alias)
            
            car_text = ft.TextField(label="Car name")
    
            def add_car(e):
                if not car_text.value:
                    return
                name = car_text.value
                if not self.car_repo.exists(name):
                    self.car_repo.add(Car(
                        id = None,
                        name = name
                    ))
                self.referenceservice.save_car_alias(car_alias, name)
                dialog.open=False
                self.page.update()
                show_next_car_alias()
                
            add_button = ft.Button(content="Add Car", on_click=add_car)
    
            def show_next_car_alias():
                remaining = missing_cars[1:]

                if remaining:
                    self.show_car_alias_dialog(remaining)
                else:
                    self.refresh_table()
    
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Add Car Alias"),
                content=ft.Column([
                    ft.Text(f"Missing car for alias: {car_alias}"),
                    ft.Divider(),
                    ft.Text("Select Existing Car"),
                    car_dropdown,
                    save_button,
                    ft.Divider(),
                    ft.Text("Add New Car"),
                    car_text,
                    add_button
                ])
            )
            self.page.show_dialog(dialog)
            self.page.update()


