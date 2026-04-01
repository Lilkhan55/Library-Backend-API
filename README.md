# Library-project-on-Django

![PyPI - Version](https://img.shields.io/pypi/v/django?label=django)
![Python](https://img.shields.io/pypi/pyversions/Django.svg?label=Python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-✓-green)
![Redis](https://img.shields.io/badge/Redis-✓-red)
![SSL](https://img.shields.io/badge/SSL-secured-brightgreen)

## Library Project 
This project is built using the Django framework. The idea behind my project is that you can view information about a book on the website, get a PDF file, and get a physical copy from a library (at the conceptual level).
The site has registration and authorization, including OAuth authentication. You can add new books if you are part of the moderator group. Users can rent and return books on the site.

You can view the site at this [link](www.pushkinlibrary.site)

## Tech Stack
- **Python** 3.11  
- **Django** 5.2  
- **PostgreSQL** 17  
- **Redis** 7.2  
- **Docker**  
- **Nginx**  
- **Git**  
- **psycopg2-binary**  
- **requests** 2.32  
- **social-auth-app-django** 5.7  

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
git clone https://github.com/Lilkhan55/Library-project-on-Django
cd Library-project-on-Django
```

2. Start up docker-compose container with command

`docker-compose up -d`

All migrations and static files will be applied automatically.

3. Create superuser with command

`docker exec -it base-web-1 createsuperuser`

Usage
Access the site in your browser at http://localhost:8000 (or your configured domain).
Register as a user or login with OAuth.
Moderators can add books, manage rentals, and handle returns.
