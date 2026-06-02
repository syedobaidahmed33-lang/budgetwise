from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from django.utils import timezone
from .models import Transaction, CATEGORY_CHOICES
from .forms import TransactionForm
import datetime


@login_required
def dashboard(request):
    """
    Main dashboard view — shows recent transactions and monthly totals.
    The spending chart (Option C) is rendered on this page using data
    from the /api/monthly-summary/ endpoint fetched by Chart.js on load.
    """
    today = timezone.now().date()
    month_start = today.replace(day=1)

    # Get transactions for the current month
    monthly_txns = Transaction.objects.filter(
        user=request.user,
        date__gte=month_start,
        date__lte=today
    )

    # Calculate totals for the summary cards
    total_income = monthly_txns.filter(is_income=True).aggregate(
        total=Sum('amount'))['total'] or 0
    total_expenses = monthly_txns.filter(is_income=False).aggregate(
        total=Sum('amount'))['total'] or 0
    balance = total_income - total_expenses

    # Most recent 5 transactions for the dashboard preview list
    recent = Transaction.objects.filter(user=request.user)[:5]

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'recent': recent,
        'current_month': today.strftime('%B %Y'),
    }
    return render(request, 'tracker/dashboard.html', context)


# ─── Option C: Data Visualization ────────────────────────────────────────────

@login_required
def monthly_summary_api(request):
    """
    API endpoint for the Chart.js spending chart (Option C — Data Visualization).
    Returns JSON with category labels and their total expense amounts for the
    current month. Called by chart.js in dashboard.html on every page load,
    so the chart always reflects current database state (not hardcoded).

    Example response:
        {"labels": ["Groceries", "Rent"], "data": [120.50, 800.00]}
    """
    today = timezone.now().date()
    month_start = today.replace(day=1)

    # Aggregate expense totals grouped by category for this month
    category_totals = (
        Transaction.objects
        .filter(user=request.user, date__gte=month_start, is_income=False)
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    # Build label/data arrays that Chart.js expects
    labels = []
    data = []
    for row in category_totals:
        # Convert the raw category key (e.g. 'groceries') to its display name
        display = dict(CATEGORY_CHOICES).get(row['category'], row['category'].title())
        labels.append(display)
        data.append(float(row['total']))

    return JsonResponse({'labels': labels, 'data': data})


# ─── Transactions (core feature) ─────────────────────────────────────────────

@login_required
def transactions(request):
    """
    Transaction list page. The client-side search filter (Option B) runs here —
    the full list is rendered server-side, then filtered in the browser by
    static/tracker/js/transaction_filter.js without any page reload.
    """
    txns = Transaction.objects.filter(user=request.user)
    return render(request, 'tracker/transactions.html', {'transactions': txns})


@login_required
def add_transaction(request):
    """Handle the add-transaction form submission."""
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            txn = form.save(commit=False)
            txn.user = request.user
            txn.save()
            messages.success(request, 'Transaction added.')
            return redirect('transactions')
    else:
        form = TransactionForm()
    return render(request, 'tracker/add_transaction.html', {'form': form})


@login_required
def delete_transaction(request, pk):
    """Delete a transaction owned by the current user."""
    txn = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        txn.delete()
        messages.success(request, 'Transaction deleted.')
    return redirect('transactions')
