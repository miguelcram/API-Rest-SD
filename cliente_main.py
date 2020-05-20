import requests

inicio = "BIENVENIDOS A LA BASE DE DATOS DEL HOTEL"
ops = """Elige que opcion deseas ralizar:
    1. Dar de alta una nueva habitacion
    2. Modificar los datos de una habitación
    3. Consultar la lista completa de habitaciones
    4. Consultar una habitacion mediante identificador
    5. Consultar la lista de habitaciones ocupadas o desocupadas
    6. Salir"""

print(inicio.center(150, '='),)
print(ops)

for x in ["1", "2", "3", "4", "5", "6"]:
    if x == '1':
        print("opcion %x\n")
        response = requests.get('http://localhost:8080/create_room')
    if x == '2':
        print("opcion %x\n")
        response = requests.get('http://localhost:8080/update_room')
    if x == '3':
        print("opcion %x\n")
        response = requests.get('http://localhost:8080/list_room')
        response.text
    if x == '4':
        print("opcion %x\n")
        print("Introduzca el identificador de la habitacion:\n")
        id = input()
        response = requests.get('http://localhost:8080/get_room')
    if x == '5':
        print("opcion %x\n")
        response = requests.get('http://localhost:8080/delete_room')
    if x == '6':
        print("opcion %x\n")
