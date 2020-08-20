# BDT Floripa API backend

Implementation of the backend that provides the API endpoints for BDT Floripa
and it's management.

## Project setup
```
# Clone this repo

# run migrations 
docker-compose run api python manage.py migrate

# create new superuser (admin)
docker-compose run api python manage.py createsuperuser

# type email, password and password confirmation

# visit http://localhost:8000/admin

```
