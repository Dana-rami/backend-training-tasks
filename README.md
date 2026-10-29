# Backend Training Tasks

A Django project built as part of backend training.

## Phase 1 – Project Setup

Completed in this phase:

- Created the Django project (`config`)
- Created the `company` app
- Created the `accounts` app
- Installed Django, Django REST Framework and Simple JWT, managed with Pipenv
- Applied database migrations (SQLite at the time; replaced by PostgreSQL in Phase 2)
- Created a superuser
- Verified that the development server runs and Django Admin is accessible

## Phase 2 – Authentication (JWT)

Endpoints (all `POST`, under `/api/auth/`):

| Endpoint | Description |
|---|---|
| `/api/auth/register/` | Create a user (`username`, `email`, `password`, optional `phone_number`) |
| `/api/auth/login/` | Obtain an access and refresh token (`username`, `password`) |
| `/api/auth/refresh/` | Get a new access token (`refresh`) |

Login and refresh use Simple JWT's `TokenObtainPairView` and `TokenRefreshView`.

### Custom user model

`accounts.User` extends Django's `AbstractUser` and adds an optional `phone_number` field (max 20 characters). It is set as `AUTH_USER_MODEL` and registered in Django Admin.

### Database (PostgreSQL)

The project uses PostgreSQL. The connection is configured with a single `DATABASE_URL` read from a `.env` file by [django-environ](https://django-environ.readthedocs.io/). The `.env` file is not tracked by git.

1. Create an empty PostgreSQL database named `backend_training_django`.
2. Copy `.env.example` to `.env` and fill in your values:

   ```
   DATABASE_URL=postgres://postgres:your_password_here@localhost:5432/backend_training_django
   ```

   The format is `postgres://USER:PASSWORD@HOST:PORT/DATABASE_NAME`. If the password contains special characters such as `@`, `#`, `/` or `:`, percent-encode them (for example `@` becomes `%40`).

## Project Structure

```
backend-training-tasks/
├── config/         # Project settings and URL configuration
├── company/        # Company app
├── accounts/       # Accounts app (custom user model, registration and JWT auth URLs)
├── manage.py
├── .env.example    # Template for database settings
├── Pipfile
└── Pipfile.lock
```

## Getting Started

Requires Python 3.12, [Pipenv](https://pipenv.pypa.io/) and PostgreSQL. Set up `.env` as described above first.

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
