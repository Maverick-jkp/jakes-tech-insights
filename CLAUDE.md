# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

# ⚠️ STOP - MANDATORY FIRST ACTION ⚠️

**Before doing ANYTHING in this repository, you MUST read these files IN ORDER:**

```
☐ 1. CLAUDE.md (this file) - Technical architecture & commands
☐ 2. .claude/WORKFLOW.md - Multi-agent workflow rules (if applicable)
☐ 3. .claude/session-state.json - Current project state & recent changes
☐ 4. .claude/mistakes-log.md - Past errors to avoid
```

**This is NOT optional. This is NOT negotiable.**

**Why this matters:**
- Skipping = Breaking workflow = Repeating past mistakes = Wasting user's time
- Takes 5-10 minutes but saves hours of rework
- System enforcement exists but reading is YOUR responsibility

**After reading all 4 files, announce:**
```
✅ Checklist complete:
   - Read CLAUDE.md
   - Read WORKFLOW.md
   - Read session-state.json
   - Read mistakes-log.md
   Ready to proceed with: [task description]
```

**DO NOT proceed until you announce checklist completion.**

---

# 🔴 MANDATORY PRE-ACTION VERIFICATION 🔴

**Before attempting to "fix" ANY reported issue, you MUST complete this verification checklist:**

```bash
# Step 1: Verify problem exists locally
git status
git diff

# Step 2: Check if already fixed in remote repository
git fetch origin
git show origin/main:path/to/file | grep "search-term"

# Step 3: Verify environment files exist
ls -la .env
ls -la .git/config

# Step 4: If issue involves environment variables, verify they exist
grep "VARIABLE_NAME" .env

# Step 5: Check documented procedures FIRST
# Example: CLAUDE.md line 81 shows how to load .env
# DO NOT improvise - follow documented method
```

**CRITICAL RULES**:
1. ❌ **NEVER assume** user's report means issue currently exists - verify first
2. ❌ **NEVER improvise** solutions when documented procedures exist
3. ❌ **NEVER claim** files/keys/tools are missing without checking
4. ✅ **ALWAYS verify** current state before attempting any fix
5. ✅ **ALWAYS follow** documented procedures exactly as written
6. ✅ **ALWAYS check** if issue already resolved in previous session

**If verification shows issue is already fixed**: Report findings, do NOT redo the work.

---

## Project Overview

**Jake's Tech Insights** is an AI-powered multilingual blog system that generates content automatically using Claude API. The system handles everything from keyword curation to content generation, quality validation, and deployment.

- **Tech Stack**: Hugo (static site generator), Python 3.x, Claude API (Sonnet 4.5), GitHub Actions
- **Languages**: English, Korean (한국어), Japanese (日本語)
- **Deployment**: Cloudflare Pages (https://jakes-tech-insights.pages.dev)
- **Automation**: 3x daily content generation (6 AM, 12 PM, 6 PM KST)

---

## Quick Command Reference

### Hugo Commands
**CRITICAL**: Hugo is installed at `/opt/homebrew/bin/hugo` (not in PATH).
Always use the full path:

```bash
# Start development server (with drafts)
/opt/homebrew/bin/hugo server -D

# Production build
/opt/homebrew/bin/hugo --minify

# Check version
/opt/homebrew/bin/hugo version

# Build and check errors
/opt/homebrew/bin/hugo --minify 2>&1 | grep -i error
```

### Python Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Required environment variables
export ANTHROPIC_API_KEY='your-key'
export UNSPLASH_ACCESS_KEY='your-key'  # For featured images

# Load from .env file (recommended)
# File location: /Users/jakepark/projects/jakes-tech-insights/.env
python -c "from dotenv import load_dotenv; load_dotenv()"
```

### Testing

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_topic_queue.py

# Run with verbose output
pytest -v

# Coverage report (HTML)
pytest --cov=scripts --cov-report=html
# View at htmlcov/index.html

# Quick validation (no API calls)
python scripts/topic_queue.py stats
```

### Content Generation Pipeline

```bash
# 1. Curate keywords (weekly, ~5 min manual filtering)
python scripts/keyword_curator.py --count 15

# 2. Generate posts (automated, uses topic queue)
python scripts/generate_posts.py --count 3

# 3. Run quality checks (automated in CI)
python scripts/quality_gate.py

# 4. AI review (optional, recommendation only)
python scripts/ai_reviewer.py

# 5. Local preview
/opt/homebrew/bin/hugo server -D
# Visit http://localhost:1313
```

---

## System Architecture

### Content Generation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     Topic Queue State Machine                    │
│                   (data/topics_queue.json)                       │
│                                                                   │
│   pending → in_progress → completed                              │
│                ↓                                                  │
│              failed (retry)                                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              Draft Agent (Claude API - Sonnet 4.5)              │
│                  System Prompt: EN/KO/JA specific               │
│                  max_tokens: 12000                              │
│                  Prompt Caching: Enabled (20% cost reduction)   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│             Editor Agent (Claude API - Sonnet 4.5)              │
│                  Refinement: Tone, Structure, SEO               │
│                  max_tokens: 12000                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Quality Gate (quality_gate.py)                │
│   - Word count: 800-2000 (EN/KO), 3000-7500 chars (JA)         │
│   - AI phrase blacklist check                                   │
│   - SEO validation (meta description, keywords)                 │
│   - Image check (WARNING only)                                  │
│   - References check                                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                 AI Reviewer (ai_reviewer.py)                     │
│   5-Criteria Scoring:                                           │
│   - Authenticity (human tone)                                   │
│   - Value (practical insights)                                  │
│   - Engagement (structure)                                      │
│   - Technical Accuracy                                          │
│   - SEO Quality                                                 │
│   Result: APPROVE (≥8.0) / REVISE (6.0-7.9) / REJECT (<6.0)    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Git Commit (Markdown Files)                   │
│   Location: content/{en,ko,ja}/{category}/{date}-{slug}.md     │
│   Frontmatter: title, date, categories, tags, image, etc.      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│          GitHub Actions (.github/workflows/daily-content.yml)   │
│   Schedule: 6 AM, 12 PM, 6 PM KST (may delay 15-60 min)        │
│   Steps: pytest → generate → quality gate → create PR          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              Cloudflare Pages (Auto-deploy on merge)            │
│   URL: https://jakes-tech-insights.pages.dev                   │
│   Build: hugo --minify                                          │
└─────────────────────────────────────────────────────────────────┘
```

### Topic Queue State Machine

Topics in `data/topics_queue.json` flow through these states:

1. **pending** - Ready to be processed (default for new topics)
2. **in_progress** - Currently being generated (reserved by `reserve_topics()`)
3. **completed** - Successfully published (marked by `mark_completed()`)
4. **failed** - Generation failed (marked by `mark_failed()`, will retry)

**Key Functions** (in `scripts/topic_queue.py`):
- `reserve_topics(count=3)` - Move pending → in_progress, return reserved topics
- `mark_completed(topic_id)` - Move in_progress → completed
- `mark_failed(topic_id, error)` - Move in_progress → failed (auto-retry later)
- `cleanup(hours=24)` - Reset stuck in_progress topics (manual recovery)

**Duplicate Prevention**: Queue automatically skips keywords already completed for same language.

---

## File Structure & Key Components

### Content Files
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

**Post Format**: Markdown with YAML frontmatter
```yaml
---
title: "Post Title"
date: 2026-01-22T18:00:00+09:00  # KST timezone required
categories: ["tech"]
tags: ["keyword1", "keyword2"]
description: "120-160 char meta description"
image: "https://images.unsplash.com/photo-..."
imageCredit: "Photo by [Name](https://unsplash.com/@username)"
lang: "en"
---

Content here...
```

### Python Scripts

| Script | Purpose | Key Functions | When to Run |
|--------|---------|---------------|-------------|
| `topic_queue.py` | Topic state management | `reserve_topics()`, `mark_completed()`, `cleanup()` | Always (imported by others) |
| `generate_posts.py` | Content generation | `generate_post()` (Draft + Editor agents) | Manual or automated (3x daily) |
| `quality_gate.py` | Validation checks | `validate_content()`, `check_ai_phrases()` | After generation (automated) |
| `ai_reviewer.py` | 5-criteria scoring | `review_content()`, provides recommendations | Optional (manual review) |
| `keyword_curator.py` | Keyword research | Fetches Google Trends, human filtering required | Weekly (Fridays 5 PM KST) |
| `affiliate_config.py` | Affiliate link management | `detect_product_mentions()`, `generate_affiliate_link()` | Imported by generate_posts.py |

### Hugo Templates

```
layouts/
├── index.html                    # Homepage (Bento grid, theme toggle)
├── _default/
│   ├── single.html              # Article page (TOC, related posts, references)
│   ├── list.html                # Generic list page
│   └── baseof.html              # Base template
├── categories/
│   └── list.html                # Category-specific list (thumbnails)
├── partials/
│   ├── head.html                # <head> section (meta tags, SEO)
│   ├── footer.html              # Footer
│   └── ...
└── shortcodes/                  # Custom shortcodes (if any)
```

**Theme**: PaperMod (in `themes/PaperMod/`, Git submodule)
- **Do NOT modify theme directly**
- Override by creating matching file in `layouts/`
- Example: `layouts/_default/single.html` overrides theme's single.html

### Data Files

- **`data/topics_queue.json`** - Topic queue with state machine (main data source)
- **`generated_files.json`** - Tracks files created by automation (for cleanup)
- **`quality_report.json`** - Latest quality gate results (pass/fail details)
- **`ai_review_report.json`** - Latest AI review scores and recommendations

### Configuration Files

- **`hugo.toml`** - Hugo config (languages, menus, params, SEO)
- **`requirements.txt`** - Python dependencies
- **`.env`** - API keys (NOT in git, see `.env.example`)
- **`pytest.ini`** - Test configuration (coverage threshold: 48%)
- **`.coveragerc`** - Coverage.py settings

### GitHub Actions Workflows

- **`.github/workflows/daily-content.yml`** - Main automation (3x daily generation)
- **`.github/workflows/daily-keywords.yml`** - Keyword curation (Fridays 5 PM KST)
- **`.github/workflows/test.yml`** - CI testing on PR

---

## Content Quality Standards

### Word Count Requirements

| Language | Minimum | Target | Maximum |
|----------|---------|--------|---------|
| English  | 800     | 900-1,200 | 2,000 |
| Korean   | 800     | 900-1,200 | 2,000 |
| Japanese | 3,000 chars | 4,000-5,000 chars | 7,500 chars |

**Structure Requirements**:
- 3-4 main sections (## headings)
- Introduction: 80-100 words (strong hook)
- Each section: 120-180 words (core insights only)
- Conclusion: 60-80 words (clear CTA)
- Must finish completely (no mid-sentence cutoffs)

### AI Phrase Blacklist

Quality gate **fails** if these phrases appear:

**English**:
- "revolutionary", "game-changer", "cutting-edge"
- "it's important to note", "in today's digital landscape"
- "in conclusion", "in summary" (unless in actual conclusion)

**Korean**:
- "물론", "혁신적", "게임체인저"
- "디지털 시대", "중요한 점은"

**Japanese**:
- "もちろん", "革新的", "ゲームチェンジャー"
- "重要なのは", "結論として"

Full list: `scripts/quality_gate.py` lines ~50-100

### SEO Requirements

- **Meta description**: 120-160 characters
- **Keyword density**: 5-7 natural mentions (not forced)
- **Featured image**: Required (auto-fetched from Unsplash)
- **Image alt text**: Required (describes image content)
- **References section**: 2+ external links (reputable sources)
- **Internal links**: Related posts (Hugo template handles automatically)

### Image Requirements

- **Source**: Unsplash API (auto-generated with credits)
- **Format**: JPEG/PNG, optimized
- **Alt text**: Descriptive, includes keyword naturally
- **Credit**: Photo by [Name](https://unsplash.com/@username)

---

## Common Development Tasks

### 1. Generate Content for Specific Keyword

```bash
# Add topic to queue
python3 << 'EOF'
import sys
from pathlib import Path
sys.path.insert(0, str(Path('scripts')))
from topic_queue import add_topic

add_topic(
    keyword="Your Keyword",
    category="tech",
    language="en",
    priority=8
)
print("✅ Topic added to queue")
EOF

# View queue
python scripts/topic_queue.py stats

# Generate (will pick highest priority pending)
python scripts/generate_posts.py --count 1
```

### 2. Fix Stuck Topics

If topics are stuck in `in_progress` for 24+ hours:

```bash
# View stuck topics
python scripts/topic_queue.py stats

# Reset stuck topics (24+ hours)
python scripts/topic_queue.py cleanup 24

# Verify
python scripts/topic_queue.py stats
```

### 3. Test Content Generation Locally

```bash
# Set API key
export ANTHROPIC_API_KEY='your-key'

# Generate 1 post
python scripts/generate_posts.py --count 1

# Check quality
python scripts/quality_gate.py

# Preview
/opt/homebrew/bin/hugo server -D
```

### 4. Update System Prompts

Prompts are in `scripts/generate_posts.py`:

- **English**: Lines ~63-450
- **Korean**: Lines ~450-850
- **Japanese**: Lines ~850-1250

After editing:
```bash
# Test with 1 post
python scripts/generate_posts.py --count 1

# Check output quality
cat content/en/tech/2026-01-22-*.md

# Run quality gate
python scripts/quality_gate.py
```

### 5. Add New Category

1. **Update `hugo.toml`**: Add menu items for EN/KO/JA (lines ~30-180)
   ```toml
   [[languages.en.menu.main]]
     name = "🆕 NewCategory"
     url = "/categories/newcategory/"
     weight = 11
   ```

2. **Update validation**: Edit `scripts/utils/validation.py`
   ```python
   VALID_CATEGORIES = [
       "tech", "business", "lifestyle",
       "society", "entertainment", "sports",
       "finance", "education", "newcategory"  # Add here
   ]
   ```

3. **Create directories**:
   ```bash
   mkdir -p content/en/newcategory
   mkdir -p content/ko/newcategory
   mkdir -p content/ja/newcategory
   ```

4. **Test**:
   ```bash
   /opt/homebrew/bin/hugo server -D
   ```

### 6. Run Full Pipeline Test

```bash
# 1. Check queue
python scripts/topic_queue.py stats

# 2. Generate
python scripts/generate_posts.py --count 1

# 3. Quality gate
python scripts/quality_gate.py

# 4. AI review (optional)
python scripts/ai_reviewer.py

# 5. Hugo build
/opt/homebrew/bin/hugo --minify

# 6. Preview
/opt/homebrew/bin/hugo server -D
```

### 7. Manually Trigger GitHub Actions

1. Go to **Actions** tab on GitHub
2. Select **Daily Content Generation**
3. Click **Run workflow**
4. Set parameters:
   - count: 3 (default)
   - skip_review: false
5. Click **Run workflow**
6. Wait for completion (~5 min)
7. Review PR created by workflow

---

## Troubleshooting

### Hugo Not Found

**Error**: `hugo: command not found`

**Solution**: Use full path
```bash
/opt/homebrew/bin/hugo server -D

# Or add to PATH (in ~/.zshrc or ~/.bashrc)
export PATH="/opt/homebrew/bin:$PATH"
```

### API Key Issues

**Error**: `anthropic.APIKeyError`

**Solution**: Check API key is set
```bash
# Verify key is set (shows first 10 chars only)
echo $ANTHROPIC_API_KEY | head -c 10

# Load from .env file
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('✅ OK' if os.getenv('ANTHROPIC_API_KEY') else '❌ MISSING')"

# Set manually (temporary)
export ANTHROPIC_API_KEY='sk-ant-...'
```

### Queue Stuck

**Symptom**: Topics stay in `in_progress` for hours

**Solution**: Reset stuck topics
```bash
# View current state
python scripts/topic_queue.py stats

# OR check JSON directly
cat data/topics_queue.json | python -m json.tool | grep -A 5 "in_progress"

# Reset topics stuck for 24+ hours
python scripts/topic_queue.py cleanup 24

# Verify reset
python scripts/topic_queue.py stats
```

### Quality Gate Failures

#### Word count too low

**Error**: `Word count 650 below minimum 800`

**Solution**: Increase `max_tokens` in `generate_posts.py`
```python
# Currently at line ~1100
max_tokens=12000  # Increase to 14000 if needed
```

#### AI phrases detected

**Error**: `Found blacklisted phrase: "revolutionary"`

**Solution**: Update system prompt to avoid phrase
```python
# In generate_posts.py, add to prompt:
"Never use these words: revolutionary, game-changer, cutting-edge"
```

#### Missing references

**Error**: `No References section found`

**Solution**: Editor agent prompt includes references
```python
# In generate_posts.py, Editor agent section:
"Ensure ## References section with 2+ external links"
```

### GitHub Actions Delays

**Symptom**: Scheduled workflow runs 15-60 min late

**Explanation**: This is **normal GitHub Actions behavior**
- High load periods cause delays (esp. 12 PM KST slot)
- Content is not time-sensitive, delays are acceptable
- Historical data: 6 AM slot = 25 min delay, 12 PM = 57 min delay

**Solution**: Accept delays or reschedule to off-peak times (e.g., 3 AM UTC)

See `.claude/session-state.json` → `automation_issues` for detailed analysis.

### Hugo Build Errors

**Error**: `WARN: found no layout file for "HTML" for kind "page"`

**Solution**: Check template exists
```bash
# List available templates
ls -la layouts/_default/

# Verify template syntax
/opt/homebrew/bin/hugo --debug
```

**Error**: `Error: error building site: failed to render pages`

**Solution**: Check frontmatter YAML syntax
```bash
# Validate YAML in recent posts
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

## Design System

### Colors

**Dark Theme** (default):
- Background: `#0a0a0a`
- Surface: `#151515`
- Border: `#2a2a2a`
- Text: `#e8e8e8`
- Accent: `#00ff88`

**Light Theme**:
- Background: `#ffffff`
- Surface: `#f5f5f5`
- Border: `#e0e0e0`
- Text: `#1a1a1a`
- Accent: `#00dd77`

**CSS Variables** (in theme, check `assets/css/`):
```css
:root {
    --bg: #0a0a0a;
    --fg: #e8e8e8;
    --accent: #00ff88;
}
```

### Typography

- **Headings**: Space Mono (monospace)
- **Body**: Instrument Sans (sans-serif)
- **Code**: Space Mono (monospace)

**Font Loading**: Google Fonts (preconnect in `layouts/partials/head.html`)

### Breakpoints

```css
/* Mobile-first approach */
@media (min-width: 768px) { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
```

### Grid System

Homepage uses **12-column Bento grid**:
- Gap: 1rem
- Max-width: 1400px
- Responsive: 1 col (mobile), 2 cols (tablet), 3-4 cols (desktop)

---

## Git Workflow

### Pre-commit Hook

A Git hook validates changes before commits:

**Location**: `.git/hooks/pre-commit`

**Checks**:
1. `topics_queue.json` structure (if modified)
2. Recent reports exist (warns if missing)
3. No hardcoded API keys (recommended, not enforced)

**Bypass** (emergency only):
```bash
git commit --no-verify -m "Emergency fix"
```

### Commit Message Format

```bash
git commit -m "$(cat <<'EOF'
type: Brief description

Optional detailed explanation of changes.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Example**:
```bash
git commit -m "$(cat <<'EOF'
feat: Add Society category for broader content coverage

- Updated hugo.toml with Society menu items (EN/KO/JA)
- Created content/{en,ko,ja}/society/ directories
- Updated validation to include 'society' category
- Tested local build and navigation

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### Branch Strategy

- **main**: Production branch (auto-deploys to Cloudflare)
- **auto-content-***: Automated PR branches from GitHub Actions
- **feature/***: Manual feature branches

**Workflow**:
1. GitHub Actions creates `auto-content-{N}` branch
2. Creates PR with quality reports
3. Human reviews and merges
4. Cloudflare auto-deploys on merge to main

---

## Cost Optimization

### Claude API

- **Cost per post**: ~$0.09 (with prompt caching)
- **Daily cost**: $0.27 (3 posts/day)
- **Monthly cost**: ~$8.10

**Optimization**:
- Prompt caching enabled (20-25% reduction)
- `max_tokens=12000` (prevents truncation, minimizes retries)
- Structure-based prompts (3-4 sections, not strict word counts)

### Unsplash API

- **Free tier**: 50 requests/hour
- **Usage**: 9 requests/day (3 posts × 3 languages)
- **Cost**: $0/month

### Cloudflare Pages

- **Free tier**: Unlimited bandwidth, 500 builds/month
- **Usage**: ~90 builds/month (3 daily deploys)
- **Cost**: $0/month

**Total**: ~$8.10/month

---

## Security

### API Keys

**Storage**:
- Local: `.env` file (NOT in git, see `.env.example`)
- GitHub Actions: Repository Secrets

**Required Secrets** (GitHub Settings → Secrets → Actions):
```
ANTHROPIC_API_KEY=sk-ant-...
UNSPLASH_ACCESS_KEY=...
```

### Pre-commit Validation

Recommended pattern checks (add to `.git/hooks/pre-commit`):
```bash
# Check for hardcoded keys
if git diff --cached | grep -E "(sk-ant-|ANTHROPIC_API_KEY=sk)"; then
    echo "❌ ERROR: API key detected in commit"
    exit 1
fi
```

### Past Incidents

See `.claude/session-state.json` → `security_incidents` for history.

**2026-01-22**: BRAVE_API_KEY exposed in git history (resolved, key rotated)

---

## Multi-Agent Workflow

**If you're working with multiple agents (Master, Designer, CTO, QA), see:**
- **`.claude/WORKFLOW.md`** - Sequential workflow rules, agent roles, report requirements

**For standard single-agent Claude Code usage, you can ignore multi-agent workflow.**

Key points:
- Master orchestrates all work
- Specialized agents (Designer/CTO/QA) create reports, never commit
- Only Master has commit authority
- Sequential workflow (one agent at a time)

---

## Important Files to Review

**Before starting work, read these:**

1. **`CLAUDE.md`** (this file) - Technical architecture
2. **`.claude/WORKFLOW.md`** - Multi-agent workflow (if applicable)
3. **`.claude/session-state.json`** - Current project state, recent changes
4. **`.claude/mistakes-log.md`** - Past errors to avoid

**For context:**
- **`README.md`** - Project overview, setup instructions
- **`PROJECT_CONTEXT.md`** - Detailed system docs, bug history
- **`hugo.toml`** - Hugo configuration
- **`docs/KEYWORD_STRATEGY.md`** - SEO and keyword strategy

---

## Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=scripts --cov-report=html
open htmlcov/index.html
```

### Run Specific Tests

```bash
# Topic queue tests
pytest tests/test_topic_queue.py -v

# Validation tests
pytest tests/test_validation.py -v

# Quality gate tests
pytest tests/test_quality_gate.py -v
```

### Test Coverage Requirements

- **Minimum**: 48% (enforced in `pytest.ini`)
- **Ideal**: 70%+

**Low coverage is acceptable for**:
- Scripts with heavy API dependencies (`generate_posts.py`)
- One-off utilities (`fetch_images_for_posts.py`)

---

## Links & Resources

- **Live Site**: https://jakes-tech-insights.pages.dev
- **GitHub Repo**: https://github.com/Maverick-jkp/jakes-tech-insights
- **Hugo Docs**: https://gohugo.io/documentation/
- **Claude API**: https://docs.anthropic.com/en/api/
- **PaperMod Theme**: https://github.com/adityatelange/hugo-PaperMod
- **Unsplash API**: https://unsplash.com/developers

---

## Quick Wins for New Contributors

**5-minute tasks**:
- Add new keywords to queue (`topic_queue.py`)
- Fix typos in existing posts
- Update `hugo.toml` menu items

**30-minute tasks**:
- Generate content for new keyword
- Update system prompts (tone adjustments)
- Add new AI phrase to blacklist

**2-hour tasks**:
- Add new category
- Implement new quality check
- Create custom Hugo shortcode

---

**Last Updated**: 2026-01-23
**System Version**: 5.0 (Technical Architecture Split)

---

## Version History

- **5.0** (2026-01-23): Split from multi-agent docs, focus on technical architecture
- **4.0** (2026-01-22): Consolidated multi-agent workflow rules
- **3.0** (2026-01-20): Added session checklists and mistakes log
- **2.0** (2026-01-18): Split into separate agent files
- **1.0** (2026-01-15): Initial version
