import flet as ft
import datetime as dt

from repositories.repositories import *
from services.version_service import *

class HomeView(ft.Container):
    def __init__(self, repos: Repositories):
        self.repo_car = repos.car
        self.repo_track = repos.track
        self.repo_settings = repos.settings
        self.repo_fuel = repos.fuel
        self.repo_laptimes = repos.laptime
        self.repo_strats = repos.strategy
        self.version_service = VersionService(repos.settings)

        self.version= self.repo_settings.get_by_key("Version")
        version_number = self.version.value_str
        self.overtake_button=ft.Button(content="Overtake", url="https://www.overtake.gg/members/splatbeef.2023019/#resources")
        self.github_button=ft.Button(content="GitHub", url="https://github.com/Splatbeef/LMUStrategyTool")
        self.version_column = ft.Column([
            ft.Text(f"Version: {version_number}", size=16),
            self.github_button,
            self.overtake_button
        ])

        self.check_button = ft.Button(content="Check Version", on_click=self.check_version_pressed)
        self.check_row = ft.Row([])
        self.check_version_pressed()

        self.banner = ft.Row([
            #Add icon here
            ft.Column([
                ft.Text("LMU Strategy Tool", size=60, weight=ft.FontWeight.BOLD),
                ft.Text(f"by Splatbeef", size=16)
            ]),
            ft.Container(expand=True),
            self.version_column
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
                self.check_row,
                ft.Divider(),
                self.datarow,
                ft.Divider()
            ],
            expand=True)
        )

    def check_version_pressed(self, e=None):
        version_check = self.version_service.check_version()
        self.check_row.controls=[self.check_button]
        if version_check["status"]=="Check Failed":
            self.check_row.controls.append(ft.Text("Version Check Failed"))
        else:
            if version_check["up_to_date"]:
                self.check_row.controls.append(ft.Text("Version Up To Date!"))
            else:
                self.check_row.controls.append(ft.Text(f"Latest version available: {version_check["latest"]}"))
                self.check_row.controls.append(ft.Button(content="View on GitHub", url="https://github.com/Splatbeef/LMUStrategyTool/releases/latest"))
                self.check_row.controls.append(ft.Button("View on Overtake", url="https://www.overtake.gg/members/splatbeef.2023019/#resources"))