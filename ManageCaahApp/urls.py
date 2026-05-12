from django.urls import path
from ManageCaahApp.views import *

urlpatterns = [
   
    path('', register_page, name='register_page' ),
    path('login_page/', login_page, name='login_page' ),
    path('dashboard/', dashboard, name='dashboard' ),
    path('logout_page/', logout_page, name='logout_page' ),
    path('profile_update/', profile_update, name='profile_update' ),
    path('cash_list/', cash_list, name='cash_list' ),
    path('add_cash/', add_cash, name='add_cash' ),
    path('update_cash/<str:id>/', update_cash, name='update_cash' ),
    path('delete_cash/<str:id>/', delete_cash, name='delete_cash' ),
    path('expense_list/', expense_list, name='expense_list' ),
    path('add_expense/', add_expense, name='add_expense' ),
    path('update_expense/<str:id>/', update_expense, name='update_expense' ),
    path('delete_expense/<str:id>/', delete_expense, name='delete_expense' ),
]
