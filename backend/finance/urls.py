from django.urls import path
from . import views

urlpatterns = [
    # Employee Salary URLs
    path('employee-salaries/', views.EmployeeSalaryListCreateView.as_view(), name='employee_salary_list'),
    path('employee-salaries/<int:pk>/', views.EmployeeSalaryDetailView.as_view(), name='employee_salary_detail'),

    # Expense URLs
    path('expenses/', views.ExpenseListCreateView.as_view(), name='expense_list'),
    path('expenses/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense_detail'),

    # Income URLs
    path('incomes/', views.IncomeListCreateView.as_view(), name='income_list'),
    path('incomes/<int:pk>/', views.IncomeDetailView.as_view(), name='income_detail'),

    # Invoice URLs
    path('invoices/', views.InvoiceListCreateView.as_view(), name='invoice_list'),
    path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
]
