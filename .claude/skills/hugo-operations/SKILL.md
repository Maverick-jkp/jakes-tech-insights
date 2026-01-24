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

## Dependencies

**Required system packages:**
- `hugo` (Extended version 0.120.0+) - Static site generator
  - **Location**: `/opt/homebrew/bin/hugo`
  - **⚠️ CRITICAL**: Hugo is NOT in PATH, always use full path

**Required Python packages:**
- `pyyaml==6.0` - YAML frontmatter validation (if running validation scripts)

**Installation:**
```bash
# Hugo (macOS with Homebrew)
brew install hugo

# Python packages
pip install -r requirements.txt
```

**Verification:**
```bash
/opt/homebrew/bin/hugo version
# Expected: hugo v0.120.0+ extended
```

**Note**: This skill does NOT require Claude API (no API costs).

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

## Development Server

### Start Server

```bash
# Basic (with drafts)
/opt/homebrew/bin/hugo server -D

# With specific options
/opt/homebrew/bin/hugo server -D --bind 0.0.0.0 --baseURL http://192.168.1.100:1313
```

**Access**: http://localhost:1313

**Features**:
- ✅ Live reload (auto-refresh on file changes)
- ✅ Fast rebuild (milliseconds)
- ✅ Draft content visible (`-D` flag)

### Common Server Options

| Flag | Purpose |
|------|---------|
| `-D` | Include draft content |
| `--bind 0.0.0.0` | Allow external access |
| `--port 8080` | Custom port |
| `--disableFastRender` | Full rebuild on changes |

---

## Production Build

```bash
# Standard build
/opt/homebrew/bin/hugo --minify

# Check for errors
/opt/homebrew/bin/hugo --minify 2>&1 | grep -i error
```

**Output**: `public/` directory

**Typical build**:
```
Total in 150 ms
Pages: 63
```

---

## Content Structure

```
content/
├── en/          # English posts
│   ├── tech/, business/, lifestyle/, etc.
├── ko/          # Korean posts (same structure)
└── ja/          # Japanese posts (same structure)
```

**Post format**: `content/en/tech/2026-01-23-ai-trends.md`

---

## Common Issues

### Issue 1: Hugo Not Found

**Error**: `hugo: command not found`

**Fix**: Use full path
```bash
/opt/homebrew/bin/hugo server -D
```

### Issue 2: Build Errors

**Error**: `Error: error building site`

**Fix**: Check frontmatter YAML syntax
```bash
# Validate YAML in posts
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

---

## Deployment

**Platform**: Cloudflare Pages
**URL**: https://jakeinsight.com
**Build Command**: `hugo --minify`
**Output Directory**: `public`

**Process**:
1. Push to `main` branch
2. Cloudflare detects commit
3. Runs `hugo --minify`
4. Deploys to CDN (~30 seconds)

---

## Advanced Topics

For detailed information, see:
- **Configuration**: `resources/configuration.md` - Hugo settings, menus, multilingual
- **Templates**: `resources/templates.md` - Theme customization, layouts
- **Troubleshooting**: `resources/troubleshooting.md` - Detailed error solutions
- **Performance**: `resources/performance.md` - Optimization techniques

---

## Testing

```bash
# Test local build
rm -rf public/
/opt/homebrew/bin/hugo --minify

# Verify pages
ls -la public/en/tech/
ls -la public/ko/tech/
ls -la public/ja/tech/
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

---

**Skill Version**: 1.2
**Last Updated**: 2026-01-24
**Maintained By**: Jake's Tech Insights project
