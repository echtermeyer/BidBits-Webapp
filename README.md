# Before getting started

General steps you have to follow in order to use this repository:

- Use Python version 3.9.7.
- Change your credentials in the [secrets.json](secrets.json) file.
- Create the database "bidbits" and create all tables using [create_tables.sql](docs/create_tables.sql)

### Important Commands:

Start the Docker containers and expose an experimental database:

- `docker-compose up -d`

Start the application using:

- `python .\src\main.py`

### TODO:

- Create database using python (today)
- Create tables using python (today)
- Create first entries (today)
- Create easy to use UI using Dash (tomorrow)
- Fix ERD / database schema
