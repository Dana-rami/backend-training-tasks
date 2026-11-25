from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Department, Employee
from .permissions import IsAdminOrReadOnly, IsSameDepartment, get_employee, is_admin
from .serializers import DepartmentSerializer, EmployeeSerializer

# Every view requires a logged-in user (DEFAULT_PERMISSION_CLASSES in settings.py)
# and also uses two custom permissions from permissions.py:
#   IsAdminOrReadOnly - admins can do anything, normal employees can only read.
#   IsSameDepartment  - a normal employee can only reach their own department
#                       (checked on a single object: detail, update, delete).
# Lists are filtered in get_queryset, because has_object_permission does not run
# on lists: a normal employee only sees their own department's data.
#
# The URL does not say what to do. The HTTP method decides:
#   collection URL (departments/):      GET = list,   POST = create
#   item URL       (departments/<id>/): GET = detail, PUT/PATCH = update, DELETE = delete
# One URL can only reach one view class, so each URL has one generic view
# that handles several methods. These are generic views, not ViewSets.


# ---------- Department ----------

class DepartmentListCreateAPIView(ListCreateAPIView):
    # GET -> list departments, POST -> create a department (admin only)
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrReadOnly, IsSameDepartment]

    def get_queryset(self):
        queryset = Department.objects.order_by('id')
        if not is_admin(self.request.user):
            # A normal employee only sees their own department.
            queryset = queryset.filter(pk=get_employee(self.request.user).department_id)
        return queryset


class DepartmentDetailAPIView(RetrieveUpdateDestroyAPIView):
    # GET -> detail, PUT/PATCH -> update, DELETE -> delete (update/delete: admin only)
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrReadOnly, IsSameDepartment]


# ---------- Employee ----------
# select_related('department') loads each employee's department in the same
# query, because the serializer reads department.name for every employee.

class EmployeeListCreateAPIView(ListCreateAPIView):
    # GET -> list employees (optionally ?department=<id>), POST -> create an employee (admin only)
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly, IsSameDepartment]

    def get_queryset(self):
        # get_queryset runs on every request, so it can depend on the request.
        # Here it narrows the list when the URL has ?department=<id>.
        queryset = Employee.objects.select_related('department').order_by('id')
        if not is_admin(self.request.user):
            # A normal employee only sees the employees of their own department.
            queryset = queryset.filter(department_id=get_employee(self.request.user).department_id)
        department = self.request.query_params.get('department')
        # An empty or missing ?department= means "no filter".
        if department:
            try:
                department_id = int(department)
            except ValueError:
                # A non-number would crash the query, so return a clean 400.
                raise ValidationError({'department': 'department must be an integer.'})
            queryset = queryset.filter(department_id=department_id)
        return queryset

    def perform_create(self, serializer):
        # Only runs for POST. created_by is read-only in the serializer, so the
        # client cannot send it. It is taken from the logged-in user (from the JWT).
        serializer.save(created_by=self.request.user)


class EmployeeDetailAPIView(RetrieveUpdateDestroyAPIView):
    # GET -> detail, PUT/PATCH -> update, DELETE -> delete (update/delete: admin only)
    queryset = Employee.objects.select_related('department')
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly, IsSameDepartment]
