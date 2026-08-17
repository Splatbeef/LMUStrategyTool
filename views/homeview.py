import flet as ft
import datetime as dt

from Repositories.repositories import *

class HomeView(ft.Container):
    def __init__(self, repos: Repositories):
        self.repo_car = repos.car
        self.repo_track = repos.track
        self.repo_settings = repos.settings
        self.repo_fuel = repos.fuel
        self.repo_laptimes = repos.laptime
        self.repo_strats = repos.strategy

        self.versionnumber = self.repo_settings.get_by_key("Version").value_str
        self.banner = ft.Row([
            #Add icon here
            ft.Text("LMU Strategy Tool", size=60, weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
            ft.Column([
                ft.Text(f"Version {self.versionnumber}", size=16),
                ft.Text(f"by Splatbeef", size=16)
            ],
            expand=False,
            )
        ])

        numcars = len(self.repo_car.get_all())
        tracks = self.repo_track.get_all()
        numlayouts = len(tracks)
        numtracks = len(sorted(list(set([t.name for t in tracks]))))
        numusages = len(self.repo_fuel.get_all())
        laptimes = self.repo_laptimes.get_all()
        numlaptimes = len(laptimes)
        numcartimes = len(list(set([t.car_id for t in laptimes])))
        numtracktimes = len(list(set([t.track_id for t in laptimes])))
        strategies = self.repo_strats.get_all()
        numstrats=len(strategies)
        numcarstrats=len(list(set([s.car_id for s in strategies])))
        numtrackstrats=len(list(set([s.track_id for s in strategies])))

        self.datarow = ft.Row([
            ft.Card(
                content=ft.Container(
                    padding=15,
                    width=250,
                    height=200,
                    content=ft.Column([
                        ft.Icon(ft.Icons.ANALYTICS, size=42),
                        ft.Text(f"{numstrats} saved strategies",
                            size=20,
                            weight=ft.FontWeight.BOLD),
                        ft.Text(f"with {numcarstrats} cars",
                            size=20,
                            weight=ft.FontWeight.BOLD),
                        ft.Text(f"on {numtrackstrats} tracks",
                            size=20,
                            weight=ft.FontWeight.BOLD)
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )),
            ft.Card(
                content=ft.Container(
                    padding=15,
                    width=250,
                    height=200,
                    content=ft.Column([
                        ft.Icon(ft.Icons.TIMER, size=42),
                        ft.Text(f"{numlaptimes} recorded laptimes",
                            size=20,
                            weight=ft.FontWeight.BOLD),
                        ft.Text(f"for {numcartimes} cars",
                            size=20,
                            weight=ft.FontWeight.BOLD),
                        ft.Text(f"on {numtracktimes} tracks",
                            size=20,
                            weight=ft.FontWeight.BOLD)
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )),
            ft.Card(
                content=ft.Container(
                    padding=15,
                    width=250,
                    height=200,
                    content=ft.Column([
                        ft.Icon(ft.Icons.LOCAL_GAS_STATION, size=42),
                        ft.Text(f"{numusages} fuel usages",
                            size=20,
                            weight=ft.FontWeight.BOLD)
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )),
            ft.Card(
                content=ft.Container(
                    padding=15,
                    width=250,
                    height=200,
                    content=ft.Column([
                        ft.Icon(ft.Icons.ROUTE, size=42),
                        ft.Text(f"{numlayouts} layouts",
                            size=20,
                            weight=ft.FontWeight.BOLD),
                        ft.Text(f"across {numtracks} tracks",
                            size=20,
                            weight=ft.FontWeight.BOLD)
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )),
            ft.Card(
                content=ft.Container(
                    padding=15,
                    width=250,
                    height=200,
                    content=ft.Column([
                        ft.Icon(ft.Icons.DIRECTIONS_CAR, size=42),
                        ft.Text(f"{numcars} cars",
                                size=20,
                                weight=ft.FontWeight.BOLD)
                    ],
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER)
                ))
        ],
        expand=False,
        wrap=False)

        super().__init__(
            expand=True,
            content=ft.Column([
                self.banner,
                ft.Divider(),
                self.datarow,
                ft.Divider()
            ],
            expand=True)
        )