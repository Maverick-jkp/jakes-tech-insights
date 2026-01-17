# Jake's Tech Insights - Project Context

## 📌 Project Overview

**Jake's Tech Insights** is a fully automated, multilingual blog platform built with Hugo, powered by AI-generated content.

- **Tech Stack**: Hugo (PaperMod theme), Python 3, Claude API, GitHub Actions, Cloudflare Pages
- **Languages**: English, Korean (한국어), Japanese (日本語)
- **Categories**: Tech, Business, Lifestyle
- **Automation Level**: 95% automated (generation → quality check → review → PR creation)

## 🎯 System Architecture

```
Topic Queue → Content Generation → Quality Gate → AI Review → GitHub PR → Human Approval → Deploy
```

### Key Components

1. **Topic Queue System** (`scripts/topic_queue.py`)
   - State machine: pending → in_progress → completed
   - Priority-based reservation
   - Automatic retry on failure
   - Multi-language support

2. **Content Generator** (`scripts/generate_posts.py`)
   - Two-stage generation: Draft Agent + Editor Agent
   - Language-specific prompts (EN/KO/JA)
   - max_tokens: 12000 (prevents truncation, ensures completion)
   - Target: 800-1,100 words (EN/KO), 3,000-4,500 chars (JA)
   - Tone: Toss style (KO), Medium/Substack (EN), Natural (JA)
   - Auto-generate titles and meta descriptions
   - Hugo frontmatter generation

3. **Quality Gate** (`scripts/quality_gate.py`)
   - Word count validation (800-1600 words, 3000-5000 chars JA)
   - AI phrase detection (warnings only, not critical)
   - Frontmatter completeness check
   - SEO and readability metrics

4. **AI Reviewer** (`scripts/ai_reviewer.py`)
   - Self-review with 5 criteria scoring
   - APPROVE/REVISE/REJECT recommendations
   - Detailed suggestions for improvement
   - JSON report generation

5. **GitHub Actions Workflows**
   - `test-pr.yml`: Manual PR testing
   - `daily-content.yml`: Automated daily content generation

## 📁 Directory Structure

```
jakes-tech-insights/
├── .github/workflows/
│   ├── test-pr.yml           # PR testing workflow
│   └── daily-content.yml     # Daily content generation
├── content/
│   ├── en/                   # English posts
│   ├── ko/                   # Korean posts
│   └── ja/                   # Japanese posts
├── data/
│   └── topics_queue.json     # Topic queue state
├── scripts/
│   ├── topic_queue.py        # Queue management
│   ├── generate_posts.py     # Content generation
│   ├── quality_gate.py       # Quality validation
│   ├── ai_reviewer.py        # AI self-review
│   └── test_queue.py         # Queue system tests
├── themes/PaperMod/          # Hugo theme
├── config.yml                # Hugo configuration
└── PROJECT_CONTEXT.md        # This file
```

## 🚀 Implementation Timeline

### ✅ Day 1: PR Workflow Setup
- Created `test-pr.yml` workflow
- Manual trigger for testing
- Basic Hugo build validation

### ✅ Day 2: Topic Queue System
- Implemented state machine pattern
- Created queue management CLI
- Added priority-based reservation
- Retry mechanism for failures
- Comprehensive test suite

### ✅ Day 3: Content Generation
- Two-stage generation (Draft + Editor)
- Language-specific system prompts
- Auto-generated metadata
- Queue integration
- Tested with Digital Minimalism post

### ✅ Day 4-5: Quality & Automation
- Quality gate with FAIL/WARN criteria
- AI self-review agent (5-criteria scoring)
- Daily content generation workflow
- Automatic PR creation
- Report artifacts upload

## 🔧 Usage Guide

### Generate Content Manually

```bash
# Generate 3 posts from queue
python scripts/generate_posts.py --count 3

# Generate specific topic
python scripts/generate_posts.py --topic-id 001-en-tech-ai-coding
```

### Run Quality Checks

```bash
# Run quality gate
python scripts/quality_gate.py

# Strict mode (warnings become failures)
python scripts/quality_gate.py --strict
```

### AI Review

```bash
# Review all generated files
python scripts/ai_reviewer.py

# Review specific file
python scripts/ai_reviewer.py --file content/en/tech/2026-01-16-my-post.md
```

### Manage Topic Queue

```bash
# View queue statistics
python scripts/topic_queue.py stats

# Reserve topics
python scripts/topic_queue.py reserve 3

# Clean up stuck topics
python scripts/topic_queue.py cleanup 24
```

### Test Queue System

```bash
python scripts/test_queue.py
```

## 📊 Quality Standards

### Content Requirements
- **Word count**: 900-1800 words
- **Tone**: Professional but friendly
- **Structure**: 3-5 H2 headings
- **Links**: 2+ external references
- **SEO**: Natural keyword integration (5-7 times)

### Frontmatter Requirements
```yaml
title: "SEO-friendly title (50-60 chars)"
date: 2026-01-16
draft: false
categories: ["tech"]
tags: ["keyword", "tags"]
description: "Meta description (120-160 chars)"
```

### AI Phrase Blacklist
- English: "revolutionary", "game-changer", "cutting-edge", "it's important to note"
- Korean: "물론", "혁신적", "게임체인저"
- Japanese: "もちろん", "革新的", "ゲームチェンジャー"

## 🤖 AI Review Criteria

1. **Authenticity** (1-10): Natural human tone, no AI phrases
2. **Value** (1-10): Practical, actionable insights
3. **Engagement** (1-10): Interesting structure and flow
4. **Technical Accuracy** (1-10): Correct facts and details
5. **SEO Quality** (1-10): Good keyword usage and structure

**Thresholds:**
- APPROVE: Average score ≥ 8.0
- REVISE: Average score 6.0-7.9
- REJECT: Average score < 6.0

## 🔄 Automated Workflow

### Weekly Keyword Curation (Sundays 6 PM KST)
```bash
# Automated via cron job
cd /Users/jakepark/projects/jakes-tech-insights && source ~/.zshrc && python3 scripts/keyword_curator.py --count 15
```

**What it does:**
- Fetches 15 trending keywords from Google Trends API
- Distributes evenly: 5 categories × 3 languages = 15 topics
- Adds to `scripts/queue.txt` for content generation
- Categories: Tech, Business, Society, Entertainment, Lifestyle

### Daily Content Generation (12 PM KST)
```bash
# Automated via cron job
cd /Users/jakepark/projects/jakes-tech-insights && source ~/.zshrc && python3 scripts/content_processor.py
```

**What it does:**
- Picks 3 topics from queue (1 per language: EN/KO/JA)
- Generates content using Claude API
- Runs quality checks
- Creates Hugo markdown files
- Commits and pushes to GitHub
- Auto-deploys via Cloudflare Pages (2-3 min)

### Manual Trigger
```bash
# Via GitHub UI
Actions → Daily Content Generation → Run workflow

# Or run locally
python3 scripts/keyword_curator.py --count 15
python3 scripts/content_processor.py
```

### Workflow Schedule
- **Sunday 6 PM KST**: Keyword curation (15 topics)
- **Daily 12 PM KST**: Content generation (3 posts)
- **Result**: ~90 posts/month (30 days × 3 posts)

## 🔐 Required Secrets

Set these in GitHub repository settings:

```
ANTHROPIC_API_KEY=your-claude-api-key
```

## 📈 Success Metrics

### Generated Content Stats
- **Test Generation**: 1 post (Digital Minimalism)
- **Word Count**: ~1,200 words
- **Character Length**: 8,291 chars (after editing)
- **Quality**: No AI phrases detected

### Queue Stats (Current)
- **Total topics**: 18
- **Completed**: 2
- **In Progress**: 7
- **Pending**: 9

### Coverage
- **Languages**: EN (6), KO (6), JA (6)
- **Categories**: Tech (6), Business (6), Lifestyle (6)
- **Priority Range**: 6-8

## 🐛 Known Issues & Solutions

### Issue 1: Hugo Server Not Showing New Content
**Solution**: Restart Hugo server with `~/hugo_bin server -D`

### Issue 2: Workflow Files Not Pushing
**Cause**: GitHub requires workflow scope permission
**Solution**: Push all files together or create workflow via GitHub UI

### Issue 3: Stuck Topics in Queue
**Solution**: Run cleanup command: `python scripts/topic_queue.py cleanup 24`

### Issue 4: Content Truncation & Monetization ✅ SOLVED
**Problem**:
- Korean (794 words) and Japanese (102 words) posts failed quality gate
- Content ending mid-sentence (truncation)
- Content too verbose for optimal completion rate

**Root Cause**:
- max_tokens insufficient for completion
- No length optimization for monetization

**Solution**:
- max_tokens: 4000 → 8000 → 12000
- Target length: 800-1,100 words (EN/KO), 3,000-4,500 chars (JA)
- Quality Gate: 800-1,600 words, 3,000-5,000 chars (JA)
- Tone optimization: Toss (KO), Medium/Substack (EN), Natural (JA)
- Completion validation: "마지막 문장까지 완결"

**Result**:
- No truncation (12K tokens provides headroom)
- Optimal for AdSense (exceeds 300-500 word minimum)
- Better completion rate (3-4 min read time)

**Cost Impact**: ~$0.03 → $0.06 → $0.09/post ($8.1/month for 3 posts/day)

## 🎉 Implementation Timeline

### Day 1-3: Foundation (Completed)
- ✅ Hugo site setup with multilingual support
- ✅ Topic queue system with state machine
- ✅ Content generation (Draft + Editor agents)
- ✅ Navigation and UI fixes

### Day 4-5: Automation (Completed)
- ✅ Quality Gate system
- ✅ AI Reviewer with 5-criteria scoring
- ✅ GitHub Actions workflows
- ✅ max_tokens optimization (4000 → 8000 → 12000)
- ✅ Monetization optimization (length, tone, completion)
- ✅ Quality Gate criteria updated (800-1,600 words for flexibility)

### Day 6+: Optimization (Planned)
- [ ] Prompt Caching for cost reduction
- [ ] Keyword research automation
- [ ] Image auto-generation
- [ ] A/B testing for titles

## 💰 Cost Analysis

### Current Setup (3 posts/day, 12K tokens)
- **Draft Agent**: ~6K tokens × $0.015/1K = $0.09/post
- **Editor Agent**: ~6K tokens × $0.015/1K = $0.09/post (may use less)
- **Total per post**: ~$0.09 (actual may be $0.06-0.09)
- **Monthly (90 posts)**: ~$8.10 (with 12K max_tokens)
- **Note**: Shorter target length may use fewer tokens in practice

### Cost vs. Value Trade-off
- **Truncation eliminated**: 12K tokens prevents mid-sentence cuts
- **Completion rate optimized**: 800-1,100 words = 3-4 min read
- **Higher RPM potential**: Better engagement = better monetization
- **Net benefit**: +$2.70/month cost, but higher revenue potential

### Optimization Options
1. **Reduce frequency**: 1 post/day = $2.70/month
2. **Prompt Caching**: Save ~50% with cache hits ($4.05/month)
3. **Monitor actual usage**: May be lower than max_tokens
4. **Enable Daily Automation**: Set up daily cron schedule
5. **Monitor & Iterate**: Track quality metrics and adjust prompts

## 📝 Notes

- All scripts support both CLI and programmatic usage
- Queue state persists in `data/topics_queue.json`
- Reports saved: `quality_report.json`, `ai_review_report.json`
- Hugo theme: PaperMod (customizable via config.yml)
- Deployment: Automatic via Cloudflare Pages on push to main

## 🔗 Resources

- **Hugo Documentation**: https://gohugo.io/documentation/
- **PaperMod Theme**: https://github.com/adityatelange/hugo-PaperMod
- **Claude API**: https://docs.anthropic.com/
- **GitHub Actions**: https://docs.github.com/en/actions

---

**Last Updated**: 2026-01-17
**Status**: Day 6 Complete ✅ (Production bugs fixed + Writing quality upgraded)

## 🐛 Recent Bug Fixes (2026-01-17)

### Issue 5: Posts Hidden on Production (Future Post Issue) ✅ SOLVED
**Problem**:
- 2026-01-17 posts (5 posts) not showing on production, but visible locally
- Thumbnails broken for all posts except one Japanese startup article

**Root Cause**:
- Missing timezone in post dates → Cloudflare interpreted as UTC, making them "future posts"
- SVG files misnamed as .jpg → Browser couldn't render

**Solution**:
- Added `+09:00` timezone to all post dates in frontmatter
- Added `timeZone = 'Asia/Seoul'` to hugo.toml
- Replaced SVG placeholders with real Unsplash JPEG images (14 posts)
- Created fetch_images_for_posts.py script for batch image downloads

**Result**:
- All 15 posts (5 per language) now visible on production
- All thumbnails display correctly with high-quality photos
- Fixed both timezone and image issues

### Writing Quality Enhancement (2026-01-17) ✅ COMPLETE

**Enhancement**: Upgraded content generation prompts based on ChatGPT's "human-touch" strategies

**Key Improvements**:
1. **Hooking Strategy**: Problem-driven openings instead of generic intros
2. **Real Examples**: Specific companies/stats, not "many companies..."
3. **Failure Cases**: Dedicated sections for "When X doesn't work"
4. **Authenticity Markers**: "In my experience...", show vulnerability
5. **Decision-Stage Focus**: "What to avoid" as much as "What to do"

**Implementation**:
- Updated Draft Agent prompts (all 3 languages)
- Updated Editor Agent prompts (all 3 languages)
- Added 🎯 HOOKING STRATEGY section to guide AI
- Added 🎯 CRITICAL ENHANCEMENTS for editors

**Expected Impact**:
- Higher engagement (longer read time)
- More authentic tone (less AI smell)
- Better trust signals (shows limitations)
- Improved conversion (decision-stage content)

**Next Milestone**: Phase 5 - Monetization preparation
