# Project Overview

## Jake's Tech Insights

Jake's Tech Insights is a fully automated, multilingual blog platform built with Hugo, powered by AI-generated content. The system generates, validates, and publishes high-quality content across three languages with minimal human intervention.

## Quick Facts

- **Tech Stack**: Hugo (PaperMod theme), Python 3, Claude API, GitHub Actions, Cloudflare Pages
- **Languages**: English, Korean (한국어), Japanese (日本語)
- **Categories**: Tech, Business, Society, Entertainment, Lifestyle
- **Automation Level**: 95% automated (generation → quality check → review → PR creation)
- **Deployment**: Cloudflare Pages (automatic on push to main)
- **Build Time**: 2-3 minutes from push to live

## System Architecture

### High-Level Flow

```
Topic Queue → Content Generation → Quality Gate → AI Review → GitHub PR → Human Approval → Deploy
```

**Explanation:**
1. **Topic Queue**: Pending topics managed in state machine (pending/in_progress/completed)
2. **Content Generation**: Two-stage AI generation (Draft Agent + Editor Agent)
3. **Quality Gate**: Validates word count, structure, SEO, frontmatter
4. **AI Review**: Self-review with 5-criteria scoring (APPROVE/REVISE/REJECT)
5. **GitHub PR**: Automated pull request creation with reports
6. **Human Approval**: Manual review and merge (optional, can be automated)
7. **Deploy**: Cloudflare Pages auto-deploys on merge to main

### Key Components

#### 1. Topic Queue System
**File**: `scripts/topic_queue.py`

**Purpose**: Manages content generation backlog

**Features**:
- State machine: pending → in_progress → completed
- Priority-based reservation (higher priority first)
- Automatic retry on failure
- Multi-language support (EN/KO/JA)
- Cleanup for stuck topics (> 24 hours)

**Usage**:
```bash
# View queue statistics
python scripts/topic_queue.py stats

# Reserve 3 topics for generation
python scripts/topic_queue.py reserve 3

# Clean up stuck topics (older than 24 hours)
python scripts/topic_queue.py cleanup 24
```

#### 2. Content Generator
**File**: `scripts/generate_posts.py`

**Purpose**: Generates blog posts using Claude API

**Features**:
- Two-stage generation: Draft Agent + Editor Agent
- Language-specific prompts (EN/KO/JA)
- max_tokens: 12,000 (prevents truncation, ensures completion)
- Target length: 800-1,100 words (EN/KO), 3,000-4,500 chars (JA)
- Tone optimization: Toss (KO), Medium/Substack (EN), Natural (JA)
- Auto-generate titles and meta descriptions
- Hugo frontmatter generation with timezone

**Usage**:
```bash
# Generate 3 posts from queue
python scripts/generate_posts.py --count 3

# Generate specific topic
python scripts/generate_posts.py --topic-id 001-en-tech-ai-coding
```

#### 3. Quality Gate
**File**: `scripts/quality_gate.py`

**Purpose**: Validates content quality before deployment

**Checks**:
- Word count validation (800-1,600 words, 3,000-5,000 chars JA)
- AI phrase detection (warnings only, not critical)
- Frontmatter completeness (title, date, category, description)
- SEO and readability metrics

**Usage**:
```bash
# Run quality gate
python scripts/quality_gate.py

# Strict mode (warnings become failures)
python scripts/quality_gate.py --strict
```

#### 4. AI Reviewer
**File**: `scripts/ai_reviewer.py`

**Purpose**: Self-review of generated content using AI

**Criteria** (scored 1-10):
1. **Authenticity**: Natural human tone, no AI phrases
2. **Value**: Practical, actionable insights
3. **Engagement**: Interesting structure and flow
4. **Technical Accuracy**: Correct facts and details
5. **SEO Quality**: Good keyword usage and structure

**Thresholds**:
- APPROVE: Average score ≥ 8.0
- REVISE: Average score 6.0-7.9
- REJECT: Average score < 6.0

**Usage**:
```bash
# Review all generated files
python scripts/ai_reviewer.py

# Review specific file
python scripts/ai_reviewer.py --file content/en/tech/2026-01-16-my-post.md
```

#### 5. GitHub Actions Workflows

**File**: `.github/workflows/test-pr.yml`
- **Purpose**: Manual PR testing
- **Trigger**: Manual workflow dispatch
- **Steps**: Hugo build validation, quality gate, AI review

**File**: `.github/workflows/daily-content.yml`
- **Purpose**: Automated daily content generation
- **Trigger**: Scheduled (cron) or manual
- **Steps**: Generate posts, run quality checks, create PR

## Directory Structure

```
jakes-tech-insights/
├── .github/
│   └── workflows/
│       ├── test-pr.yml           # PR testing workflow
│       └── daily-content.yml     # Daily content generation
├── content/
│   ├── en/                       # English posts
│   │   ├── tech/
│   │   ├── business/
│   │   ├── society/
│   │   ├── entertainment/
│   │   └── lifestyle/
│   ├── ko/                       # Korean posts (한국어)
│   │   └── (same structure)
│   └── ja/                       # Japanese posts (日本語)
│       └── (same structure)
├── data/
│   └── topics_queue.json         # Topic queue state
├── docs/
│   ├── PROJECT_CONTEXT.md        # Comprehensive project documentation
│   ├── DESIGN_SYSTEM.md          # UI/UX design decisions
│   ├── HUGO_CONFIG.md            # Hugo configuration guide
│   ├── MONETIZATION.md           # AdSense and revenue strategy
│   ├── TROUBLESHOOTING.md        # Common issues and solutions
│   ├── ARCHITECTURE_DECISIONS.md # ADRs (why we made key choices)
│   └── PROJECT_OVERVIEW.md       # This file
├── layouts/
│   ├── index.html                # Homepage Bento grid layout
│   ├── categories/
│   │   └── list.html             # Category landing pages
│   └── _default/
│       ├── all-posts.html        # All posts listing
│       └── single.html           # Individual post pages
├── scripts/
│   ├── topic_queue.py            # Queue management
│   ├── generate_posts.py         # Content generation
│   ├── quality_gate.py           # Quality validation
│   ├── ai_reviewer.py            # AI self-review
│   └── test_queue.py             # Queue system tests
├── static/
│   └── images/
│       └── thumbnails/           # Post thumbnail images
├── themes/
│   └── PaperMod/                 # Hugo theme (git submodule)
├── assets/
│   └── css/
│       └── extended/
│           └── custom.css        # Custom styling overrides
├── hugo.toml                     # Hugo configuration
└── requirements.txt              # Python dependencies
```

## Content Structure

### Multilingual Organization

Each language maintains a separate content directory with identical category structure:

```
content/
├── en/
│   ├── tech/
│   ├── business/
│   ├── society/
│   ├── entertainment/
│   └── lifestyle/
├── ko/
│   └── (same categories)
└── ja/
    └── (same categories)
```

**Benefits**:
- Clear language separation
- No file name conflicts
- Easy automated generation
- Simple backup/migration

### Post Frontmatter

**Required Fields**:
```yaml
---
title: "SEO-friendly title (50-60 chars)"
date: 2026-01-17T12:00:00+09:00
draft: false
categories: ["tech"]
description: "Meta description (120-160 chars)"
---
```

**Optional Fields**:
```yaml
author: "Jake Park"
image: "/images/thumbnails/post-image.jpg"
keywords: ["keyword1", "keyword2"]
```

## Automation Workflows

### Daily Content Generation (Planned)

**Schedule**: 12 PM KST (3 AM UTC)

**Process**:
1. Pick 3 topics from queue (1 per language: EN/KO/JA)
2. Generate content using Claude API
3. Run quality checks (quality gate + AI review)
4. Create Hugo markdown files
5. Commit and push to GitHub
6. Auto-deploy via Cloudflare Pages (2-3 min)

**Monthly Output**: ~90 posts (30 days × 3 posts)

### Weekly Keyword Curation (Planned)

**Schedule**: Sundays 6 PM KST

**Process**:
1. Fetch 15 trending keywords from Google Trends API
2. Distribute evenly: 5 categories × 3 languages = 15 topics
3. Add to `data/topics_queue.json` for content generation

**Categories**: Tech, Business, Society, Entertainment, Lifestyle

## Required Secrets

Set these in GitHub repository settings (Settings → Secrets and variables → Actions):

```
ANTHROPIC_API_KEY=your-claude-api-key
```

## Technology Choices

### Hugo Static Site Generator
- **Why**: Extremely fast builds (< 1 sec for 100+ posts)
- **Deployment**: Cloudflare Pages (free, global CDN)
- **Theme**: PaperMod (clean, minimal, SEO-optimized)

### Claude API (Anthropic)
- **Model**: claude-3-5-sonnet-20241022
- **Why**: Best balance of quality, speed, and cost
- **Cost**: ~$0.09/post with 12K max_tokens

### Python Scripts
- **Why**: Easy to write, maintain, and integrate with CI/CD
- **Dependencies**: anthropic, pyyaml, markdown

### GitHub Actions
- **Why**: Free for public repos, integrated with GitHub
- **Use Cases**: Automated testing, content generation, PR creation

## Key Metrics

### Content Quality
- **Target Length**: 800-1,100 words (EN/KO), 3,000-4,500 chars (JA)
- **AI Phrase Detection**: Warnings only (not blocking)
- **AI Review Score**: Target ≥ 8.0/10 for approval

### Automation
- **Success Rate**: 95% (minimal human intervention needed)
- **Generation Time**: 6-8 seconds per post (two-stage)
- **Build Time**: < 1 second (Hugo)
- **Deployment Time**: 2-3 minutes (Cloudflare Pages)

### Cost
- **Per Post**: ~$0.09 (Claude API)
- **Monthly (90 posts)**: ~$8.10
- **Hosting**: Free (Cloudflare Pages)

## Current Status

**Production**: Live at https://jakes-tech-insights.pages.dev/

**Progress**:
- ✅ Day 1-3: Foundation (Hugo setup, topic queue, content generation)
- ✅ Day 4-5: Automation (quality gate, AI review, GitHub Actions)
- ✅ Day 6: Optimization (UI/UX fixes, writing quality upgrade, bug fixes)

**Next Steps**:
- [ ] Enable daily automated content generation
- [ ] Set up weekly keyword curation
- [ ] Apply for Google AdSense
- [ ] Implement prompt caching for cost reduction
- [ ] Add search functionality
- [ ] Create privacy policy, about, contact pages

## Getting Started

### Prerequisites
- Hugo (0.120.0 or later)
- Python 3.8+
- Claude API key (Anthropic)
- Git and GitHub account

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/jakes-tech-insights.git
cd jakes-tech-insights

# Initialize Hugo theme submodule
git submodule update --init --recursive

# Install Python dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Start Hugo server
hugo server -D
```

### First Content Generation

```bash
# Add topics to queue
# (Edit data/topics_queue.json or use topic_queue.py)

# Generate 1 post
python scripts/generate_posts.py --count 1

# Run quality checks
python scripts/quality_gate.py

# Review with AI
python scripts/ai_reviewer.py

# Start Hugo server to preview
hugo server -D
```

## Documentation

For detailed information on specific topics, see:

- **PROJECT_CONTEXT.md**: Comprehensive project documentation
- **DESIGN_SYSTEM.md**: UI/UX design decisions and guidelines
- **HUGO_CONFIG.md**: Hugo configuration and multilingual setup
- **MONETIZATION.md**: AdSense integration and revenue strategy
- **TROUBLESHOOTING.md**: Common issues and solutions
- **ARCHITECTURE_DECISIONS.md**: ADRs explaining key choices
- **WINDOWS_SETUP.md**: Windows environment setup guide

## Resources

- **Hugo Documentation**: https://gohugo.io/documentation/
- **PaperMod Theme**: https://github.com/adityatelange/hugo-PaperMod
- **Claude API**: https://docs.anthropic.com/
- **GitHub Actions**: https://docs.github.com/en/actions
- **Cloudflare Pages**: https://pages.cloudflare.com/

---

**Last Updated**: 2026-01-17
**Status**: Day 6 Complete - Production Ready
