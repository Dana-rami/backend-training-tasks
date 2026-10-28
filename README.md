# Backend Training Tasks

A Django project built as part of backend training.

## Phase 1 – Project Setup

Completed in this phase:

- Created the Django project (`config`)
- Created the `company` app
- Created the `accounts` app (empty for now; reserved for the custom user model and authentication code)
- Installed Django, Django REST Framework and Simple JWT, managed with Pipenv
- Applied database migrations (SQLite)
- Created a superuser
- Verified that the development server runs and Django Admin is accessible

## Project Structure

```
backend-training-tasks/
├── config/       # Project settings and URL configuration
├── company/      # Company app
├── accounts/     # Accounts app
├── manage.py
├── Pipfile
└── Pipfile.lock
```

## Getting Started

Requires Python 3.12 and [Pipenv](https://pipenv.pypa.io/).

```bash
# Install dependencies from Pipfile.lock
pipenv install

# Apply migrations
pipenv run python manage.py migrate

# Create a superuser
pipenv run python manage.py createsuperuser

# Run the development server
pipenv run python manage.py runserver
```

Django Admin is available at <http://127.0.0.1:8000/admin/>.
