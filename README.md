# GEO API

REST API for GEO app

Technologies used:
- Django REST Framework
- PostgreSQL(with PostGIS extension)
- Docker
## Installing using GitHub:

```shell
  git clone https://github.com/danylo-d/postgis_test_task.git
  cd postgis_test_task
  python -m venv venv
Linux/macOS:
  source venv/bin/activate
Windows: 
  venv\Scripts\activate
```

## Run with docker:
```shell
  docker-compose up --build
```

## Features:
- Admin panel (/admin/)
- SWAGER documentation (/api/doc/swagger/) (explanation of how to use each endpoint.)
- Getting a list of places
- Creating a new location
- Update information about the place;
- Deleting a place;
- Search for the nearest place to a given point

## Test coverage:
- Cover all custom methods with tests