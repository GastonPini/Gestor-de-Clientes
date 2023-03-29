## Controla los datos y provee una interfaz para editar/agregar/eliminar información
import csv
import config

class Cliente:
    def __init__(self, dni, nombre, apellido):
        self.dni = dni ## Variables a nivel de instancia
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        return f"{self.dni} {self.nombre} {self.apellido}"


class Clientes:

    lista = [] ## Variables a nivel de clase

    with open(config.DATABASE_PATH, newline = '\n') as fichero: ## carga de clientes desde un fichero
        reader = csv.reader(fichero, delimiter = ';')
        for dni, nombre, apellido in reader:
            cliente = Cliente(dni, nombre, apellido)
            lista.append(cliente)

    @staticmethod ## métodos que no gestionan instancias, se manejan con la clase
    def buscar(dni):
        for cliente in Clientes.lista:
            if cliente.dni == dni:
                return cliente
            
    @staticmethod
    def crear(dni, nombre, apellido):
        cliente = Cliente(dni, nombre, apellido)
        Clientes.lista.append(cliente)
        Clientes.guardar()
        return cliente
    
    @staticmethod
    def modificar(dni, nombre, apellido):
        for indice, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                Clientes.lista[indice].nombre = nombre
                Clientes.lista[indice].apellido = apellido
                Clientes.guardar()
                return Clientes.lista[indice]
            
    @staticmethod
    def eliminar(dni):
        for indice, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                cliente = Clientes.lista.pop(indice)
                Clientes.guardar()
                return cliente
            
    @staticmethod
    def guardar():
        with open(config.DATABASE_PATH, 'w', newline = '\n') as fichero: ## carga de clientes desde un fichero
            writer = csv.writer(fichero, delimiter = ';')
            for cliente in Clientes.lista:
                writer.writerow((cliente.dni, cliente.nombre, cliente.apellido))