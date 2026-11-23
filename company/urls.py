from django.urls import path

from .views import (
    DepartmentDetailAPIView,
    DepartmentListCreateAPIView,
    EmployeeDetailAPIView,
    EmployeeListCreateAPIView,
)

# The HTTP method decides the action, so the paths have no create/update/delete.
urlpatterns = [
    # Departments
    path('departments/', DepartmentListCreateAPIView.as_view(), name='department_list'),
    path('departments/<int:pk>/', DepartmentDetailAPIView.as_view(), name='department_detail'),
    # Employees
    path('employees/', EmployeeListCreateAPIView.as_view(), name='employee_list'),
    path('employees/<int:pk>/', EmployeeDetailAPIView.as_view(), name='employee_detail'),
]
