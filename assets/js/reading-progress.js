// Reading Progress Bar
(function() {
    document.addEventListener('DOMContentLoaded', () => {
        const progressBar = document.getElementById('reading-progress-bar');
        if (!progressBar) return;

        const updateProgress = () => {
            // Get scroll position
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;
            const scrollTop = window.scrollY || document.documentElement.scrollTop;

            // Calculate progress (0-100%)
            const maxScroll = documentHeight - windowHeight;
            const progress = maxScroll > 0 ? (scrollTop / maxScroll) * 100 : 0;

            // Update progress bar width
            progressBar.style.width = `${Math.min(progress, 100)}%`;
        };

        // Update on scroll with throttling for performance
        let ticking = false;
        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    updateProgress();
                    ticking = false;
                });
                ticking = true;
            }
        });

        // Initial update
        updateProgress();
    });
})();
