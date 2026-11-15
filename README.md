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

## Phase 3 – Models

Two models in the `company` app, both registered in Django Admin:

| Model | Fields |
|---|---|
| `Department` | `name`, `created_at` |
| `Employee` | `name`, `email` (unique), `department`, `created_by`, `created_at` |

- `Employee.department` is a foreign key to `Department` (`related_name="employees"`, cascade delete).
- `Employee.created_by` is a foreign key to the custom user model (`settings.AUTH_USER_MODEL`, cascade delete).

Apply the migrations with `pipenv run python manage.py migrate`.

## Phase 4 – Serializers

Serializers for the `company` app are in `company/serializers.py` (no views or URLs yet):

- `DepartmentSerializer`: `id`, `name`, `created_at`.
- `EmployeeSerializer`: `id`, `name`, `email`, `department`, `department_name`, `created_by`, `created_at`.
  - `department` accepts a department id; `department_name` is read-only output.
  - `created_by` is read-only (it will be set from the logged-in user in a later phase).
  - `email` must be unique, compared case-insensitively. The email is stored as typed.

## Phase 5 – Views

Class-based generic views (`ListAPIView`, `CreateAPIView`, `RetrieveAPIView`, `UpdateAPIView`, `DestroyAPIView`), one class per operation. No ViewSets.

All endpoints are under `/api/` and require a JWT access token (`Authorization: Bearer <access token>`). This is set with `DEFAULT_PERMISSION_CLASSES = IsAuthenticated`; the register, login and refresh endpoints stay open.

| Method | Endpoint | Name | Description |
|---|---|---|---|
| GET | `/api/departments/` | `department_list` | List departments |
| POST | `/api/departments/create/` | `department_create` | Create a department |
| GET | `/api/departments/<id>/` | `department_detail` | Get one department |
| PUT, PATCH | `/api/departments/<id>/update/` | `department_update` | Update a department |
| DELETE | `/api/departments/<id>/delete/` | `department_delete` | Delete a department (also deletes its employees) |
| GET | `/api/employees/` | `employee_list` | List employees; filter with `?department=<id>` |
| POST | `/api/employees/create/` | `employee_create` | Create an employee (`created_by` is the logged-in user) |
| GET | `/api/employees/<id>/` | `employee_detail` | Get one employee |
| PUT, PATCH | `/api/employees/<id>/update/` | `employee_update` | Update an employee |
| DELETE | `/api/employees/<id>/delete/` | `employee_delete` | Delete an employee |

An invalid `?department=` value (not a number) returns `400`. Lists are not paginated.

## Project Structure

```
backend-training-tasks/
├── config/         # Project settings and URL configuration
├── company/        # Company app (Department and Employee models, serializers, views, URLs)
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
