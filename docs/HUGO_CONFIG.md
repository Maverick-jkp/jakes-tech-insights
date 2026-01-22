# Hugo Configuration Guide

## Overview

Jake's Tech Insights uses Hugo with the PaperMod theme, configured for multilingual content generation across English, Korean, and Japanese. This document explains the key configuration decisions and settings.

## hugo.toml Configuration

### Base Settings

```toml
baseURL = 'https://jakes-tech-insights.pages.dev/'
languageCode = 'en-us'
title = "Jake's Tech Insights"
theme = 'PaperMod'
```

**Key Points:**
- `baseURL`: Cloudflare Pages deployment URL
- `languageCode`: Default language (English)
- `title`: Site-wide title (used in metadata)
- `theme`: PaperMod theme from themes directory

### Timezone Configuration

```toml
timeZone = 'Asia/Seoul'
```

**Purpose:**
- Ensures post dates are interpreted correctly in KST (Korea Standard Time)
- Prevents "future post" issues on Cloudflare Pages deployment
- All posts include timezone in frontmatter: `date: 2026-01-17T12:00:00+09:00`

**Why This Matters:**
Without timezone configuration, Hugo and Cloudflare may interpret dates differently:
- Local dev: Assumes system timezone
- Cloudflare: Assumes UTC
- Result: Posts appear as "future posts" and are hidden

**Solution:**
- Set `timeZone = 'Asia/Seoul'` in hugo.toml
- Include `+09:00` in all post date fields
- Ensures consistent interpretation across environments

## Language Configuration

### Multilingual Support

Hugo is configured for three languages with separate content directories:

```
content/
├── en/     # English posts
├── ko/     # Korean posts (한국어)
└── ja/     # Japanese posts (日本語)
```

### Language Settings

```toml
[languages.en]
languageName = "English"
weight = 1
contentDir = "content/en"

[languages.ko]
languageName = "한국어"
weight = 2
contentDir = "content/ko"

[languages.ja]
languageName = "日本語"
weight = 3
contentDir = "content/ja"
```

**Weight Ordering:**
- Weight determines language menu order
- Lower weight appears first (EN → KO → JA)

**Content Directory Separation:**
- Each language has isolated content directory
- Prevents cross-language file conflicts
- Simplifies automated content generation
- Enables language-specific organization

### URL Structure

**Default Hugo Behavior:**
```
/posts/my-article/      # English
/ko/posts/my-article/   # Korean
/ja/posts/my-article/   # Japanese
```

**Current Implementation:**
```
/tech/my-article/       # Category-based
/ko/tech/my-article/    # Korean with category
/ja/tech/my-article/    # Japanese with category
```

## Taxonomy Configuration

### Categories (Primary Taxonomy)

Categories are the main content organization method:

```yaml
categories:
  - tech
  - business
  - society
  - entertainment
  - lifestyle
```

**Category Pages:**
- `/categories/tech/` - Lists all tech posts
- `/ko/categories/tech/` - Korean tech posts
- `/ja/categories/tech/` - Japanese tech posts

**Why Category-Based:**
1. **Clear Content Segmentation**: Easy for users to browse by topic
2. **SEO Benefits**: Category pages rank for broader keywords
3. **Navigation Simplicity**: 5 clear sections vs. dozens of tags
4. **Automated Classification**: AI can reliably assign categories
5. **URL Structure**: Clean, predictable URLs

### Tags (Removed)

**Previous Implementation:**
- Tags were included in post frontmatter
- Generated tag archive pages
- Created complex taxonomy structure

**Why Tags Were Removed:**

1. **Redundancy**: Tags overlapped with categories
2. **AI Limitations**: AI-generated tags were inconsistent
3. **SEO Dilution**: Too many thin tag pages hurt rankings
4. **User Confusion**: Multiple navigation paths to same content
5. **Maintenance Burden**: Required tag curation and cleanup

**Decision:**
Focus on 5 well-defined categories instead of 50+ unpredictable tags.

### Frontmatter Requirements

**Minimal Required Fields:**

```yaml
---
title: "Article Title (50-60 chars for SEO)"
date: 2026-01-17T12:00:00+09:00
draft: false
categories: ["tech"]
description: "Meta description (120-160 chars)"
---
```

**Field Explanations:**

- `title`: SEO-optimized title (50-60 characters ideal)
- `date`: ISO 8601 format with timezone (`+09:00` for KST)
- `draft`: Must be `false` for production visibility
- `categories`: Array with single category (from 5 options)
- `description`: Meta description for search engines (120-160 chars)

**Optional Fields:**

```yaml
author: "Jake Park"
image: "/images/post-thumbnail.jpg"
keywords: ["keyword1", "keyword2"]
```

## Content Directory Structure

### Why Separate contentDir?

**Rationale for `contentDir` Separation:**

1. **Language Isolation**: Each language maintains independent file structure
2. **Automated Generation**: Scripts target specific language directories
3. **Deployment Simplicity**: No complex multilingual file matching
4. **Git Conflict Prevention**: Team members can work on different languages
5. **Backup/Migration**: Easy to extract one language's content

**Alternative (Not Used):**
```
content/
└── posts/
    ├── my-article.en.md
    ├── my-article.ko.md
    └── my-article.ja.md
```

**Why Not This Approach:**
- Requires complex file matching logic
- AI generation scripts need to handle .LANG.md naming
- Git conflicts when generating same topic in multiple languages
- Harder to isolate language-specific issues

### Directory Organization

**Current Structure:**
```
content/
├── en/
│   ├── tech/
│   │   └── 2026-01-17-article-title.md
│   ├── business/
│   ├── society/
│   ├── entertainment/
│   └── lifestyle/
├── ko/
│   ├── tech/
│   ├── business/
│   └── ...
└── ja/
    ├── tech/
    ├── business/
    └── ...
```

**Benefits:**
- Clear visual separation of languages and categories
- Easy to locate specific posts
- Predictable file paths for automated scripts
- Simplified backup and migration

## PaperMod Theme Configuration

### Theme Integration

```toml
theme = 'PaperMod'
```

**Installation:**
```bash
git submodule add https://github.com/adityatelange/hugo-PaperMod themes/PaperMod
git submodule update --init --recursive
```

**Customizations:**
- Custom layouts in `layouts/` directory (override theme defaults)
- Custom CSS in `assets/css/extended/custom.css`
- Custom homepage: `layouts/index.html`
- Custom category pages: `layouts/categories/list.html`

### Layout Override Priority

Hugo layout resolution order:
1. `layouts/` (project root) - **Highest priority**
2. `themes/PaperMod/layouts/` - Theme defaults
3. Hugo built-in layouts

**Custom Layouts:**
- `layouts/index.html` - Homepage Bento grid
- `layouts/categories/list.html` - Category landing pages
- `layouts/_default/all-posts.html` - All posts listing
- `layouts/_default/single.html` - Individual post pages

## Server and Build Commands

### Development Server

```bash
# Standard server (draft posts hidden)
hugo server

# Show draft posts
hugo server -D

# Custom Hugo binary location
~/hugo_bin server -D
```

### Production Build

```bash
# Build for production
hugo

# Build with drafts (testing)
hugo -D

# Output directory: public/
```

### Cloudflare Pages Deployment

**Build Settings:**
- Build command: `hugo`
- Build output directory: `public`
- Environment variable: `HUGO_VERSION = 0.120.0` (or latest)

**Automatic Deployment:**
- Push to `main` branch triggers build
- Deployment time: 2-3 minutes
- URL: https://jakes-tech-insights.pages.dev/

## Configuration Best Practices

### Date Handling

**Always Include Timezone:**
```yaml
# Good
date: 2026-01-17T12:00:00+09:00

# Bad (timezone ambiguity)
date: 2026-01-17
date: 2026-01-17T12:00:00
```

### Category Naming

**Use Lowercase Slugs:**
```yaml
# Good
categories: ["tech"]

# Bad (inconsistent casing)
categories: ["Tech"]
categories: ["TECH"]
```

### Draft Management

**Production Posts:**
```yaml
draft: false  # Visible on production
```

**Testing Posts:**
```yaml
draft: true   # Hidden unless hugo -D
```

## Troubleshooting

### Issue: Posts Not Showing on Production

**Symptoms:**
- Posts visible locally with `hugo server`
- Missing on Cloudflare deployment

**Causes:**
1. Missing timezone in date field
2. `draft: true` in frontmatter
3. Future date (ahead of server time)

**Solution:**
1. Add `+09:00` to all post dates
2. Set `draft: false`
3. Verify date is not in the future (UTC or KST)

### Issue: Language Switcher Not Working

**Cause:**
- Missing language configuration in hugo.toml
- Incorrect `contentDir` paths

**Solution:**
- Verify all three languages defined in `[languages.XX]` sections
- Check `contentDir` points to correct directories

### Issue: Custom Layouts Not Applied

**Cause:**
- Layout files in wrong directory
- Incorrect naming convention

**Solution:**
- Place layouts in `layouts/` not `themes/PaperMod/layouts/`
- Use correct naming: `index.html`, `single.html`, `list.html`

## References

- Hugo Documentation: https://gohugo.io/documentation/
- PaperMod Theme: https://github.com/adityatelange/hugo-PaperMod
- Hugo Multilingual: https://gohugo.io/content-management/multilingual/
- Hugo Taxonomies: https://gohugo.io/content-management/taxonomies/
