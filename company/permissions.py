from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Department, Employee


def get_employee(user):
    """Return the Employee linked to this user, or None if there is none."""
    # user.employee_profile is the reverse side of Employee.user.
    # It raises when no Employee is linked, so we catch that and return None.
    try:
        return user.employee_profile
    except Employee.DoesNotExist:
        return None


def is_admin(user):
    """Superusers and employees with the admin role are admins."""
    if user.is_superuser:
        return True
    employee = get_employee(user)
    return employee is not None and employee.role == Employee.Role.ADMIN


class IsAdminOrReadOnly(BasePermission):
    """
    Role check (runs before the view).
    - Admins can do everything.
    - Normal employees can only use safe methods (GET, HEAD, OPTIONS).
    - A logged-in user with no Employee profile (and not an admin) gets nothing.
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if is_admin(user):
            return True
        if get_employee(user) is None:
            return False
        return request.method in SAFE_METHODS


class IsSameDepartment(BasePermission):
    """
    Department check (runs on single objects: detail, update, delete).
    Admins can reach any department. A normal employee can only reach their own
    department and the employees who belong to it.
    """

    def has_object_permission(self, request, view, obj):
        if is_admin(request.user):
            return True
        employee = get_employee(request.user)
        if employee is None:
            return False
        # A Department object is the department itself, an Employee has department_id.
        department_id = obj.pk if isinstance(obj, Department) else obj.department_id
        return department_id == employee.department_id
