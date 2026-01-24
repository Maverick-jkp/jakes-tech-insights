---
name: hugo-operations
description: Hugo static site operations including development server (with live reload), production builds (with minification), multilingual content preview (EN/KO/JA), and Cloudflare Pages deployment. Use when building the site, previewing content locally, or troubleshooting Hugo configuration issues. Critical - Hugo is installed at /opt/homebrew/bin/hugo (not in PATH).
---

# Hugo Operations Skill

Hugo static site generator operations for Jake's Tech Insights multilingual blog.

---

## When to Use This Skill

**Activate this skill when:**
- User requests "hugo", "build site", "preview", or "local server"
- Need to start development server for content preview
- Building site for production deployment
- Troubleshooting Hugo configuration or template issues
- Testing multilingual features (EN/KO/JA)

**Do NOT use this skill for:**
- Content creation → Use `content-generation` skill
- Quality validation → Use `quality-validation` skill
- Managing topic queue → Use `keyword-curation` skill

**Examples:**
- "Start Hugo development server"
- "Build site for production"
- "Preview latest posts"

---

## Skill Boundaries

**This skill handles:**
- ✅ Hugo development server (live reload, draft mode)
- ✅ Production builds (minification, optimization)
- ✅ Hugo configuration (hugo.toml)
- ✅ Template troubleshooting (layouts/)
- ✅ Multilingual site operations (EN/KO/JA)
- ✅ Build performance analysis

**Defer to other skills:**
- ❌ Content creation → Use `content-generation` skill
- ❌ Quality checks → Use `quality-validation` skill
- ❌ Topic management → Use `keyword-curation` skill
- ❌ Git/deployment → Master agent or CI/CD

---

## Quick Start

```bash
# Start development server (with drafts)
/opt/homebrew/bin/hugo server -D

# Production build
/opt/homebrew/bin/hugo --minify

# Check Hugo version
/opt/homebrew/bin/hugo version
```

**⚠️ CRITICAL**: Hugo is installed at `/opt/homebrew/bin/hugo` (not in PATH). Always use full path.

---

## Hugo Installation

### Current Installation

**Path**: `/opt/homebrew/bin/hugo`
**Version**: Extended (required for SCSS processing)
**Installed via**: Homebrew

### Verify Installation

```bash
# Check version
/opt/homebrew/bin/hugo version

# Check if extended
/opt/homebrew/bin/hugo version | grep extended
# Should show: hugo vX.XX.X+extended
```

### If Not Installed

```bash
# Install via Homebrew
brew install hugo

# Verify extended version
hugo version | grep extended
```

---

## Development Server

### Start Server

```bash
# Basic (with drafts)
/opt/homebrew/bin/hugo server -D

# With specific options
/opt/homebrew/bin/hugo server -D --bind 0.0.0.0 --baseURL http://192.168.1.100:1313

# With live reload disabled (rare)
/opt/homebrew/bin/hugo server -D --disableLiveReload
```

**Access**: http://localhost:1313

**Features**:
- ✅ Live reload (auto-refresh on file changes)
- ✅ Fast rebuild (milliseconds)
- ✅ Draft content visible (`-D` flag)
- ✅ Fast render mode

### Stop Server

Press `Ctrl+C` in terminal

### Common Server Options

| Flag | Purpose |
|------|---------|
| `-D` | Include draft content |
| `--bind 0.0.0.0` | Allow external access |
| `--port 8080` | Custom port |
| `--disableFastRender` | Full rebuild on changes |
| `--navigateToChanged` | Auto-navigate to changed page |

---

## Production Build

### Build Site

```bash
# Standard build
/opt/homebrew/bin/hugo --minify

# Check for errors
/opt/homebrew/bin/hugo --minify 2>&1 | grep -i error

# Build with debug info
/opt/homebrew/bin/hugo --minify --debug
```

**Output**: `public/` directory

**Process**:
1. Reads content from `content/`
2. Applies templates from `layouts/`
3. Processes assets (CSS/JS)
4. Generates HTML files
5. Minifies output (if `--minify`)

### Build Metrics

**Typical build**:
```
Total in 150 ms
Pages: 63
Resources: 15
Aliases: 3
```

**Performance**:
- < 200ms: Excellent ✅
- 200-500ms: Good ✅
- > 500ms: Investigate ⚠️

---

## Content Structure

### Directory Layout

```
content/
├── en/          # English posts
│   ├── tech/
│   ├── business/
│   ├── lifestyle/
│   ├── society/
│   ├── entertainment/
│   ├── sports/
│   ├── finance/
│   └── education/
├── ko/          # Korean posts (same structure)
└── ja/          # Japanese posts (same structure)
```

### Post Format

**File**: `content/en/tech/2026-01-23-ai-trends.md`

**Frontmatter** (YAML):
```yaml
---
title: "AI Trends 2026: What You Need to Know"
date: 2026-01-23T18:00:00+09:00
categories: ["tech"]
tags: ["AI", "trends", "2026"]
description: "Explore the latest AI trends shaping 2026, from generative models to autonomous systems and their real-world applications."
image: "https://images.unsplash.com/photo-..."
imageCredit: "Photo by [Name](https://unsplash.com/@username)"
lang: "en"
---

Content here...
```

**Required Fields**:
- `title` - Post title
- `date` - ISO 8601 with KST timezone (`+09:00`)
- `categories` - Array (8 valid categories)
- `tags` - Array (keywords)
- `description` - 120-160 chars (SEO)
- `image` - Unsplash URL
- `imageCredit` - Photo credit
- `lang` - `en`, `ko`, or `ja`

---

## Templates & Themes

### Theme

**Name**: PaperMod
**Location**: `themes/PaperMod/` (Git submodule)
**Version**: Customized

**⚠️ NEVER modify theme directly**

### Template Override

To customize, create matching file in `layouts/`:

```
themes/PaperMod/layouts/_default/single.html (theme)
    ↓ (override)
layouts/_default/single.html (project)
```

**Example**: Article page
```
layouts/_default/single.html    # Our customization
themes/PaperMod/layouts/_default/single.html  # Original (don't touch)
```

### Key Templates

| Template | Purpose | Location |
|----------|---------|----------|
| `index.html` | Homepage | `layouts/index.html` |
| `single.html` | Article page | `layouts/_default/single.html` |
| `list.html` | Category/list page | `layouts/categories/list.html` |
| `baseof.html` | Base template | `layouts/_default/baseof.html` |
| `head.html` | `<head>` section | `layouts/partials/head.html` |
| `footer.html` | Footer | `layouts/partials/footer.html` |

---

## Hugo Configuration

### File

**Location**: `hugo.toml`
**Format**: TOML

### Key Sections

**Languages**:
```toml
[languages.en]
  languageName = "English"
  weight = 1
  [languages.en.params]
    description = "AI-powered tech insights..."

[languages.ko]
  languageName = "한국어"
  weight = 2

[languages.ja]
  languageName = "日本語"
  weight = 3
```

**Menus** (for each language):
```toml
[[languages.en.menu.main]]
  name = "🔧 Tech"
  url = "/categories/tech/"
  weight = 1
```

**SEO Params**:
```toml
[params]
  description = "AI-powered multilingual tech blog"
  images = ["/og-image.png"]
  keywords = ["tech", "AI", "blog"]
```

### Update Configuration

```bash
# Edit hugo.toml
vim hugo.toml

# Test build
/opt/homebrew/bin/hugo --minify

# Check for errors
/opt/homebrew/bin/hugo --minify 2>&1 | grep -i error
```

---

## Common Build Issues

### Issue 1: Hugo Not Found

**Error**: `hugo: command not found`

**Cause**: Hugo not in PATH

**Fix**: Use full path
```bash
/opt/homebrew/bin/hugo server -D
```

**Or add to PATH** (`~/.zshrc` or `~/.bashrc`):
```bash
export PATH="/opt/homebrew/bin:$PATH"
```

### Issue 2: Template Not Found

**Error**: `WARN: found no layout file for "HTML" for kind "page"`

**Cause**: Missing template

**Fix**: Check template exists
```bash
ls -la layouts/_default/
ls -la themes/PaperMod/layouts/_default/
```

### Issue 3: Failed to Render

**Error**: `Error: error building site: failed to render pages`

**Cause**: Invalid YAML frontmatter

**Fix**: Validate YAML
```bash
python -c "
import yaml
from pathlib import Path
for f in Path('content/en/tech').glob('*.md'):
    with open(f) as file:
        content = file.read()
        if '---' in content:
            frontmatter = content.split('---')[1]
            try:
                yaml.safe_load(frontmatter)
            except Exception as e:
                print(f'❌ {f}: {e}')
"
```

### Issue 4: Slow Build

**Symptom**: Build takes > 500ms

**Causes**:
- Too many posts (> 1000)
- Large images not optimized
- Complex templates

**Fix**:
```bash
# Debug slow build
/opt/homebrew/bin/hugo --debug --templateMetrics

# Check which templates are slow
# Look for "rendering" times > 50ms
```

---

## Multilingual Features

### Language Switcher

**Location**: `layouts/partials/header.html`

**Implementation**:
```html
<div class="lang-switch">
  {{ range .Site.Languages }}
    <a href="{{ .Permalink }}">{{ .LanguageName }}</a>
  {{ end }}
</div>
```

### Hreflang Tags

**Location**: `layouts/partials/head.html`

**SEO for multilingual**:
```html
{{ range .Translations }}
<link rel="alternate" hreflang="{{ .Language.Lang }}" href="{{ .Permalink }}" />
{{ end }}
```

### Per-language Configuration

Each language has separate:
- Menus
- Params (description, keywords)
- Content directories (`content/en/`, `content/ko/`, `content/ja/`)

---

## Deployment

### Cloudflare Pages

**URL**: https://jakes-tech-insights.pages.dev

**Build Command**: `hugo --minify`
**Output Directory**: `public`
**Branch**: `main`

**Process**:
1. Push to `main` branch
2. Cloudflare detects commit
3. Runs `hugo --minify`
4. Deploys `public/` to CDN
5. Live in ~30 seconds

### Manual Deploy Test

```bash
# Build locally
/opt/homebrew/bin/hugo --minify

# Check output
ls -la public/

# Test index.html
cat public/index.html | head -20
```

---

## Performance Optimization

### Images

**Auto-optimized** via Unsplash API:
- Responsive sizes
- WebP format (when supported)
- CDN delivery
- Lazy loading

**Manual optimization** (if needed):
```bash
# Resize image
convert input.jpg -resize 1200x output.jpg

# Convert to WebP
cwebp -q 80 input.jpg -o output.webp
```

### CSS/JS

**Minification**: Enabled via `--minify` flag

**Bundle size**: Check with
```bash
du -sh public/css/
du -sh public/js/
```

**Target**:
- CSS: < 100KB
- JS: < 50KB

### Caching

**Static assets**: Cached by Cloudflare CDN
- CSS/JS: 1 year
- Images: 1 year
- HTML: 1 hour

---

## Testing

### Test 1: Local Build

```bash
# Clean build
rm -rf public/
/opt/homebrew/bin/hugo --minify

# Verify pages
ls -la public/en/tech/
ls -la public/ko/tech/
ls -la public/ja/tech/
```

### Test 2: Development Server

```bash
# Start server
/opt/homebrew/bin/hugo server -D

# Check homepage
curl http://localhost:1313 | grep "<title>"

# Check post
curl http://localhost:1313/en/tech/2026-01-23-ai-trends/ | grep "<title>"
```

### Test 3: Mobile Preview

```bash
# Start with external access
/opt/homebrew/bin/hugo server -D --bind 0.0.0.0

# Access from mobile device
# http://<your-local-ip>:1313
```

### Test 4: Lighthouse

```bash
# Install Lighthouse CLI (if needed)
npm install -g lighthouse

# Run audit (need deployed site)
lighthouse https://jakes-tech-insights.pages.dev --view
```

**Targets**:
- Performance: > 90
- Accessibility: > 90
- Best Practices: > 90
- SEO: > 90

---

## Troubleshooting

### Debug Mode

```bash
# Enable verbose logging
/opt/homebrew/bin/hugo --debug --verbose

# Template metrics
/opt/homebrew/bin/hugo --templateMetrics
```

### Clear Cache

```bash
# Remove resources cache
rm -rf resources/_gen/

# Full rebuild
rm -rf public/ resources/
/opt/homebrew/bin/hugo --minify
```

### Check Dependencies

```bash
# Verify theme submodule
git submodule status

# Update theme (if needed)
git submodule update --init --recursive
```

---

## Related Skills

- **content-generation**: Generate posts (then preview with Hugo)
- **quality-validation**: Validate before building
- **keyword-curation**: Manage topics

---

## References

- **Hugo Docs**: https://gohugo.io/documentation/
- **PaperMod Theme**: https://github.com/adityatelange/hugo-PaperMod
- **Architecture**: `.claude/docs/architecture.md`
- **Troubleshooting**: `.claude/docs/troubleshooting.md`

---

**Skill Version**: 1.0
**Last Updated**: 2026-01-23
**Maintained By**: Jake's Tech Insights project
