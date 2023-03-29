# Gestor de clientes en Python
Proyecto final del curso de Python en Udemy.
Este gestor almacena datos de clientes (DNI, nombre y apellido), con la posibilidad de crear, modificar y borrar datos.

## Uso:

* El DNI tiene dos números enteros seguidos de una letra.
* El nombre puede tener entre 3 y 20 caracteres.
* El apellido puede tener entre 2 y 20 caracteres.


## RoadMap de scripts:
```bash
run.py -> menu.py -> herlpers.py
                  -> database.py -> config.py -> clientes.csv
```

## Instalar las dependencias

_Nota: Sólo incluye pytest para realizar pruebas unitarias._

```bash
pip install -r requirements.txt
```

## Para probar el programa en modo gráfico

```bash
python run.py
```

## Para probar el programa en modo terminal

```bash
python run.py -t
```

## Para ejecutar las pruebas unitarias

```bash
pytest -v
```
