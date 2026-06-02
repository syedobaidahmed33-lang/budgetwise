from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('transactions/delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),

    # Option C — Data Visualization API endpoint
    # Called by Chart.js in dashboard.html on every page load
    path('api/monthly-summary/', views.monthly_summary_api, name='monthly_summary_api'),
]
