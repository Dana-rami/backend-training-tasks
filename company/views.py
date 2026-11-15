from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer

# All views require a logged-in user. This comes from DEFAULT_PERMISSION_CLASSES
# in settings.py, so permission_classes is not repeated on each view.


# ---------- Department ----------

class DepartmentListAPIView(ListAPIView):
    queryset = Department.objects.order_by('id')
    serializer_class = DepartmentSerializer


class DepartmentCreateAPIView(CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentDetailAPIView(RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentUpdateAPIView(UpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentDeleteAPIView(DestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


# ---------- Employee ----------
# select_related('department') loads each employee's department in the same
# query, because the serializer reads department.name for every employee.

class EmployeeListAPIView(ListAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        # get_queryset runs on every request, so it can depend on the request.
        # Here it narrows the list when the URL has ?department=<id>.
        queryset = Employee.objects.select_related('department').order_by('id')
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


class EmployeeCreateAPIView(CreateAPIView):
    queryset = Employee.objects.select_related('department')
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        # created_by is read-only in the serializer, so the client cannot send it.
        # It is taken from the logged-in user (from the JWT) when saving.
        serializer.save(created_by=self.request.user)


class EmployeeDetailAPIView(RetrieveAPIView):
    queryset = Employee.objects.select_related('department')
    serializer_class = EmployeeSerializer


class EmployeeUpdateAPIView(UpdateAPIView):
    queryset = Employee.objects.select_related('department')
    serializer_class = EmployeeSerializer


class EmployeeDeleteAPIView(DestroyAPIView):
    queryset = Employee.objects.select_related('department')
    serializer_class = EmployeeSerializer
