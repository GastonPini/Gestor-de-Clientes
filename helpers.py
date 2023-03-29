## Contiene funciones auxiliares de uso general en el proyecto
import re
import os
import platform

def limpiar_pantalla():
    ##if platform.system == "Windows":
    ##    os.system('cls')
    ##else:
    ##    os.system('clear')
    os.system('cls') if platform.system() == "Windows" else os.system('clear')

def leer_texto(min=0, max=100, mensaje=None):
    print(mensaje) if mensaje else None
    while True:
        texto = input("> ")
        if len(texto) >= min and len(texto) <= max:
            return texto
        
def dni_valido(dni, lista):
    if not re.match('[0-9]{2}[A-Z]$', dni):
        print("DNI incorrecto, debe cumplir el formato.")
        return False
    for cliente in lista:
        if cliente.dni == dni:
            print("DNI utilizado por otro cliente.")
            return False
    return True