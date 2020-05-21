# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from PyInquirer import prompt

from examples import custom_style_2

import requests

from rich.console import Console
from rich.table import Column, Table


class Client():
    questions = [
        {
            'type': 'list',
            'name': 'option',
            'message': '¿Que desea realizar?',
            'choices': [
                {
                    'name': 'Dar de alta una nueva habitacion',
                    'value': 1
                },
                {
                    'name': 'Modificar los datos de una habitación', 'value': 2
                },
                {
                    'name': 'Consultar la lista completa de habitaciones',
                    'value': 3
                },
                {
                    'name': 'Consultar una habitacion mediante identificador',
                    'value': 4
                },
                {
                    'name': 'Consultar la lista de habitaciones ocupadas o desocupadas',
                    'value': 5
                },
                {
                    'name': 'Dar de baja una habitacion',
                    'value': 6
                },
                {
                    'name': 'Salir',
                    'value': 7
                }
            ]
        }
    ]

    base_url = "http://127.0.0.1:8080/rooms"
    console = Console()
    room_fields = [
        {
            'type': 'confirm',
            'name': 'booked',
            'message': '¿Esta la habitación reservada?',
            'default': False,
        },
        {
            'type': 'input',
            'name': 'capacity',
            'message': '¿Cual es la capacidad de la habitación?',
            'default': '2',
            'filter': lambda val: int(val)
        },
        {
            'type': 'input',
            'name': 'equipment',
            'message': 'Equipamiento',
            'filter': lambda val: [equip.strip() for equip in val.split(',')] if val else []
        },
    ]

    def __init__(self):
        self.loop = True
        pass

    def option_1(self):
        room = prompt(self.room_fields, style=custom_style_2)
        try:
            response = requests.post(self.base_url, json=room)
            response.raise_for_status()
            room_id = response.json()["id"]
            message = "Habitacion creada con el [bold cyan]id[/bold cyan]"
            " = [bold cyan]{id}[/bold cyan].".format(id=room_id)
            self.console.print(message)
        except requests.HTTPError as e:
            self.console.print("Error en el sevidor: " +
                               e.response.json()['message'], style="bold red")

    def option_2(self):
        fields_to_change = [
            {
                'type': 'checkbox',
                'name': 'fields',
                'message': '¿Qué campos desea modificar?',
                'choices': [
                    {
                        'name': 'booked'
                    },
                    {
                        'name': 'capacity'
                    },
                    {
                        'name': 'equipment'
                    }
                ]
            }
        ]
        selected_fields = prompt(
            fields_to_change, style=custom_style_2)['fields']
        fields = filter(lambda field: field['name']
                        in selected_fields, self.room_fields)
        room = prompt(fields, style=custom_style_2)
        question = [
            {
                'type': 'input',
                'name': 'id',
                'message': '¿Cual es el id del la habitación?'
            }
        ]
        room_id = prompt(question, style=custom_style_2)['id']
        try:
            response = requests.put(self.base_url+'/'+room_id, json=room)
            response.raise_for_status()
            room = response.json()
            table = Table(
                Column("id"),
                Column("booked"),
                Column("capacity"),
                Column("equipment"),
                show_header=True,
                header_style="bold cyan"
            )
            table.add_row(str(room['id']), str(room['booked']),
                          str(room['capacity']), ', '.join(room['equipment']))
            self.console.print(table)
        except requests.HTTPError as e:
            self.console.print("Error en el sevidor: " +
                               e.response.json()['message'], style="bold red")

    def option_3(self):
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            rooms = response.json()['data']
            table = Table(
                Column("id"),
                Column("booked"),
                Column("capacity"),
                Column("equipment"),
                show_header=True,
                header_style="bold cyan"
            )
            for room in rooms:
                table.add_row(str(room['id']), str(room['booked']),
                              str(room['capacity']), ', '.join(room['equipment']))
            self.console.print(table)
        except requests.HTTPError as e:
            self.console.print("Error en el sevidor: " +
                               e.response.json()['message'], style="bold red")

    def option_4(self):
        question = [
            {
                'type': 'input',
                'name': 'id',
                'message': '¿Cual es el id del la habitación?'
            }
        ]
        room_id = prompt(question, style=custom_style_2)['id']
        try:
            response = requests.get(self.base_url + '/' + room_id)
            response.raise_for_status()
            room = response.json()
            table = Table(
                Column("id"),
                Column("booked"),
                Column("capacity"),
                Column("equipment"),
                show_header=True,
                header_style="bold cyan"
            )
            table.add_row(str(room['id']), str(room['booked']),
                          str(room['capacity']), ', '.join(room['equipment']))
            self.console.print(table)
        except requests.HTTPError as e:
            self.console.print("Error en el sevidor: " +
                               e.response.json()['message'], style="bold red")

    def option_5(self):
        question = [{
            'type': 'confirm',
            'name': 'booked',
            'message': '¿Esta la habitación reservada?',
            'default': False,
        }]

        query_params = prompt(question, style=custom_style_2)

        try:
            response = requests.get(self.base_url, params=query_params)
            response.raise_for_status()
            rooms = response.json()['data']
            table = Table(
                Column("id"),
                Column("booked"),
                Column("capacity"),
                Column("equipment"),
                show_header=True,
                header_style="bold cyan"
            )
            for room in rooms:
                table.add_row(str(room['id']), str(room['booked']),
                              str(room['capacity']), ', '.join(room['equipment']))
            self.console.print(table)
        except requests.HTTPError as e:
            self.console.print("Error en el sevidor: " +
                               e.response.json()['message'], style="bold red")

    def option_6(self):
        question = [
            {
                'type': 'input',
                'name': 'id',
                'message': '¿Cual es el id del la habitación a eliminar?'
            }
        ]
        room_id = prompt(question, style=custom_style_2)['id']
        try:
            response = requests.delete(self.base_url + '/' + room_id)
            response.raise_for_status()
            room_id = response.json()["id"]
            message = "Se ha eliminado la habiatación con el [bold cyan]id[/bold cyan] "
            "= [bold cyan]{id}[/bold cyan].".format(id=room_id)
            self.console.print(message)
        except requests.HTTPError as e:
            self.console.print("Error en el sevidor: " +
                               e.response.json()['message'], style="bold red")

    def option_7(self):
        self.loop = False

    def handle_options(self, option: int):
        handler = getattr(self, 'option_'+str(option))
        handler()

    def run(self):
        while self.loop:
            answers = prompt(self.questions, style=custom_style_2)
            option = answers['option']
            self.handle_options(answers['option'])
            self.loop = option != 7
            if self.loop:
                input("Pulse para continuar...")
            print("\033c", end="")


if __name__ == "__main__":
    client = Client()
    client.run()
