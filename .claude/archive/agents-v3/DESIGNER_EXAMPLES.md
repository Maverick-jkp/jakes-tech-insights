# Designer Agent - Examples

This file contains detailed examples for Designer agent work patterns.

## Example 1: Blog Post Layout Improvement

```
User: "Blog posts are hard to read"

Designer Analysis:
1. Current issues
   - Line length too long (100+ characters)
   - Line spacing too tight (line-height 1.4)
   - Font size too small (14px)
   - Insufficient margins

2. Improvement plan
   - Optimal line length: 60-80 characters (max-width: 65ch)
   - Line spacing: 1.6-1.8
   - Font size: 16px (body text)
   - Increase padding

3. Implementation
   - Modify layouts/_default/single.html
   - Add assets/css/blog-post.css
   - Define typography scale

Action:
- Create feature/improve-post-readability branch
- Modify CSS and templates
- Test on multiple posts
```

**Design Proposal**:
```markdown
## Design Proposal: Post Readability

### Current Status
- Issue: Poor reading experience
- User impact: Difficult to read long articles
- Screenshot: [Current state]

### Proposed Design

**Concept**: Reader-friendly typography

**Key Changes**:
1. Line Length
   - Before: 100+ characters per line
   - After: 60-80 characters (max-width: 65ch)
   - Reason: Optimal reading comfort

2. Line Spacing
   - Before: line-height 1.4
   - After: line-height 1.7
   - Reason: Better text breathing room

3. Font Size
   - Before: 14px
   - After: 16px
   - Reason: More readable on all devices

**Technical Implementation**:
- Modified files: layouts/_default/single.html, assets/css/typography.css
- Added resources: None
- Browser compatibility: All modern browsers

**Performance Impact**:
- Bundle size increase: 0.5KB
- Loading time impact: Negligible
```

**Implementation**:
```css
/* assets/css/blog-post.css */
.post-content {
  max-width: 65ch; /* 60-80 character line length */
  margin: 0 auto;
  padding: 2rem 1.5rem;
  font-size: 16px;
  line-height: 1.7;
  color: var(--color-text);
}

.post-content h2 {
  margin-top: 2.5rem;
  margin-bottom: 1rem;
  font-size: 1.75rem;
  font-weight: 600;
  line-height: 1.3;
}

.post-content p {
  margin-bottom: 1.5rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .post-content {
    font-size: 15px;
    padding: 1.5rem 1rem;
  }
}
```

**Validation Results**:
```markdown
### Responsive Testing
- ✓ Mobile (375px, 414px)
- ✓ Tablet (768px, 1024px)
- ✓ Desktop (1440px, 1920px)

### Accessibility Check
- Color contrast: 7.2:1 (AAA compliant)
- Keyboard navigation: Pass
- Screen reader: Pass

### Performance Check
- Lighthouse score: 96/100
- FCP: 0.8s
- CLS: 0.05
```

---

## Example 2: Dark Mode Implementation

```
User: "Add dark mode"

Designer Work:
1. Define color palette
   Light mode:
   - Background: #ffffff
   - Text: #1a1a1a
   - Accent: #0066cc

   Dark mode:
   - Background: #1a1a1a
   - Text: #e5e5e5
   - Accent: #4d9fff

2. CSS variable structure
   :root {
     --color-bg: #ffffff;
     --color-text: #1a1a1a;
   }

   @media (prefers-color-scheme: dark) {
     :root {
       --color-bg: #1a1a1a;
       --color-text: #e5e5e5;
     }
   }

3. Theme toggle implementation
   - localStorage persistence
   - Respect system preference
   - Toggle button in header

Action:
- Create feature/dark-mode branch
- Refactor CSS variables
- Add JavaScript toggle logic
- Verify accessibility (color contrast)
```

**Color Palette**:
```css
/* Light Mode (Default) */
:root {
  /* Background Colors */
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f5f5f5;
  --color-bg-tertiary: #e5e5e5;

  /* Text Colors */
  --color-text-primary: #1a1a1a;
  --color-text-secondary: #4a4a4a;
  --color-text-tertiary: #757575;

  /* Accent Colors */
  --color-accent: #0066cc;
  --color-accent-hover: #0052a3;

  /* Border Colors */
  --color-border: #d1d1d1;
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  :root {
    /* Background Colors */
    --color-bg-primary: #1a1a1a;
    --color-bg-secondary: #2a2a2a;
    --color-bg-tertiary: #3a3a3a;

    /* Text Colors */
    --color-text-primary: #e5e5e5;
    --color-text-secondary: #b5b5b5;
    --color-text-tertiary: #8a8a8a;

    /* Accent Colors */
    --color-accent: #4d9fff;
    --color-accent-hover: #6baeff;

    /* Border Colors */
    --color-border: #3a3a3a;
  }
}

/* Manual Toggle (when user clicks toggle button) */
[data-theme="dark"] {
  --color-bg-primary: #1a1a1a;
  --color-bg-secondary: #2a2a2a;
  /* ... rest of dark colors ... */
}
```

**Theme Toggle JavaScript**:
```javascript
// assets/js/theme-toggle.js
(function() {
  const STORAGE_KEY = 'theme-preference';

  // Get saved preference or system preference
  const getTheme = () => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) return saved;

    return window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  };

  // Apply theme
  const applyTheme = (theme) => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
  };

  // Toggle theme
  const toggleTheme = () => {
    const current = getTheme();
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
  };

  // Initialize on page load
  applyTheme(getTheme());

  // Expose toggle function
  window.toggleTheme = toggleTheme;
})();
```

**Accessibility Verification**:
```markdown
### Color Contrast Ratios (WCAG AA requires 4.5:1)

**Light Mode**:
- Primary text on primary bg: 12.6:1 (Pass AAA)
- Secondary text on primary bg: 7.8:1 (Pass AAA)
- Accent on primary bg: 6.2:1 (Pass AAA)

**Dark Mode**:
- Primary text on primary bg: 11.4:1 (Pass AAA)
- Secondary text on primary bg: 6.9:1 (Pass AAA)
- Accent on primary bg: 5.8:1 (Pass AAA)

### Testing Checklist
- ✓ All text readable in both modes
- ✓ Focus indicators visible
- ✓ Images have proper contrast
- ✓ Toggle button accessible via keyboard
- ✓ Screen reader announces theme change
```

---

## Example 3: Responsive Navigation Menu

```
User: "Navigation menu breaks on mobile"

Designer Analysis:
1. Current issues
   - Horizontal menu overflows on small screens
   - No hamburger menu for mobile
   - Touch targets too small (<44px)

2. Solution
   - Desktop: Horizontal navigation (>768px)
   - Mobile: Hamburger menu (<768px)
   - Touch targets: 44x44px minimum

3. Implementation
   - Add hamburger icon
   - Add mobile menu overlay
   - Add smooth animations
   - Ensure keyboard accessibility

Action:
- Create feature/responsive-nav branch
- Modify header partial
- Add mobile menu styles
- Test on actual devices
```

**Mobile Menu Implementation**:
```html
<!-- layouts/partials/header.html -->
<header class="site-header">
  <div class="header-container">
    <a href="/" class="site-logo">My Site</a>

    <!-- Hamburger Button (Mobile only) -->
    <button
      class="menu-toggle"
      aria-label="Toggle menu"
      aria-expanded="false"
      aria-controls="nav-menu"
    >
      <span class="hamburger"></span>
    </button>

    <!-- Navigation Menu -->
    <nav class="nav-menu" id="nav-menu">
      <ul class="nav-list">
        <li><a href="/about/">About</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/contact/">Contact</a></li>
      </ul>
    </nav>
  </div>
</header>
```

```css
/* Mobile-first approach */
.site-header {
  padding: 1rem;
  background: var(--color-bg-primary);
  border-bottom: 1px solid var(--color-border);
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

/* Hamburger Menu (Mobile) */
.menu-toggle {
  display: block;
  width: 44px;
  height: 44px;
  padding: 0;
  border: none;
  background: transparent;
  cursor: pointer;
}

.hamburger {
  display: block;
  width: 24px;
  height: 2px;
  background: var(--color-text-primary);
  position: relative;
  transition: background 0.3s;
}

.hamburger::before,
.hamburger::after {
  content: '';
  position: absolute;
  width: 24px;
  height: 2px;
  background: var(--color-text-primary);
  transition: transform 0.3s;
}

.hamburger::before { top: -8px; }
.hamburger::after { top: 8px; }

/* Animated hamburger to X */
.menu-toggle[aria-expanded="true"] .hamburger {
  background: transparent;
}

.menu-toggle[aria-expanded="true"] .hamburger::before {
  transform: rotate(45deg) translate(6px, 6px);
}

.menu-toggle[aria-expanded="true"] .hamburger::after {
  transform: rotate(-45deg) translate(6px, -6px);
}

/* Mobile Menu */
.nav-menu {
  position: fixed;
  top: 0;
  right: -100%;
  width: 80%;
  max-width: 320px;
  height: 100vh;
  background: var(--color-bg-primary);
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  transition: right 0.3s ease-in-out;
  z-index: 1000;
}

.nav-menu.is-open {
  right: 0;
}

.nav-list {
  list-style: none;
  padding: 4rem 2rem;
  margin: 0;
}

.nav-list li {
  margin-bottom: 1.5rem;
}

.nav-list a {
  display: block;
  padding: 0.75rem 0;
  font-size: 1.125rem;
  color: var(--color-text-primary);
  text-decoration: none;
  min-height: 44px; /* Touch target */
}

/* Desktop (Tablet and up) */
@media (min-width: 768px) {
  .menu-toggle {
    display: none; /* Hide hamburger */
  }

  .nav-menu {
    position: static;
    width: auto;
    height: auto;
    background: transparent;
    box-shadow: none;
  }

  .nav-list {
    display: flex;
    padding: 0;
  }

  .nav-list li {
    margin: 0 1rem;
  }

  .nav-list a {
    padding: 0.5rem 1rem;
  }
}
```

**JavaScript Toggle**:
```javascript
// Mobile menu toggle
const menuToggle = document.querySelector('.menu-toggle');
const navMenu = document.querySelector('.nav-menu');

menuToggle.addEventListener('click', () => {
  const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';

  menuToggle.setAttribute('aria-expanded', !isExpanded);
  navMenu.classList.toggle('is-open');
});

// Close menu when clicking outside
document.addEventListener('click', (e) => {
  if (!menuToggle.contains(e.target) && !navMenu.contains(e.target)) {
    menuToggle.setAttribute('aria-expanded', 'false');
    navMenu.classList.remove('is-open');
  }
});

// Close menu on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && navMenu.classList.contains('is-open')) {
    menuToggle.setAttribute('aria-expanded', 'false');
    navMenu.classList.remove('is-open');
    menuToggle.focus(); // Return focus
  }
});
```

---

## Example 4: Image Gallery Optimization

```
User: "Image gallery loads slowly"

Designer Work:
1. Current issues
   - All images load immediately (no lazy loading)
   - Large file sizes (PNG, not WebP)
   - No responsive images (srcset)
   - CLS (layout shift) during load

2. Optimization plan
   - Convert to WebP format
   - Add lazy loading
   - Implement responsive images
   - Specify width/height to prevent CLS

3. Implementation
   - Hugo image processing
   - Picture element with WebP fallback
   - Native lazy loading
   - Aspect ratio placeholder

Action:
- Create feature/optimize-gallery branch
- Update image partial
- Test on slow connection (3G throttle)
```

**Optimized Image Component**:
```html
<!-- layouts/partials/responsive-image.html -->
{{ $image := .Page.Resources.GetMatch (.Get "src") }}
{{ $alt := .Get "alt" }}
{{ $width := .Get "width" | default "800" }}
{{ $height := .Get "height" | default "600" }}

{{ if $image }}
  {{ $webp := $image.Resize (printf "%dx%d webp" $width $height) }}
  {{ $fallback := $image.Resize (printf "%dx%d" $width $height) }}
  {{ $small := $image.Resize (printf "%dx%d webp" (div $width 2) (div $height 2)) }}

  <picture>
    <!-- WebP format with srcset -->
    <source
      type="image/webp"
      srcset="{{ $small.RelPermalink }} 400w,
              {{ $webp.RelPermalink }} 800w"
      sizes="(max-width: 768px) 100vw, 800px"
    />

    <!-- Fallback format -->
    <img
      src="{{ $fallback.RelPermalink }}"
      alt="{{ $alt }}"
      width="{{ $width }}"
      height="{{ $height }}"
      loading="lazy"
      decoding="async"
      style="aspect-ratio: {{ $width }} / {{ $height }};"
    />
  </picture>
{{ end }}
```

**Usage**:
```markdown
<!-- In content files -->
{{< responsive-image src="gallery-01.jpg" alt="Gallery image" width="800" height="600" >}}
```

**Performance Results**:
```markdown
### Before Optimization
- Image format: PNG
- Total size: 3.2MB (8 images)
- Loading time (3G): 12.4s
- CLS: 0.32

### After Optimization
- Image format: WebP with JPEG fallback
- Total size: 480KB (8 images) - 85% reduction
- Loading time (3G): 2.1s - 83% faster
- CLS: 0.02 - 93% improvement

### Lighthouse Scores
- Performance: 94 → 98
- Best Practices: 92 → 100
```

---

**Last Updated**: 2026-01-20
**Related**: [DESIGNER.md](DESIGNER.md)
