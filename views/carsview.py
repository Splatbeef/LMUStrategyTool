import flet as ft
from models import Car, CarAlias
from Repositories.repositories import *


class CarsView(ft.Container):
    def __init__(self, repos: Repositories):
        self.car_repo = repos.car
        self.class_repo = repos.classes
        self.alias_repo = repos.caralias
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
        self.filters()
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
                        ft.Column(
                            controls=[self.filter_row,self.cars_table],
                            expand=True,
                            scroll=ft.ScrollMode.AUTO
                                  ),
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
                    ],
                    expand=True)                    
                ]
            )
        )

    def filters(self):
        self.carfilter = ft.Dropdown(label="Car", on_select=self.refresh_table, editable=True, enable_search=True)
        cars = self.car_repo.get_all()
        self.carfilter.options = [
            ft.dropdown.Option(
                key=str(c.id),
                text=c.name
            ) 
            for c in cars
        ]
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
            self.carfilter,
            self.classfilter
        ],
        expand=True)

    def clear_filters(self):
        self.carfilter.value=None
        self.classfilter.value=None
        self.refresh_table()

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
        if not self.classfilter.value and not self.carfilter.value:
            cars = self.car_repo.get_all()
        elif self.classfilter.value and not self.carfilter.value:
            cars = self.car_repo.get_by_class(int(self.classfilter.value))
        elif self.carfilter.value and not self.classfilter.value:
            cars = [self.car_repo.get_by_id(int(self.carfilter.value))]
        else:
            car=self.car_repo.get_by_id(int(self.carfilter.value))
            if car.carclass_id == int(self.classfilter.value):
                cars=[car]
            else:
                cars=[]
        

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

        if not self.checks():
            return

        car = Car(
            id=None,
            name=self.name_field.value,
            carclass_id = int(self.class_dropdown.value),
            fuel_capacity = float(self.fuel_capacity_field.value),
            ve=self.ve_checkbox.value
        )
        alias = CarAlias(
            id = None,
            alias=self.name_field.value,
            name=self.name_field.value
        )

        self.car_repo.add(car)
        self.alias_repo.add(alias)

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
        if not self.checks():
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
        oldcar = self.car_repo.get_by_id(self.selected_car_id)
        aliases = self.alias_repo.get_by_name(oldcar.name)
        for a in aliases:
            self.alias_repo.update(
                CarAlias(
                    id=a.id,
                    alias=a.alias,
                    name=self.name_field.value
                )
            )

        self.car_repo.update(car)

        self.clear_form()

        self.refresh_table()

        self.update()

    def checks(self):
        if not self.name_field.value:
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"No Name Found"),
                title_padding = ft.Padding.all(25),
                content=ft.Text("Please add a car name")
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return False
        if not self.class_dropdown.value:
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"No Class Found"),
                title_padding = ft.Padding.all(25),
                content=ft.Text("Please select a class")
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return False
        if not self.fuel_capacity_field.value:
            dialog = ft.AlertDialog(
                modal=False,
                alignment=ft.Alignment.CENTER,
                title=ft.Text(f"No Fuel Capacity Found"),
                title_padding = ft.Padding.all(25),
                content=ft.Text("Please input the fuel tank capacity")
            )
            self.page.show_dialog(dialog)
            self.page.update()
            return False
        return True

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