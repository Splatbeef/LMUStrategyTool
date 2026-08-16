import flet as ft

from Repositories.repositories import *
from models import Setting

class SettingsView(ft.Container):
    def __init__(self, repos: Repositories):
        self.repo = repos.settings

        self.save_button = ft.Button(content="Save Changes", on_click=self.save_settings)

        self.load_settings()

        super().__init__(
            expand=True,
            content=ft.Column(
                [
                    ft.Text(
                        "Settings",
                        size=28,
                        weight=ft.FontWeight.BOLD
                    ),
                    self.save_button,
                    ft.Divider(),
                    self.sessiontype_row,
                    self.multiplier_row
                ],
                expand=True
            )
        )

    def load_settings(self):
        #Laptime sessiontypes
        self.session_dropdown = ft.Dropdown(label="Sessions",options=[
            ft.dropdown.Option(
                key=str(0),
                text="Qualifying, Race"
            ),
            ft.dropdown.Option(
                key=str(1),
                text="Qualifying, Race, Practice"
            ),
            ft.dropdown.Option(
                key=str(2),
                text="Qualifying, Race, Quali Practice, Race Practice"
            )
        ])
        self.session_dropdown.value = str(self.repo.get_by_key("Laptime Sessiontypes").value_int)
        self.sessiontype_row = ft.Row([
            ft.Text("Sessiontypes for laptimes:"),
            self.session_dropdown
        ])

        #Multiplier
        self.multiplier_field = ft.TextField(label="Multiplier")
        self.multiplier_field.value = str(self.repo.get_by_key("Laptime Multiplier").value_float)
        self.multiplier_row = ft.Row([
            ft.Text("Reference laptime multiplier:"),
            self.multiplier_field
        ])

    def save_settings(self):
        if not self.checks():
            return None
        setting = self.repo.get_by_key("Laptime Sessiontypes")
        if setting.value_int != int(self.session_dropdown.value):
            new = Setting(
                id = setting.id,
                key = "Laptime Sessiontypes",
                value_str = None,
                value_bool = None,
                value_int = int(self.session_dropdown.value),
                value_float = None
            )
            self.repo.update(new)

        setting = self.repo.get_by_key("Laptime Multiplier")
        if setting.value_float != float(self.multiplier_field.value):
            new = Setting(
                id = setting.id,
                key = "Laptime Multiplier",
                value_str = None,
                value_bool = None,
                value_int = None,
                value_float = float(self.multiplier_field.value)
            )
            self.repo.update(new)


        dialog = ft.AlertDialog(
            modal=False,
            alignment=ft.Alignment.CENTER,
            title=ft.Text(f"Settings Saved"),
            title_padding = ft.Padding.all(25),
            content=ft.Text("All changes have been saved")
        )
        self.page.show_dialog(dialog)
        self.page.update()

    def checks(self):
        try:
            multiplier = float(self.multiplier_field.value)
        except:
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"Multiplier not valid"),
                title_padding = ft.Padding.all(25),
                content=ft.Text("Multiplier is not a valid number")
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return False
        return True
        