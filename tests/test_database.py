import copy
import unittest
import csv
import config
import helpers as h
import database as db

## pip install pytest
## pytest -v

class TestDatabase(unittest.TestCase):

    def setUp(self): ## Método ejecutado al principio de cada test
        db.Clientes.lista = [
            db.Cliente('15M', 'Melisa', 'Perez'), ## MockUp objects
            db.Cliente('12V', 'Juan', 'Gomwz'),
            db.Cliente('13M', 'Maria', 'Gonzalez')
        ]

    def test_buscar_cliente(self):
        cliente_existente = db.Clientes.buscar('15M')
        cliente_inexistente = db.Clientes.buscar('15V')
        self.assertIsNotNone(cliente_existente) ## Si el cliente en búsqueda existe
        self.assertIsNone(cliente_inexistente) ## Si el cliente en búsqueda no existe

    def test_crear_cliente(self):
        nuevo_cliente = db.Clientes.crear('15M', 'Gaston', 'Pini')
        self.assertEqual(len(db.Clientes.lista), 4) ## el tamaño actual de clientes es 4
        self.assertEqual(nuevo_cliente.dni, '15M') ## Si existe el cliente con DNI...
        self.assertEqual(nuevo_cliente.nombre, 'Gaston') ## Si existe el cliente con nombre...
        self.assertEqual(nuevo_cliente.apellido, 'Pini') ## Si existe el cliente con apellido...

    def test_modificar_cliente(self): # Los objetos se manejan por referencia, por lo que se crea una copia
        cliente_a_modificar = copy.copy(db.Clientes.buscar('12V'))
        cliente_modificado = db.Clientes.modificar('12V', 'Mariano', 'Martinez')
        self.assertEqual(cliente_a_modificar.nombre, 'Juan') ## Si el cliente a modificar es de nombre...
        self.assertEqual(cliente_modificado.nombre, 'Gaston') ## Si el cliente modificado es de nombre...
        
    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar('12V')
        cliente_buscado = db.Clientes.buscar('12V')
        self.assertEqual(cliente_borrado.dni, '12V')
        self.assertIsNone(cliente_buscado)

    def test_dni_valido(self):
        self.assertTrue(h.dni_valido('00A', db.Clientes.lista))
        self.assertFalse(h.dni_valido('232323S', db.Clientes.lista))
        self.assertFalse(h.dni_valido('F35', db.Clientes.lista))
        self.assertFalse(h.dni_valido('48H', db.Clientes.lista))

    def test_escritura_csv(self):
        db.Clientes.borrar('15M')
        db.Clientes.borrar('12V')
        db.Clientes.modificar('13M', 'Mikasa', 'Ackerman')

        dni, nombre, apellido = None, None, None
        with open(config.DATABASE_PATH, newline = '\n') as fichero:
            reader = csv.reader(fichero, delimiter = ';')
            dni, nombre, apellido = next(reader)

        self.assertEqual(dni, '13M')
        self.assertEqual(nombre, 'Mikasa')
        self.assertEqual(apellido, 'Ackerman')