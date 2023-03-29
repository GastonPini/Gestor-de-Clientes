# Customer manager in Python
Final project of the Python course in Udemy.
This manager stores customer data (ID, name and surname), with the possibility of creating, modifying and deleting data.

## Usage:

* The DNI has two integers followed by a letter.
* The name can have between 3 and 20 characters.
* The last name can have between 2 and 20 characters.


## Scripts RoadMap
```bash
run.py -> menu.py -> herlpers.py
                  -> database.py -> config.py -> customers.csv
```

## Install the dependencies

_Note: Only include pytest for unit testing._

```bash
pip install -r requirements.txt
```

## Test the program in graphical mode

```bash
python run.py
```

## Test the program in terminal mode

```bash
python run.py -t
```

## Run the unit tests

```bash
pytest -v
```