from django.urls import path

from .views import (
    DepartmentCreateAPIView,
    DepartmentDeleteAPIView,
    DepartmentDetailAPIView,
    DepartmentListAPIView,
    DepartmentUpdateAPIView,
    EmployeeCreateAPIView,
    EmployeeDeleteAPIView,
    EmployeeDetailAPIView,
    EmployeeListAPIView,
    EmployeeUpdateAPIView,
)

urlpatterns = [
    # Departments
    path('departments/', DepartmentListAPIView.as_view(), name='department_list'),
    path('departments/create/', DepartmentCreateAPIView.as_view(), name='department_create'),
    path('departments/<int:pk>/', DepartmentDetailAPIView.as_view(), name='department_detail'),
    path('departments/<int:pk>/update/', DepartmentUpdateAPIView.as_view(), name='department_update'),
    path('departments/<int:pk>/delete/', DepartmentDeleteAPIView.as_view(), name='department_delete'),
    # Employees
    path('employees/', EmployeeListAPIView.as_view(), name='employee_list'),
    path('employees/create/', EmployeeCreateAPIView.as_view(), name='employee_create'),
    path('employees/<int:pk>/', EmployeeDetailAPIView.as_view(), name='employee_detail'),
    path('employees/<int:pk>/update/', EmployeeUpdateAPIView.as_view(), name='employee_update'),
    path('employees/<int:pk>/delete/', EmployeeDeleteAPIView.as_view(), name='employee_delete'),
]
