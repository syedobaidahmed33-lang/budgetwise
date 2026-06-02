# BudgetWise

A personal finance tracker built with Django and vanilla JavaScript. Users can register, log in, and manage income and expense transactions organized by category. The dashboard displays monthly totals and a spending breakdown chart.

## Tech Stack

- **Back end:** Django 4.2, SQLite
- **Front end:** Bootstrap 5, vanilla JavaScript, Chart.js (CDN)
- **Auth:** Django built-in authentication

## Setup

```bash
# 1. Clone the repo and enter the project folder
git clone <your-repo-url>
cd budgetwise

# 2. Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Run migrations and create a superuser
python manage.py migrate
python manage.py createsuperuser

# 4. Start the development server
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and log in.

## Running Tests

```bash
python manage.py test
```

All 8 tests should pass.

---

## Lesson 14 Enhancements

### Option C — Data Visualization (Spending Chart)

**Why I chose it:** The app already collects spending data by category but had no way to visualize it. A chart turns raw numbers into an instant insight — the core value of any budgeting tool.

**What you can do now that you couldn't before:** Open the dashboard and see your monthly expenses broken down in an interactive doughnut chart. Hover over a slice to see the exact dollar amount. Add a new expense, refresh the dashboard, and the chart updates automatically.

**New files created / modified:**
- `tracker/views.py` — added `monthly_summary_api()` view (the Django JSON endpoint)
- `tracker/urls.py` — wired `/api/monthly-summary/` to the new view
- `tracker/templates/tracker/dashboard.html` — added `<canvas>` element and the Chart.js fetch/render script block

**New dependency:** Chart.js 4.4 loaded via CDN (no `pip install` needed).

**How to see it working:**
1. Log in and go to `/dashboard/`
2. The doughnut chart renders automatically on page load
3. To see the raw JSON the chart uses, open `/api/monthly-summary/` in your browser while logged in

---

### Option B — Advanced JavaScript Interactivity (Live Search Filter)

**Why I chose it:** With more than a handful of transactions, finding a specific one meant scrolling through the entire list. The live filter makes the app feel instant and usable.

**What you can do now that you couldn't before:** On the Transactions page, type any word into the search box and the table filters in real time — no page reload, no server request. The result count updates as you type, and a "no results" message appears if nothing matches.

**New files created / modified:**
- `tracker/static/tracker/js/transaction_filter.js` — all filtering logic (new file)
- `tracker/templates/tracker/transactions.html` — added the `<input id="txn-search">` field, `data-description` / `data-category` attributes on table cells, and the `<script>` tag loading the JS file

**No new dependencies** — pure vanilla JavaScript, no libraries.

**How to see it working:**
1. Add several transactions with different categories (e.g. Groceries, Rent, Entertainment)
2. Go to `/transactions/`
3. Type "gro" in the search box — only Groceries rows appear instantly
4. Clear the box — all rows reappear

**Event used:** `input` (fires on every keystroke — not `click`)

---

### Notes

- Both enhancements work together with the existing feature set — no regressions introduced
- Every new function and endpoint has inline comments explaining what it does
- The JS filter has a documented limitation: if server-side pagination is added later, the filter would only search the current page
