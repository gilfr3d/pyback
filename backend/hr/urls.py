from django.urls import path
from .views import DepartmentListView, EmployeeListView, LeaveListView

urlpatterns = [
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('leaves/', LeaveListView.as_view(), name='leave_list'),
]
