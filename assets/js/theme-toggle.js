// Dark/Light Mode Toggle
(function() {
    // Get theme from localStorage or default to 'dark'
    const getTheme = () => localStorage.getItem('theme') || 'dark';

    // Apply theme to document
    const applyTheme = (theme) => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);

        // Update toggle button icon
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.textContent = theme === 'dark' ? '☀️' : '🌙';
            toggleBtn.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
        }
    };

    // Initialize theme on page load (before DOM ready to prevent flash)
    applyTheme(getTheme());

    // Toggle theme function (called by button)
    window.toggleTheme = () => {
        const currentTheme = getTheme();
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(newTheme);
    };

    // Re-apply on DOM ready to ensure button icon is correct
    document.addEventListener('DOMContentLoaded', () => {
        applyTheme(getTheme());
    });
})();
