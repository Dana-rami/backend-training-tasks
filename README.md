# Django Backend Training Tasks

A Django project built as part of backend training.

## Phase 1 – Project Setup

Completed in this phase:

- Created the Django project (`config`)
- Created the `company` app
- Installed Django REST Framework and Simple JWT
- Applied database migrations (SQLite)
- Created a superuser
- Verified that the development server runs and Django Admin is accessible

## Project Structure

```
backend-training-tasks/
├── config/     # Project settings and URL configuration
├── company/    # Company app
└── manage.py
```

## Getting Started

```bash
# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows

# Install dependencies
pip install django djangorestframework djangorestframework-simplejwt

# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

Django Admin is available at <http://127.0.0.1:8000/admin/>.
