from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'description', 'amount', 'category', 'is_income', 'date']
    list_filter = ['category', 'is_income', 'date']
