"""
tests.py — BudgetWise Test Suite
Run with: python manage.py test

Covers:
  - Transaction model method
  - Dashboard view HTTP status
  - Authentication-gated views (authenticated vs unauthenticated)
  - The /api/monthly-summary/ JsonResponse endpoint data shape
"""

import json
import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Transaction


# ─────────────────────────────────────────────────────────────────────────────
class TransactionModelTest(TestCase):
    """Tests for Transaction model methods and properties."""

    def setUp(self):
        # Create a test user and two sample transactions
        self.user = User.objects.create_user(username='tester', password='pass123')
        self.expense = Transaction.objects.create(
            user=self.user,
            description='Groceries run',
            amount=75.50,
            category='groceries',
            is_income=False,
            date=datetime.date.today(),
        )
        self.income = Transaction.objects.create(
            user=self.user,
            description='Freelance payment',
            amount=500.00,
            category='income',
            is_income=True,
            date=datetime.date.today(),
        )

    def test_signed_amount_negative_for_expense(self):
        """signed_amount() should return a negative value for expense transactions."""
        self.assertEqual(self.expense.signed_amount(), -75.50)

    def test_signed_amount_positive_for_income(self):
        """signed_amount() should return a positive value for income transactions."""
        self.assertEqual(self.income.signed_amount(), 500.00)

    def test_str_representation(self):
        """__str__ should include the date, category, and amount."""
        result = str(self.expense)
        self.assertIn('groceries', result)
        self.assertIn('75.50', result)


# ─────────────────────────────────────────────────────────────────────────────
class DashboardViewTest(TestCase):
    """Tests for the main dashboard view — HTTP status and authentication."""

    def setUp(self):
        self.user = User.objects.create_user(username='dashuser', password='pass123')
        self.client = Client()

    def test_dashboard_returns_200_when_authenticated(self):
        """Authenticated users should get a 200 response from the dashboard."""
        self.client.login(username='dashuser', password='pass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_redirects_unauthenticated_user(self):
        """Unauthenticated users should be redirected away from the dashboard."""
        response = self.client.get(reverse('dashboard'))
        # Should redirect (302) not return 200
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)

    def test_dashboard_uses_correct_template(self):
        """Dashboard should render using dashboard.html."""
        self.client.login(username='dashuser', password='pass123')
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(response, 'tracker/dashboard.html')


# ─────────────────────────────────────────────────────────────────────────────
class MonthlySummaryAPITest(TestCase):
    """
    Tests for the /api/monthly-summary/ endpoint (Option C — Data Visualization).
    Verifies JSON shape, correct aggregation, and authentication requirement.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='apiuser', password='pass123')
        self.client = Client()
        today = datetime.date.today()

        # Add two expenses in different categories for the current month
        Transaction.objects.create(
            user=self.user, description='Rent', amount=800.00,
            category='rent', is_income=False, date=today,
        )
        Transaction.objects.create(
            user=self.user, description='Groceries', amount=120.50,
            category='groceries', is_income=False, date=today,
        )
        # Add an income transaction — should NOT appear in the expense chart
        Transaction.objects.create(
            user=self.user, description='Salary', amount=2000.00,
            category='income', is_income=True, date=today,
        )

    def test_api_returns_200_for_authenticated_user(self):
        """The API endpoint should return 200 for a logged-in user."""
        self.client.login(username='apiuser', password='pass123')
        response = self.client.get(reverse('monthly_summary_api'))
        self.assertEqual(response.status_code, 200)

    def test_api_requires_authentication(self):
        """The API endpoint should redirect unauthenticated requests."""
        response = self.client.get(reverse('monthly_summary_api'))
        self.assertNotEqual(response.status_code, 200)

    def test_api_response_has_correct_keys(self):
        """Response JSON must contain 'labels' and 'data' keys (shape Chart.js expects)."""
        self.client.login(username='apiuser', password='pass123')
        response = self.client.get(reverse('monthly_summary_api'))
        data = json.loads(response.content)
        self.assertIn('labels', data)
        self.assertIn('data', data)

    def test_api_excludes_income_from_chart(self):
        """Income transactions must not appear in the spending chart data."""
        self.client.login(username='apiuser', password='pass123')
        response = self.client.get(reverse('monthly_summary_api'))
        data = json.loads(response.content)
        # 'Income' category should not be in the labels returned for the expense chart
        self.assertNotIn('Income', data['labels'])

    def test_api_returns_correct_number_of_categories(self):
        """There should be exactly 2 expense categories in the response."""
        self.client.login(username='apiuser', password='pass123')
        response = self.client.get(reverse('monthly_summary_api'))
        data = json.loads(response.content)
        self.assertEqual(len(data['labels']), 2)
        self.assertEqual(len(data['data']), 2)
