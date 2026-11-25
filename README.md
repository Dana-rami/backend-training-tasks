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

Class-based generic views (`ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`). No ViewSets.

The URL does not say what to do; the HTTP method decides. The collection URL handles list and create, and the item URL handles detail, update and delete.

All endpoints are under `/api/` and require a JWT access token (`Authorization: Bearer <access token>`). This is set with `DEFAULT_PERMISSION_CLASSES = IsAuthenticated`; the register, login and refresh endpoints stay open.

| Method | Endpoint | Name | Description |
|---|---|---|---|
| GET | `/api/departments/` | `department_list` | List departments |
| POST | `/api/departments/` | `department_list` | Create a department |
| GET | `/api/departments/<id>/` | `department_detail` | Get one department |
| PUT, PATCH | `/api/departments/<id>/` | `department_detail` | Update a department |
| DELETE | `/api/departments/<id>/` | `department_detail` | Delete a department (also deletes its employees) |
| GET | `/api/employees/` | `employee_list` | List employees; filter with `?department=<id>` |
| POST | `/api/employees/` | `employee_list` | Create an employee (`created_by` is the logged-in user) |
| GET | `/api/employees/<id>/` | `employee_detail` | Get one employee |
| PUT, PATCH | `/api/employees/<id>/` | `employee_detail` | Update an employee |
| DELETE | `/api/employees/<id>/` | `employee_detail` | Delete an employee |

An invalid `?department=` value (not a number) returns `400`. Lists are not paginated.

## Phase 6 – URLs

All routes are written by hand in `company/urls.py` (mounted under `/api/` in `config/urls.py`), one explicit `path()` per view. No router is used.

- **URL design:** Paths use lowercase, dash-separated, plural nouns (`departments/`, `employees/`). An item is addressed by its id with `<int:pk>/`. URL names are snake_case (`department_list`, `employee_detail`, ...), so code can use `reverse('employee_detail', kwargs={'pk': 1})` instead of hard-coded paths.
- **The HTTP method decides the action:** The URL names the resource, not the operation, so there are no `create/`, `update/` or `delete/` parts. `departments/` and `employees/` handle `GET` (list) and `POST` (create); `<int:pk>/` handles `GET` (detail), `PUT`/`PATCH` (update) and `DELETE` (delete).
- **Two views per model:** A URL can only point to one view class, so the list and create operations share one generic view (`ListCreateAPIView`) and detail, update and delete share another (`RetrieveUpdateDestroyAPIView`). That gives four `path()` entries in total.
- **Why no router:** A router builds URLs from a ViewSet automatically. This project uses generic views, not ViewSets, and writing the URLs by hand keeps every endpoint visible in one file and easy to read and debug.

## Phase 7 – Permissions

Every endpoint requires a JWT (`IsAuthenticated` is the default). On top of that, `company/permissions.py` adds roles and department checks.

**User ↔ Employee.** An employee is a person who logs in, so `Employee.user` links an employee to a login account (`OneToOneField`, optional, so employees created before this phase still work). `Employee.role` is `admin` or `employee` (default `employee`). Superusers are always admins.

| Role | What they can do |
|---|---|
| Admin (`role=admin` or superuser) | Everything: view, create, update, delete, on all departments and employees |
| Employee (`role=employee`) | View only, and only their own department and its employees |
| Logged-in user with no employee profile | Nothing (`403`) |

**How it is enforced**

- `IsAdminOrReadOnly`: role check. Normal employees may only use `GET`, `HEAD` and `OPTIONS`.
- `IsSameDepartment`: department check on a single object. Opening another department (or one of its employees) returns `403`.
- Lists are filtered in `get_queryset`, so a normal employee only sees their own department's data.
- `created_by` is still set from the logged-in user. The admin sets `user` and `role` when creating an employee.

**Migrations.** The new fields are in a new migration (`company/0002_employee_user_role.py`). The first migration was not edited.

**First admin.** Create a superuser with `createsuperuser` (it is an admin without an employee profile). It can then create employees and link them to users with `user` and `role`. `POST /api/auth/register/` still only creates a user, so register first, then an admin links that user to an employee.

## Phase 8 – Middleware

Two middleware classes in `config/middleware.py`, registered first in `MIDDLEWARE`:

- `RequestIDMiddleware`: gives every request an ID. It keeps the client's `X-Request-ID` header if it is a normal value (letters, digits, `.`, `_`, `-`, up to 64 characters), otherwise it creates a UUID. The ID is stored on `request.request_id` and sent back in the `X-Request-ID` response header.
- `RequestLoggingMiddleware`: logs one line per request with the request ID, method, path, status code and time, using the `requests` logger (console, configured in `LOGGING`).

Example log line: `[0326075e...] POST /api/auth/login/ -> 200 (284.2 ms)`

**Request lifecycle.** A request goes down the `MIDDLEWARE` list (top to bottom) to the view, and the response goes back up in the reverse order. Each middleware wraps the next one through `get_response`. Order matters: the ID middleware is first so the ID already exists when the logging middleware runs, and the logging middleware sees the final status code of everything below it.

## Project Structure

```
backend-training-tasks/
├── config/         # Project settings, URL configuration and middleware
├── company/        # Company app (models, serializers, views, URLs, permissions)
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
