inicio = "BIENVENIDOS A LA BASE DE DATOS DEL HOTEL"
ops = """Elige que opcion deseas ralizar:
    1. Dar de alta una nueva habitacion
    2. Modificar los datos de una habitación
    3. Consultar la lista completa de habitaciones
    4. Consultar una habitacion mediante identificador
    5. Consultar la lista de habitaciones ocupadas o desocupadas
    6. Salir"""

print(inicio.center(136, '-'),)

print(ops)
items = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6}
