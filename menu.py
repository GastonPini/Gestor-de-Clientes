## Interfaz, une run.py con la base de datos
import sys
import os
import helpers as h
import database as db

def iniciar():
    while True:
        h.limpiar_pantalla()
        ## os.system('cls') ## Limpiar lo mostrado en pantalla: cls en Windows, clear en Linux
        
        print("========================")
        print("  Bienvenido al Gestor  ")
        print("========================")
        print("[1] Listar los clientes ")
        print("[2] Buscar un cliente   ")
        print("[3] Añadir un cliente   ")
        print("[4] Modificar un cliente")
        print("[5] Borrar un cliente   ")
        print("[6] Cerrar el Gestor    ")
        print("========================")

        opcion = input("> ")
        h.limpiar_pantalla()

        if opcion == '1':
            print("Listando los clientes...\n")
            for cliente in db.Clientes.lista:
                print(cliente)

        elif opcion == '2':
            print("Buscando un cliente...\n")
            dni = h.leer_texto(3, 3, "DNI: 2 ints + 1 char").upper()
            cliente = db.Clientes.buscar(dni)
            print(cliente) if cliente else print("Cliente inexistente")

        elif opcion == '3':
            print("Añadiendo un cliente...\n")
            dni = None
            while True:
                dni = h.leer_texto(3, 3, "DNI: 2 ints + 1 char").upper()
                if h.dni_valido(dni, db.Clientes.lista):
                    break

            nombre = h.leer_texto(2, 30, "Nombre: 2 a 30 char").capitalize()
            apellido = h.leer_texto(2, 30, "Apellido: 2 a 30 char").capitalize()
            db.Clientes.crear(dni, nombre, apellido)
            print("Cliente creado correctamente")

        elif opcion == '4':
            print("Modificando un cliente...\n")
            dni = h.leer_texto(3, 3, "DNI: 2 ints + 1 char").upper()
            cliente = db.Clientes.buscar(dni)
            if cliente:
                nombre = h.leer_texto(2, 30, f"Nombre: 2 a 30 char {cliente.nombre}").capitalize()
                apellido = h.leer_texto(2, 30, f"Apellido: 2 a 30 char {cliente.apellido}").capitalize()
                db.Clientes.modificar(dni, nombre, apellido)
                print("Cliente modificado correctamente")
            else:
                print("Cliente no encontrado")

        elif opcion == '5':
            print("Borrando un cliente...\n")
            dni = h.leer_texto(3, 3, "DNI: 2 ints + 1 char").upper()
            print("Cliente borrado") if db.Clientes.eliminar(dni) else print("Cliente no encontrado")

        elif opcion == '6':
            print("Saliendo...\n")
            break

        input("\nPresiona ENTER para continuar...")