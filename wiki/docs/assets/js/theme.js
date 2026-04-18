// Dark Mode Toggle
(function() {
  const toggle = document.getElementById('dark-mode-toggle');
  const html = document.documentElement;
  const body = document.body;
  
  // Check for saved theme preference or default to light mode
  const savedTheme = localStorage.getItem('theme') || 'light-mode';
  body.className = savedTheme;
  updateToggleIcon(savedTheme);
  
  // Theme toggle event listener
  toggle.addEventListener('click', function() {
    const currentTheme = body.className;
    const newTheme = currentTheme === 'light-mode' ? 'dark-mode' : 'light-mode';
    
    body.className = newTheme;
    localStorage.setItem('theme', newTheme);
    updateToggleIcon(newTheme);
  });
  
  function updateToggleIcon(theme) {
    const icon = toggle.querySelector('.theme-icon');
    icon.textContent = theme === 'dark-mode' ? '☀️' : '🌙';
  }
})();
