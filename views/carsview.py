import flet as ft
from models import Car
from Repositories.car_repository import CarRepository
from Repositories.carclass_repository import CarClassRepository


class CarsView(ft.Container):
    def __init__(self, car_repo: CarRepository, class_repo: CarClassRepository):
        self.car_repo = car_repo
        self.class_repo = class_repo

        self.name_field = ft.TextField(label="Car Name")
        self.class_dropdown = ft.Dropdown(label="Class")
        self.fuel_capacity_field = ft.TextField(label="Fuel Tank Capacity")
        self.ve_checkbox = ft.Checkbox(label="VE Capable")

        self.cars_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Car")),
                ft.DataColumn(ft.Text("Class")),
                ft.DataColumn(ft.Text("Fuel Tank")),
                ft.DataColumn(ft.Text("VE"))
            ],
            rows=[]
        )

        self.add_button = ft.Button(content="Add Car", on_click=self.add_car)
        self.edit_button = ft.Button(content="Save Changes", on_click=self.save_car, disabled=True)
        self.clear_button = ft.Button(content="Clear Fields", on_click=self.clear_form)
        self.delete_button = ft.Button(content="Delete", on_click=self.delete_car, disabled=True)

        self.load_classes()
        self.refresh_table()

        super().__init__(
            expand=True,
            content=ft.Column(
                [
                    ft.Text(
                        "Cars",
                        size=28,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Row([
                        self.cars_table,
                        ft.Column([
                            self.name_field,
                            self.class_dropdown,
                            self.fuel_capacity_field,
                            self.ve_checkbox,

                            ft.Divider(),

                            ft.Column([
                                self.add_button,
                                self.edit_button,
                                self.clear_button,
                                self.delete_button
                            ]),
                        ])
                    ])                    
                ]
            )
        )

    def load_classes(self):
        classes = self.class_repo.get_all()
        self.class_dropdown.options = [
            ft.dropdown.Option(
                key=str(c.id),
                text=c.name
            ) 
            for c in classes
        ]

    def refresh_table(self):
        cars = self.car_repo.get_all()

        classes = {
            c.id: c.name
            for c in self.class_repo.get_all()
        }

        cars = sorted(
            cars,
            key=lambda c:(
                classes.get(c.carclass_id, ""),
                c.name.lower()
            )
        )

        self.cars_table.rows.clear()

        for car in cars:
            self.cars_table.rows.append(
                ft.DataRow(
                    on_select_change=lambda e, car=car: self.edit_car(car),
                    cells=[
                        ft.DataCell(ft.Text(car.name)),
                        ft.DataCell(ft.Text(classes.get(car.carclass_id, "?"))),
                        ft.DataCell(ft.Text(str(car.fuel_capacity))),
                        ft.DataCell(ft.Text("Yes" if car.ve else "No"))
                    ]
                )
            )

    def add_car(self):

        car = Car(
            id=None,
            name=self.name_field.value,
            carclass_id = int(self.class_dropdown.value),
            fuel_capacity = float(self.fuel_capacity_field.value),
            ve=self.ve_checkbox.value
        )

        self.car_repo.add(car)

        self.clear_form()

        self.refresh_table()
        self.update()

    def edit_car(self, car: Car):

        self.selected_car_id = car.id

        self.name_field.value = car.name

        self.class_dropdown.value = str(
            car.carclass_id
        )

        self.fuel_capacity_field.value = str(
            car.fuel_capacity
        )

        self.ve_checkbox.value = car.ve

        self.edit_button.disabled = False
        self.delete_button.disabled = False

        self.update()

    def save_car(self, e):

        if self.selected_car_id is None:
            return

        car = Car(
            id=self.selected_car_id,
            name=self.name_field.value,
            carclass_id=int(
                self.class_dropdown.value
            ),
            fuel_capacity=float(
                self.fuel_capacity_field.value
            ),
            ve=self.ve_checkbox.value
        )

        self.car_repo.update(car)

        self.clear_form()

        self.refresh_table()

        self.update()

    def clear_form(self):

        self.selected_car_id = None

        self.name_field.value = ""
        self.class_dropdown.value = None
        self.fuel_capacity_field.value = ""
        self.ve_checkbox.value = False

        self.edit_button.disabled = True

        self.update()

    def delete_car(self):
        if self.selected_car_id is None:
            return

        self.car_repo.delete(self.selected_car_id)

        self.clear_form()
        self.refresh_table()
        self.update()