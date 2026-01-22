# Technology Stack

**Project**: Jake's Tech Insights
**Last Updated**: 2026-01-20

---

## Core Technologies

### Static Site Generator
- **Hugo v0.121.1**
  - Multilingual support (EN/KO/JA)
  - Fast build times (<1s)
  - Content management via markdown

### Theme & Design
- **PaperMod Theme** (Git Submodule)
  - Base structure only
  - Heavily customized layouts
- **Custom CSS**
  - Vanilla CSS with CSS Variables
  - Dark cyberpunk theme
  - Bento grid layout

### Deployment & Hosting
- **Cloudflare Pages**
  - Automatic deployment on git push
  - Global CDN
  - Free SSL
  - Build command: `hugo --cleanDestinationDir`
  - Deploy URL: https://jakes-tech-insights.pages.dev

---

## Design System

### Typography
- **Headings/Logo**: Space Mono (monospace)
- **Body Text**: Instrument Sans (sans-serif)

### Color Palette (Dark Theme)
```css
--bg: #1a1a1a;           /* Background */
--surface: #242424;      /* Card background */
--border: #333333;       /* Borders */
--text: #f5f5f5;         /* Primary text */
--text-dim: #b0b0b0;     /* Dimmed text (WCAG AA compliant) */
--accent: #00ff88;       /* Neon green accent */
```

### Animations
- Grid background animation
- Hover effects on cards
- Smooth transitions

---

## Multilingual Support

### Hugo Configuration
```toml
[languages]
  [languages.en]
    languageName = "English"
    languageCode = "en-us"
    weight = 1
    contentDir = "content/en"

  [languages.ko]
    languageName = "한국어"
    languageCode = "ko-kr"
    weight = 2
    contentDir = "content/ko"

  [languages.ja]
    languageName = "日本語"
    languageCode = "ja-jp"
    weight = 3
    contentDir = "content/ja"
```

### URL Structure
- EN (default): `/tech/`, `/business/`, `/lifestyle/`
- KO: `/ko/tech/`, `/ko/business/`, `/ko/lifestyle/`
- JA: `/ja/tech/`, `/ja/business/`, `/ja/lifestyle/`

### Date Localization
- EN: January 16, 2025
- KO: 2025년 01월 16일
- JA: 2025年01月16日

---

## Development Tools

### Local Development
```bash
# Hugo binary path (platform-specific)
# MacOS: /opt/homebrew/bin/hugo
# Windows: Check instructions.md

# Start dev server
hugo server -D

# Build for production
hugo --cleanDestinationDir
```

### Version Control
- **Git**: Source control
- **GitHub**: Repository hosting
- **.gitignore**: Excludes `public/`, `.hugo_build.lock`, `resources/_gen/`

---

## Future Considerations

### Potential Additions
- **Analytics**: Google Analytics 4
- **Search**: Algolia or Lunr.js
- **Comments**: Disqus or Utterances
- **CDN Optimization**: Image optimization via Cloudflare

### Not Currently Used
- ❌ JavaScript frameworks (Vue/React)
- ❌ CSS preprocessors (SASS/LESS)
- ❌ Build tools (Webpack/Vite)
- ✅ Keeping it simple: Hugo only

---

## References

- [Hugo Documentation](https://gohugo.io/documentation/)
- [Hugo Multilingual](https://gohugo.io/content-management/multilingual/)
- [PaperMod Theme](https://github.com/adityatelange/hugo-PaperMod)
- [Cloudflare Pages](https://developers.cloudflare.com/pages/)
