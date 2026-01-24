---
name: content-generation
description: Generates high-quality multilingual blog posts (EN/KO/JA) using Claude API with Draft + Editor agents. Use when generating content from trending keywords, creating articles (800-2000 words), or adding posts to the blog. Includes automatic quality validation and SEO optimization.
---

# Content Generation Skill

Generate high-quality multilingual blog posts (EN/KO/JA) using Claude API with Draft + Editor agents.

---

## When to Use This Skill

**Activate this skill when:**
- User requests "generate posts", "create content", or "write article"
- Task involves creating blog content from keywords
- Need to produce 800-2000 word articles in EN/KO/JA
- Working with topic queue for content automation

**Do NOT use this skill for:**
- Quality checking existing content → Use `quality-validation` skill
- Hugo build or preview operations → Use `hugo-operations` skill
- Adding new keywords to queue → Use `keyword-curation` skill

**Examples:**
- "Generate 3 blog posts"
- "Create content for keyword X"
- "Write an article about tech trends"

---

## Skill Boundaries

**This skill handles:**
- ✅ Content generation (Draft + Editor agents)
- ✅ Topic queue reservation and completion
- ✅ Frontmatter creation (title, date, categories, tags, description, image)
- ✅ File saving to content directories
- ✅ Multilingual post creation (EN/KO/JA)

**Defer to other skills:**
- ❌ Quality validation → Use `quality-validation` skill
- ❌ Hugo build/preview → Use `hugo-operations` skill
- ❌ Adding new keywords → Use `keyword-curation` skill
- ❌ Git operations → Master agent responsibility

---

## Quick Start

```bash
# Generate 3 posts (uses topic queue)
python scripts/generate_posts.py --count 3

# Add specific keyword first
python scripts/topic_queue.py add --keyword "AI trends" --lang en --category tech

# Check queue before generating
python scripts/topic_queue.py stats
```

---

## System Architecture

### Two-Agent Pipeline

```
Topic Queue (pending)
    ↓
Draft Agent (Claude API)
    ↓ (raw content)
Editor Agent (Claude API)
    ↓ (refined content)
Quality Gate
    ↓ (validated)
Git Commit → GitHub Actions → Deploy
```

**Key Components**:
- **Topic Queue**: `data/topics_queue.json` (state machine: pending → in_progress → completed)
- **Draft Agent**: Creates initial content (EN/KO/JA prompts)
- **Editor Agent**: Refines tone, structure, SEO
- **Quality Gate**: Validates word count, AI phrases, SEO

---

## Content Quality Standards

### Word Count

| Language | Minimum | Target | Maximum |
|----------|---------|--------|---------|
| English  | 800     | 900-1,200 | 2,000 |
| Korean   | 800     | 900-1,200 | 2,000 |
| Japanese | 3,000 chars | 4,000-5,000 chars | 7,500 chars |

### Structure

- **3-4 main sections** (## headings)
- **Introduction**: 80-100 words (strong hook)
- **Each section**: 120-180 words (core insights)
- **Conclusion**: 60-80 words (clear CTA)
- **Must finish completely** (no mid-sentence cutoffs)

### AI Phrase Blacklist

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

---

## Topic Queue Management

### Queue States

1. **pending** - Ready to be processed
2. **in_progress** - Currently generating (reserved)
3. **completed** - Successfully published
4. **failed** - Generation failed (will retry)

### Key Operations

```bash
# View queue status
python scripts/topic_queue.py stats

# Add topic manually
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
EOF

# Fix stuck topics (24+ hours in_progress)
python scripts/topic_queue.py cleanup 24
```

---

## Generation Process

### Step 1: Reserve Topics

Script automatically reserves topics from queue:
- Moves `pending` → `in_progress`
- Returns top 3 pending topics (by priority)
- Prevents duplicates (same keyword + language)

### Step 2: Draft Agent

**System Prompts** (in `scripts/generate_posts.py`):
- **English**: Lines ~63-450
- **Korean**: Lines ~450-850
- **Japanese**: Lines ~850-1250

**Parameters**:
```python
model="claude-sonnet-4-5-20250929"
max_tokens=12000
system_prompt=LANGUAGE_SPECIFIC_PROMPT
prompt_caching=True  # 20-25% cost reduction
```

**Output**: Raw content (markdown)

### Step 3: Editor Agent

**Refinement Focus**:
- Tone adjustment (human-like, authentic)
- Structure optimization (3-4 sections)
- SEO enhancement (keyword density 5-7)
- References section (2+ external links)

**Parameters**: Same as Draft Agent

**Output**: Refined content (markdown with frontmatter)

### Step 4: Save & Mark Complete

```yaml
---
title: "Post Title"
date: 2026-01-23T18:00:00+09:00  # KST timezone
categories: ["tech"]
tags: ["keyword1", "keyword2"]
description: "120-160 char meta description"
image: "https://images.unsplash.com/photo-..."
imageCredit: "Photo by [Name](https://unsplash.com/@username)"
lang: "en"
---

Content here...

## References
1. [Source 1](https://example.com)
2. [Source 2](https://example.com)
```

**File Location**: `content/{lang}/{category}/{date}-{slug}.md`

**Queue Update**: Move `in_progress` → `completed`

---

## Quality Validation

### Automated Checks (quality_gate.py)

```bash
# Run quality gate
python scripts/quality_gate.py

# View results
cat quality_report.json
```

**Checks**:
1. ✅ Word count (within range)
2. ✅ No AI phrases (blacklist)
3. ✅ Meta description (120-160 chars)
4. ✅ References section exists (2+ links)
5. ⚠️ Image exists (warning only)
6. ✅ Frontmatter valid YAML

**Exit code**:
- `0` - All checks passed
- `1` - Critical failures (blocks deployment)

### Optional AI Review

```bash
# Run AI reviewer (5-criteria scoring)
python scripts/ai_reviewer.py

# View results
cat ai_review_report.json
```

**Criteria** (1-10 scale):
- Authenticity (human tone)
- Value (practical insights)
- Engagement (structure)
- Technical Accuracy
- SEO Quality

**Recommendation**:
- **≥ 8.0**: APPROVE
- **6.0-7.9**: REVISE
- **< 6.0**: REJECT

---

## Common Issues & Solutions

### Issue 1: Word count too low

**Error**: `Word count 650 below minimum 800`

**Solution**: Increase `max_tokens` in `generate_posts.py`
```python
# Line ~1100
max_tokens=12000  # Increase to 14000 if needed
```

### Issue 2: AI phrases detected

**Error**: `Found blacklisted phrase: "revolutionary"`

**Solution**: Update system prompt
```python
# In generate_posts.py, add to prompt:
"Never use these words: revolutionary, game-changer, cutting-edge"
```

### Issue 3: Queue stuck

**Symptom**: Topics stay in `in_progress` for hours

**Solution**:
```bash
# View stuck topics
python scripts/topic_queue.py stats

# Reset (24+ hours)
python scripts/topic_queue.py cleanup 24
```

### Issue 4: Missing references

**Error**: `No References section found`

**Solution**: Editor agent already includes this, but verify prompt:
```python
# In generate_posts.py, Editor agent section:
"Ensure ## References section with 2+ external links"
```

---

## Categories

**Valid categories** (8 total):
- tech
- business
- lifestyle
- society
- entertainment
- sports
- finance
- education

**To add new category**:
1. Update `hugo.toml` (menu items for EN/KO/JA)
2. Update `scripts/utils/validation.py` (VALID_CATEGORIES)
3. Create directories: `content/{en,ko,ja}/{category}/`

---

## Cost Optimization

### Claude API

- **Cost per post**: ~$0.09 (with prompt caching)
- **Daily cost**: $0.27 (3 posts/day × 3 runs)
- **Monthly cost**: ~$8.10

**Optimizations**:
- ✅ Prompt caching enabled (20-25% reduction)
- ✅ `max_tokens=12000` (prevents truncation, minimizes retries)
- ✅ Structure-based prompts (not strict word counts)

### Unsplash API

- **Free tier**: 50 requests/hour
- **Usage**: 9 requests/day (3 posts × 3 languages)
- **Cost**: $0/month

---

## Testing

### Local Test

```bash
# Set API key
export ANTHROPIC_API_KEY='your-key'

# Generate 1 post
python scripts/generate_posts.py --count 1

# Check quality
python scripts/quality_gate.py

# Preview
/opt/homebrew/bin/hugo server -D
# Visit http://localhost:1313
```

### CI/CD Pipeline

**GitHub Actions** (`.github/workflows/daily-content.yml`):
- **Schedule**: 6 AM, 12 PM, 6 PM KST
- **Steps**: pytest → generate → quality gate → create PR
- **Manual trigger**: Actions tab → Run workflow

**Delays**: 15-60 min normal (GitHub Actions scheduler)

---

## Advanced Usage

### Custom Prompts

Edit system prompts in `scripts/generate_posts.py`:

**English** (lines ~63-450):
```python
ENGLISH_DRAFT_PROMPT = """
You are writing for Medium-style tech blog...
[customize here]
"""
```

**Korean** (lines ~450-850):
```python
KOREAN_DRAFT_PROMPT = """
토스 블로그 스타일로 작성...
[customize here]
"""
```

**Japanese** (lines ~850-1250):
```python
JAPANESE_DRAFT_PROMPT = """
日本のテックブログ風に...
[customize here]
"""
```

### Affiliate Links

**Auto-detection** (in `scripts/affiliate_config.py`):
- Product mentions detected
- Affiliate links generated
- Inserted naturally in content

**Supported**:
- Amazon
- Coupang (Korea)
- Rakuten (Japan)

---

## Related Skills

- **quality-validation**: Run quality checks
- **hugo-operations**: Build and preview
- **keyword-curation**: Add topics to queue

---

## References

- **Architecture**: `.claude/docs/architecture.md`
- **Quality Standards**: `.claude/docs/quality-standards.md`
- **Troubleshooting**: `.claude/docs/troubleshooting.md`
- **Commands**: `.claude/docs/commands.md`

---

**Skill Version**: 1.0
**Last Updated**: 2026-01-23
**Maintained By**: Jake's Tech Insights project
