# Expense Tracker API

Short Django REST API for tracking user expenses.

## Requirements
- Python 3.10+
- MySQL (or adjust DATABASES in settings)
- see requirements.txt

## Setup
1. Create and activate virtualenv:
   - python3 -m venv venv
   - source venv/bin/activate
2. Install deps:
   - pip install -r requirements.txt
3. Copy env and update DB values:
   - cp .env.example .env
4. Run migrations and create superuser:
   - python manage.py migrate
   - python manage.py createsuperuser
5. Run server:
   - python manage.py runserver

## Env variables (from .env.example)
- DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
