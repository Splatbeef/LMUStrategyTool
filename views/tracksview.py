import flet as ft
from models import Track
from repositories.track_repository import TrackRepository


class TracksView(ft.Container):
    def __init__(self, track_repo: TrackRepository):
        self.track_repo = track_repo

        self.name_field = ft.TextField(label="Track Name")
        self.layout_field = ft.TextField(label="Layout")

        self.tracks_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Track")),
                ft.DataColumn(ft.Text("Layout")),
            ],
            rows=[]
        )

        self.add_button = ft.Button(content="Add Track", on_click=self.add_track)
        self.edit_button = ft.Button(content="Save Changes", on_click=self.save_track, disabled=True)
        self.clear_button = ft.Button(content="Clear Fields", on_click=self.clear_form)
        self.delete_button = ft.Button(content="Delete", on_click=self.delete_track, disabled=True)

        self.filters()
        self.refresh_table()

        super().__init__(
            expand=True,
            content=ft.Column(
                [
                    ft.Text(
                        "Tracks",
                        size=28,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Row([
                        ft.Column([
                                self.filter_row,
                                self.tracks_table
                            ],
                            expand=True,
                            scroll=ft.ScrollMode.AUTO),
                        # ft.Column([
                        #     self.name_field,
                        #     self.layout_field,

                        #     ft.Divider(),

                        #     ft.Column([
                        #         self.add_button,
                        #         self.edit_button,
                        #         self.clear_button,
                        #         self.delete_button
                        #     ]),
                        # ])
                    ],
                    expand=True)                    
                ]
            )
        )

    def filters(self):
        self.trackfilter = ft.Dropdown(label="Track", on_select=self.refresh_table, editable=True, enable_filter=True)
        tracks = self.track_repo.get_all()
        tracknames = sorted(list(set([t.name for t in tracks])))
        self.trackfilter.options = [
            ft.dropdown.Option(
                key = t,
                text=t
            )
            for t in tracknames
        ]

        self.clear_filter_button = ft.Button(content="Clear Filtes", on_click=self.clear_filters)

        self.filter_row = ft.Row([
            self.clear_filter_button,
            self.trackfilter
        ],
        expand=True)

    def clear_filters(self):
        self.trackfilter.value=None

        self.refresh_table()

    def refresh_table(self):
        if not self.trackfilter.value:
            tracks = self.track_repo.get_all()
        else:
            tracks = self.track_repo.get_by_name(self.trackfilter.value)

        self.tracks_table.rows.clear()

        for track in tracks:
            self.tracks_table.rows.append(
                ft.DataRow(
                    on_select_change=lambda e, track=track: self.edit_track(track),
                    cells=[
                        ft.DataCell(ft.Text(track.name)),
                        ft.DataCell(ft.Text(track.layout)),
                    ]
                )
            )

    def add_track(self):

        track=Track(
            id=None,
            name=self.name_field.value,
            layout=self.layout_field.value
        )

        self.track_repo.add(track)

        self.clear_form()

        self.refresh_table()
        self.update()

    def edit_track(self, track: Track):

        self.selected_track_id = track.id

        self.name_field.value = track.name

        self.layout_field.value = track.layout

        self.edit_button.disabled = False
        self.delete_button.disabled = False

        self.update()

    def save_track(self, e):

        if self.selected_track_id is None:
            return

        track = Track(
            id=self.selected_track_id,
            name=self.name_field.value,
            layout=self.layout_field.value
        )

        self.track_repo.update(track)

        self.clear_form()

        self.refresh_table()

        self.update()

    def clear_form(self):

        self.selected_track_id = None

        self.name_field.value = ""
        self.layout_field.value = ""

        self.edit_button.disabled = True

        self.update()

    def delete_track(self, e):
        if self.selected_track_id is None:
            return

        self.track_repo.delete(self.selected_track_id)

        self.clear_form()
        self.refresh_table()
        self.update()