import requests

inicio = "BIENVENIDOS A LA BASE DE DATOS DEL HOTEL"
ops = """\nElige que opcion deseas ralizar:
    1. Dar de alta una nueva habitacion
    2. Modificar los datos de una habitación
    3. Consultar la lista completa de habitaciones
    4. Consultar una habitacion mediante identificador
    5. Consultar la lista de habitaciones ocupadas o desocupadas.
    6. Eliminar una habitación
    7. Salir\n"""

print(inicio.center(75, '='),)

while True:
    print(ops)
    x = input()

    if x == '1':
        booked = bool(input("Se ocupara la habitacion? Ocupado=t/Libre=f? ") == 't')
        capacity = int(input("Cuantas plazas necesita para la habitacion? "))
        equip = [p.strip() for p in input("Que necesita tener en la habitación? Escriba la lista separada por comas: ").split(',')]

        datos = {"booked": booked, "capacity": capacity, "equipment": equip}
        try:
            response = requests.post('http://localhost:8080/rooms', json=datos)
            response.raise_for_status()
            print("Cliente creado con id {}".format(response.json()["id"]))
        except Exception:
            print("Ha ocurrido un error")
    if x == '2':
        id = input("Que habitacion desea modificar?\n")
        booked = bool(input("Se ocupara la habitacion? Ocupado=t/Libre=f? ") == 't')
        capacity = int(input("Cuantas plazas necesita para la habitacion? "))
        equip = [p.strip() for p in input("Que necesita tener en la habitación? Escriba la lista separada por comas: ").split(',')]

        datos = {"booked": booked, "capacity": capacity, "equipment": equip}
        try:
            response = requests.put('http://localhost:8080/rooms/{id}'.format(id=id), json=datos)
            response.raise_for_status()
        except Exception:
            print("Ha ocurrido un error")
    if x == '3':
        try:
            response = requests.get('http://localhost:8080/rooms')
            response.raise_for_status()

            print("\033c", end="")
            for y in response.json()["data"]:
                print("Habitacion {}: ".format(y["id"]))
                print("\t - {} plazas".format(y["capacity"]))
                print("\t - Equipamiento: {}".format(y["equipment"]))
                if y["booked"]:
                    print("\t - Ocupado\n")
                else:
                    print("\t - Libre\n")
        except Exception:
            print("Ha ocurrido un error")
    if x == '4':
        id = int(input("Introduzca el identificador de la habitacion:\n"))
        try:
            response = requests.get('http://localhost:8080/rooms/{id}'.format(id=id))
            response.raise_for_status()

            print("\033c", end="")
            print("Habitacion {}: \n".format(response.json()["id"]))
            print("\t - {} plazas".format(response.json()["capacity"]))
            print("\t - Equipamiento: {}".format(response.json()["equipment"]))
            if response.json()["booked"]:
                print("\t - Ocupado\n")
            else:
                print("\t - Libre\n")
        except Exception:
            print("Ha ocurrido un error. Puede que el id introducido no sea valido")
    if x == '5':
        status = bool(input("Que habitaciones desea visualizar? Ocupadas=t / Libres=f? ") == 't')
        try:
            response = requests.get('http://localhost:8080/rooms', params={"booked": status})
            response.raise_for_status()

            print("\033c", end="")
            for y in response.json()["data"]:
                print("Habitacion {}: ".format(y["id"]))
                print("\t - {} plazas".format(y["capacity"]))
                print("\t - Equipamiento: {}".format(y["equipment"]))
                if y["booked"]:
                    print("\t - Ocupado\n")
                else:
                    print("\t - Libre\n")
        except Exception:
            print("Ha ocurrido un error")
    if x == '6':
        id = input("Que habitacion desea eliminar?\n")
        try:
            response = requests.delete('http://localhost:8080/rooms/{id}'.format(id=id))
            response.raise_for_status()
            print("Habitacion eliminada con exito\n")
        except Exception:
            print("Ha ocurrido un error")
    if x == '7':
        break
        print("Fin de la sesion, hasta luego")
    if x not in ["1", "2", "3", "4", "5", "6", "7"]:
        print("Opcion no permitida, por favor seleccione entre 1 y 6.\n")
