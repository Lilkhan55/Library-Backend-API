# Library Backend API

![PyPI - Version](https://img.shields.io/pypi/v/django?label=django)
![Python](https://img.shields.io/pypi/pyversions/Django.svg?label=Python)
![Django_Rest_Framework](https://img.shields.io/pypi/v/django_rest_framework?label=rest_framework&color=blue
)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-✓-green)
![Redis](https://img.shields.io/badge/Redis-✓-red)

## About Project 
This project is built using the Django REST Framework. The idea behind my project is that you can view information about a book using API endpoint.
The site has registration, authorization and JWT token base, including OAuth authorization. Swagger documentation was wrote by drf-spectacular, according to standard OpenAPI3. You can add new books if you are part of the moderator group. Users can rent and return books on the site.

## Architecture
A monolithic backend application with a REST API architecture.
The application uses PostgreSQL as the main data store, Redis for caching, and Nginx/Gunicorn for production deployment.

## API documentation
Interactive API documentation is available via Swagger UI:
- Swagger UI: /api/schema/swagger-ui/
- OpenAPI Schema: /api/schema/
- ReDoc: /api/schema/redoc/

## API endpoints
For books:
- library/api/v1/books/
- library/api/v1/books/{id}/
- library/api/v1/genre/
- library/api/v1/genre/{id}/
- library/api/v1/tag/
- library/api/v1/tag/{id}/

For users:
- users/api/v1/login/
- users/api/v1/token/refresh/
- users/api/v1/token/verify/
- users/api/v1/registration/

## Tech Stack
- **Python** 3.11  
- **Django REST Framework** 3.17.1
- **Django REST Framework SimpleJwt** - 5.5.1
- **PostgreSQL** 17  
- **Redis** 7.2  
- **Docker**  
- **Nginx**  
- **Git**  
- **psycopg2-binary**  
- **requests** 2.32  
- **social-auth-app-django** 5.7  
- **drf-spectacular** 0.29.0

## Testing
The project is covered with tests via Pytest to check the functionality of the API:
- API endpoints
- authentication / authorization
- registration
- filters
- permissions
- validation
- database operations


## Requirements
- Python 3.11 or higher  
- pip 23.2.1 or higher  
- Docker & Docker Compose

Dependencies are listed in `requirements.txt`. Install them with:

```bash
pip install -r requirements.txt
```

## Installation 
1. Install project from remote repository

```bash
git clone https://github.com/Lilkhan55/Library-Backend-API
cd Library-Backend-API
```

2. Start up docker-compose container with command

`docker-compose up -d`

All migrations and static files will be applied automatically.

3. Create superuser with command

`docker exec -it base-web-1 createsuperuser`

Usage
Access the site in your browser at http://localhost:8000 (or your configured domain).
