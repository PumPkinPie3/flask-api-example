# FLAKS-API-EXAMPLE
flask-api-example

## Enviroments
- Python 3.5.1
- MySQL 5.7.2

## How to install
```bash
$ pip install -r requirements.txt
```

## ENVs
- FLASK_APP
- FLASK_ENV
- MYSQL_DATABASE
- MYSQL_USER
- MYSQL_PASSWORD
- MYSQL_HOST

## How to initialize database
```bash
$ flask db_create
$ flask db_init
```

## Run
```bash
$ flask run -h 0.0.0.0
```

## Test
```bash
$ python -m unittest tests.test_api
```