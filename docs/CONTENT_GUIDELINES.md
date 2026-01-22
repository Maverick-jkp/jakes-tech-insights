# Content Guidelines

**Project**: Jake's Tech Insights
**Last Updated**: 2026-01-20

---

## Content Structure Rules

### CRITICAL: Category-Based Structure

**⚠️ ALL posts MUST be placed in one of 3 categories:**

✅ **Allowed**:
- `content/{lang}/tech/post.md`
- `content/{lang}/business/post.md`
- `content/{lang}/lifestyle/post.md`

❌ **NOT Allowed**:
- `content/{lang}/post.md` ← Creates orphan content!

---

## Post Frontmatter Template

```markdown
---
title: "Your Post Title Here"
date: 2026-01-20
draft: false
categories: ["tech"]              # REQUIRED! One of: tech, business, lifestyle
tags: ["AI", "trends", "2025"]    # Optional
description: "SEO description (150-160 chars)"
---

First paragraph becomes the summary automatically.
Keep it under 150 characters for clean display on homepage.

## Start Content Here

Your actual content...
```

---

## Summary Rules

### How Summaries Work
- **Auto-generated**: First paragraph becomes `.Summary`
- **Display**: Truncated to 150 chars on homepage
- **Best practice**: Write compelling first paragraph

### Good Example
```markdown
AI coding assistants are transforming software development in 2025.
This guide explores the top tools and how to integrate them effectively.
```

### Bad Example
```markdown
# AI Coding Assistants 2025

Welcome to this comprehensive guide about AI coding assistants...
```
❌ Problem: Title gets included in summary

---

## URL Structure

### Pattern
```
/{lang}/{category}/{slug}/
```

### Examples
| Language | Category | Post | URL |
|----------|----------|------|-----|
| EN | Tech | `ai-trends-2025.md` | `/tech/ai-trends-2025/` |
| KO | Business | `startup-funding.md` | `/ko/business/startup-funding/` |
| JA | Lifestyle | `digital-nomad.md` | `/ja/lifestyle/digital-nomad/` |

**Note**: EN (default language) has no `/en/` prefix

---

## Category Definitions

### Tech (💻 Technology)
**Topics**:
- AI, Machine Learning, Data Science
- Web Development, Programming
- Cloud, DevOps, Infrastructure
- Cybersecurity, Privacy

**Translations**:
- EN: Technology
- KO: 기술
- JA: テクノロジー

---

### Business (💼 Business)
**Topics**:
- Startups, Entrepreneurship
- Marketing, Sales
- Investment, Funding
- Business Strategy, Management

**Translations**:
- EN: Business
- KO: 비즈니스
- JA: ビジネス

---

### Lifestyle (🌟 Lifestyle)
**Topics**:
- Digital Nomad, Remote Work
- Productivity, Time Management
- Travel, Living Abroad
- Work-Life Balance

**Translations**:
- EN: Lifestyle
- KO: 라이프스타일
- JA: ライフスタイル

---

## Creating New Posts

### Manual Creation
```bash
# Create new post
hugo new content/{lang}/{category}/post-title.md

# Examples
hugo new content/en/tech/ai-coding-2025.md
hugo new content/ko/business/startup-guide.md
hugo new content/ja/lifestyle/nomad-tips.md
```

### Automated Creation
See `scripts/generate_posts.py` for automation workflow.

---

## Quality Standards

### Length
- **Minimum**: 800 words
- **Optimal**: 1,200-1,500 words
- **Maximum**: 2,500 words

### Structure
- **Headings**: 3-5 H2 sections
- **Paragraphs**: 2-4 sentences max
- **Lists**: Use bullet points for scanability

### SEO
- **Title**: 50-60 characters
- **Description**: 150-160 characters
- **Keywords**: 5-7 natural mentions in content
- **Images**: Alt text required

### Readability
- **Tone**: Professional but friendly
- **Sentences**: Active voice preferred
- **Jargon**: Explain technical terms
- **CTAs**: End with question or next step

---

## Prohibited Content

❌ **Do NOT**:
- Pure keyword stuffing
- AI-obvious phrases ("revolutionary", "game-changer")
- Duplicate content across languages (translate properly)
- Posts without categories
- Draft: true in production

---

## Multilingual Best Practices

### Translation Quality
- ✅ Native-level translation
- ✅ Culturally appropriate examples
- ✅ Local date formats
- ❌ Direct machine translation without review

### Language-Specific Considerations

**English**:
- US English spelling
- Casual but professional tone
- Examples: US companies/brands

**Korean**:
- Formal speech level (해요체)
- Korean examples when possible
- KST timezone references

**Japanese**:
- Polite form (です・ます)
- Japanese companies as examples
- JST timezone references

---

## References

- Hugo Content Organization: https://gohugo.io/content-management/organization/
- Multilingual Mode: https://gohugo.io/content-management/multilingual/
