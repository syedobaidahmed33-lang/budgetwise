/**
 * transaction_filter.js
 * Option B — Advanced JavaScript Interactivity: Live Client-Side Search
 *
 * Filters the transaction table in real time as the user types into the
 * #txn-search input. No page reload or server request is made — all
 * filtering happens entirely on the client using the data already rendered
 * in the HTML table rows by Django templates.
 *
 * Event used: 'input' (fires on every keystroke, satisfying the assignment
 * requirement for an event type beyond 'click').
 *
 * Matching logic:
 *   - Case-insensitive
 *   - Checks the transaction description AND category fields
 *   - Rows are shown/hidden by toggling their CSS display property
 *
 * Limitation (documented): If server-side pagination is added later, this
 * filter will only search the rows currently rendered on the page, not all
 * records. A fetch-based approach would be needed at that point.
 */

(function () {
  'use strict';

  // Grab DOM references once — avoids repeated querySelector calls on each keystroke
  const searchInput = document.getElementById('txn-search');
  const tbody       = document.getElementById('txn-tbody');
  const noResults   = document.getElementById('no-results');
  const searchCount = document.getElementById('search-count');

  // If the search input or table body doesn't exist, bail out silently
  // (guards against this script being loaded on a page without the table)
  if (!searchInput || !tbody) return;

  // Cache all data rows at initialisation time for fast iteration
  // NodeList → Array so we can use .filter() on it later
  const allRows = Array.from(tbody.querySelectorAll('tr'));

  /**
   * filterRows — called on every 'input' event.
   *
   * Reads the current value of the search box, trims whitespace,
   * converts to lowercase, then iterates over every cached row and
   * decides whether to show or hide it based on whether the query
   * appears in the description or category data attributes.
   *
   * @param {Event} event — the input event from the search field
   */
  function filterRows(event) {
    const query = event.target.value.trim().toLowerCase();
    let visibleCount = 0;

    allRows.forEach(function (row) {
      // Read the pre-lowercased data attributes set in transactions.html
      const description = row.querySelector('[data-description]')
                          ?.getAttribute('data-description') || '';
      const category    = row.querySelector('[data-category]')
                          ?.getAttribute('data-category') || '';

      // Show the row if either field contains the query string
      const matches = description.includes(query) || category.includes(query);
      row.style.display = matches ? '' : 'none';
      if (matches) visibleCount++;
    });

    // Update the result count label below the search input
    if (query.length > 0) {
      searchCount.textContent = `Showing ${visibleCount} of ${allRows.length} transactions`;
    } else {
      searchCount.textContent = '';
    }

    // Show or hide the "no results" message
    noResults.style.display = (visibleCount === 0 && query.length > 0) ? 'block' : 'none';
  }

  // Attach the listener — 'input' fires on every keystroke (including paste,
  // backspace, etc.) giving the user instant feedback as they type
  searchInput.addEventListener('input', filterRows);

})();
