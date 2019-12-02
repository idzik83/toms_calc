# Tomas calculator

## Installing project dependencies
* install virtual environment:
```.bash
python3 -m virtualenv .venv 
```
* activate virtual environment
```bash
source .venv/bin/activate 
```
* install dependencies from `requirements` file
```bash
pip install -r requirements.txt
```

## Running tests
To run tests:
```bash
python manage.py test
```

## Starting project
To start project:
```bash
python manage.py runserver
```
Local dev server will be started listening on port 8000

## Verify results
To check results send `POST` request to endpoint `http://127.0.0.1:8000/api/orders/` with
the following payload:
```json
{
   "price": 1000,
   "quantity": 15,
   "state_code": "tx"
}
```
Example response:
```json
{
    "price": 1000.0,
    "quantity": 15,
    "state_code": "tx",
    "total": 14343.75
}
```