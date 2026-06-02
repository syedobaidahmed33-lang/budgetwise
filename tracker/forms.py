from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    """Form for adding a new transaction."""
    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'category', 'is_income', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.TextInput(attrs={'placeholder': 'e.g. Monthly rent payment'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
