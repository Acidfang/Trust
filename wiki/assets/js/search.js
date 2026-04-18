// Search Functionality
(function() {
  SimpleJekyllSearch({
    searchInput: document.getElementById('search-input'),
    resultsContainer: document.getElementById('search-results'),
    json: '/cold-hard-truth/search.json',
    searchResultTemplate: '<li><a href="{url}">{title}</a></li>',
    noResultsText: 'No results found',
    limit: 10,
    fuzzy: true,
    exclude: ['Welcome']
  });
  
  // Highlight search results
  const searchInput = document.getElementById('search-input');
  searchInput.addEventListener('input', function() {
    const results = document.querySelectorAll('.search-results li');
    if (results.length > 0) {
      results[0].focus();
    }
  });
  
  // Close search results on click outside
  document.addEventListener('click', function(event) {
    const searchContainer = document.querySelector('.search-container');
    if (!searchContainer.contains(event.target)) {
      document.getElementById('search-results').innerHTML = '';
      searchInput.value = '';
    }
  });
})();
