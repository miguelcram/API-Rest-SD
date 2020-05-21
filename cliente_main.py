import requests

inicio = "BIENVENIDOS A LA BASE DE DATOS DEL HOTEL"
ops = """\nElige que opcion deseas ralizar:
    1. Dar de alta una nueva habitacion
    2. Modificar los datos de una habitación
    3. Consultar la lista completa de habitaciones
    4. Consultar una habitacion mediante identificador
    5. Eliminar una habitación
    6. Salir\n"""

print(inicio.center(75, '='),)

while True:
    print(ops)
    x = input()

    if x == '1':
        booked = bool(input("Se ocupara la habitacion? t/f? ") == 't')
        capacity = int(input("Cuantas plazas necesita para la habitacion? "))
        equip = [p.strip() for p in input("Que necesita tener en la habitación? Escriba la lista separada por comas: ").split(',')]  # noqa:E501

        datos = {"booked": booked, "capacity": capacity, "equipment": equip}
        try:
            response = requests.post('http://localhost:8080/rooms', json=datos)  # noqa:E501
            print("Cliente creado con id {}".format(response.json()["id"]))
        except Exception:
            print("Ha ocurrido un error")
    if x == '2':
        id = input("Que habitacion desea modificar?\n")
        booked = bool(input("Se ocupara la habitacion? t/f?") == 't')
        capacity = int(input("Cuantas plazas necesita para la habitacion? "))
        equip = [p.strip() for p in input("Que necesita tener en la habitación? Escriba la lista separada por comas: ").split(',')]  # noqa:E501

        datos = {"booked": booked, "capacity": capacity, "equipment": equip}
        try:
            response = requests.put('http://localhost:8080/rooms/{id}'.format(id=id), data=datos)  # noqa:E501
        except Exception:
            print("Ha ocurrido un error")
    if x == '3':
        try:
            response = requests.get('http://localhost:8080/rooms')
        except Exception:
            print("Ha ocurrido un error")

        for y in response.json()["data"]:
            print("Habitacion {}: ".format(y["id"]))
            print("\t - {} plazas".format(y["capacity"]))
            print("\t - Equipamiento: {}".format(y["equipment"]))
            if y["booked"]:
                print("\t - Libre\n")
            else:
                print("\t - Ocupado\n")
    if x == '4':
        id = int(input("Introduzca el identificador de la habitacion:\n"))
        try:
            response = requests.get('http://localhost:8080/rooms/{id}'.format(id=id))  # noqa:E501
            print("Habitacion {}: \n".format(response.json()["id"]))
            print("\t - {} plazas".format(response.json()["capacity"]))
            print("\t - Equipamiento: {}".format(response.json()["equipment"]))
            if response.json()["booked"]:
                print("\t - Libre\n")
            else:
                print("\t - Ocupado\n")
        except Exception:
            print("Ha ocurrido un error. Puede que el id introducido no sea valido")  # noqa:E501
    if x == '5':
        id = input("Que habitacion desea eliminar?\n")
        try:
            response = requests.delete('http://localhost:8080/rooms/{id}'.format(id=id))  # noqa:E501
            print("Habitacion eliminada con exito\n")
        except Exception:
            print("Ha ocurrido un error")
    if x == '6':
        break
        print("Fin de la sesion, hasta luego")
    if x not in ["1", "2", "3", "4", "5", "6"]:
        print("Opcion no permitida, por favor seleccione entre 1 y 6.\n")
