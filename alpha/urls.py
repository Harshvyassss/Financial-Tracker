from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.home, name='home'),
    path('add-income/', views.add_income, name='add_income'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('income-list/', views.income_list, name='income_list'),
    path('expense-list/', views.expense_list, name='expense_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('income/edit/<int:pk>/', views.edit_income, name='edit_income'),
    path('income/delete/<int:pk>/', views.delete_income, name='delete_income'),
    path('expense/edit/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('expense/delete/<int:pk>/', views.delete_expense, name='delete_expense'),
]
