from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('employee/logout/', views.employee_logout, name='employee_logout'),
    path('employee-register/', views.employee_register, name='employee_register'),
    path('admin/add/', views.add_employee, name='add_employee'),
    path('admin/edit/<int:id>/', views.edit_employee, name='edit_employee'),
    path('admin/delete/<int:id>/', views.delete_employee, name='delete_employee'),
    path('admin/approve-leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('admin/reject-leave/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    path('employee-login-search/', views.employee_login_search, name='employee_login_search'), 
    path('employee-profile-dashboard/', views.employee_profile_dashboard, name='employee_profile_dashboard'),
    path('submit-leave/', views.submit_leave_request, name='submit_leave_request'),
]
