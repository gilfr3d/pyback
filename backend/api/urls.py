from django.urls import path, include
from .views import CreateUserView, AdminRegistrationView, CustomTokenObtainPairView, LogoutView, RefreshTokenView, CheckAuthView, AdminDashboardView, HRDashboardView, FinanceDashboardView

app_name = 'api'

urlpatterns = [
    path('user/register/', CreateUserView.as_view(), name='user_register'),
    path('admin/register/', AdminRegistrationView.as_view(), name='admin_register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh-cookie/', RefreshTokenView.as_view(), name='refresh_token_cookie'), 
    path('logout/', LogoutView.as_view(), name='logout'),
    path('auth-status/', CheckAuthView.as_view(), name='auth_status'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('hr-dashboard/', HRDashboardView.as_view(), name='hr_dashboard'), 
    path('finance-dashboard/', FinanceDashboardView.as_view(),name='finance_dashboard'),
]
