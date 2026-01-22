# Automation Strategy

**Project**: Jake's Tech Insights
**Last Updated**: 2026-01-20
**Status**: Phase 1 Complete (Content Generation)

---

## Overview

### Goal
**Automated daily content generation** across 3 languages and 3 categories.

### Target Output
- **Daily**: 9 posts (3 categories × 3 languages)
- **Monthly**: 270 posts
- **Quality**: Human-level, SEO-optimized

---

## Architecture

### Current Implementation (GitHub Actions)

```yaml
# .github/workflows/daily-content.yml
name: Daily Content Generation

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:      # Manual trigger

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - Checkout code
      - Setup Python
      - Install dependencies
      - Run generation script
      - Commit & push changes
```

**Advantages**:
- ✅ Completely free (2,000 min/month)
- ✅ Git-integrated
- ✅ Code-based control
- ✅ Transparent logs
- ✅ Auto-deploys to Cloudflare

**Limitations**:
- ❌ No GUI
- ❌ Limited real-time monitoring

---

## Content Generation Pipeline

### 1. Topic Queue System
**File**: `scripts/topic_queue.py`

**State Machine**:
```
pending → in_progress → completed
         ↓ (on failure)
       pending (retry++)
```

**Features**:
- Priority-based selection
- Automatic retry on failure
- Stuck topic cleanup (24h+ auto-reset)
- Statistics tracking

**Usage**:
```bash
python scripts/topic_queue.py stats     # View queue status
python scripts/topic_queue.py cleanup   # Reset stuck topics
python scripts/topic_queue.py reserve 3 # Reserve 3 topics
```

---

### 2. Content Generation
**File**: `scripts/generate_posts.py`

**Two-Stage Process**:

#### Stage 1: Draft Generation
- Model: Claude Sonnet 4.5
- Input: Topic + Language + Category
- Output: Initial draft (1,200+ words)

#### Stage 2: Editorial Review
- Model: Claude Sonnet 4.5
- Input: Draft from Stage 1
- Output: Polished, SEO-optimized post

**Quality Controls**:
- Natural tone (no AI clichés)
- Specific examples with names/data
- Proper structure (3-5 H2 sections)
- SEO optimization
- Meta description generation

**Usage**:
```bash
export ANTHROPIC_API_KEY='your-key'
python scripts/generate_posts.py --count 3
python scripts/generate_posts.py --topic-id specific-topic
```

---

### 3. Quality Gate (Coming Soon)
**File**: `scripts/quality_gate.py` (planned)

**Checks**:
- [ ] Minimum word count (800+)
- [ ] Proper frontmatter
- [ ] SEO description present
- [ ] No AI-obvious phrases
- [ ] Readability score
- [ ] Duplicate content detection

---

### 4. AI Reviewer (Coming Soon)
**File**: `scripts/ai_reviewer.py` (planned)

**Reviews**:
- [ ] Content quality
- [ ] Factual accuracy
- [ ] Tone consistency
- [ ] SEO optimization
- [ ] Human-like writing

---

## Cost Analysis

### Claude API (Company Account)
```
Daily: 9 posts × ~50K tokens/post = 450K tokens
Monthly: 13.5M tokens

With Prompt Caching (90% savings):
- Cost: $60-90/month (personal account)
- Cost: $0 (company API)
```

### Infrastructure
- **GitHub Actions**: $0 (free tier: 2,000 min/month)
- **Cloudflare Pages**: $0 (free)
- **Total**: $0 with company API

---

## Quality Strategy

### AI Content Risks
**Google's Helpful Content Update (2023+)**:
- ❌ Simple AI-generated content → Penalty
- ❌ Scraped/reprocessed → Thin content rejection
- ❌ Hundreds of auto-posts/month → Obvious automation

### Quality Assurance Methods

#### A. High-Quality Prompts
```python
SYSTEM_PROMPT = """
You are a professional writer for Jake's Tech Insights.

[Writing Principles]
1. First paragraph: Empathize with reader's pain point
2. Structure: Problem → Solution → Tips → Conclusion
3. Tone: Professional but friendly, advisory
4. Length: 1,200-1,500 words
5. SEO: Keyword "{keyword}" naturally 5-7 times
6. Sections: 3-5 H2 headings
7. End: CTA - question or next step

[Style]
- Active voice
- Short sentences (2 lines max)
- Specific numbers/examples
- Use bullet points

[Forbidden]
- AI tells: "of course", "importantly"
- Vague: "revolutionary", "game-changer"
- Excessive emojis
"""
```

#### B. Multi-Agent Chain
```
1. Research Agent: Gather latest info (Google Trends, Reddit API)
2. Draft Agent: Write with style guide (Claude + Prompt Caching)
3. SEO Agent: Check keyword density, meta tags
4. Proofreading Agent: Grammar, duplication, AI feel removal
5. Humanizer Agent: Add personal touches
```

#### C. Human Proofreading (10 min/post)
```
Checklist:
□ Title clickable?
□ First paragraph interesting?
□ Fix 1-2 awkward sentences
□ Add 1 line of personal opinion
□ Add 1 image (Unsplash)
□ Publish

9 posts × 10 min = 90 min/day
```

---

## Writing Style Learning

### Method A: Few-Shot Learning (Current)
- Collect 5-10 posts written by Jake
- Analyze with Claude → Generate Style Guide
- Include Style Guide in every prompt

### Method B: Prompt Caching (Recommended)
```python
STYLE_GUIDE = """
Jake's Writing DNA:

[Sentence Structure]
- Average length: 12-18 words
- Question frequency: 1 per paragraph
- Active voice: 85%

[Vocabulary]
- Common verbs: recommend, consider, check
- Avoid: revolutionary, disruptive
- Signature phrases: "you know", "how about", "first"

[Structure]
1. Empathy question
2. 3-5 sections
3. Each section: Concept → Example → Action
4. Ending: Reader question

[Tone]
- Formality: 6/10
- Enthusiasm: 7/10
- Technical: 7/10
"""

# 90% token savings with Prompt Caching
response = client.messages.create(
    model="claude-sonnet-4",
    system=[
        {
            "type": "text",
            "text": STYLE_GUIDE,
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[...]
)
```

**Implementation Timeline**:
```
Week 1: Jake writes 5-10 posts manually
Week 2: Generate Style Guide with Claude
Week 3: Test & iterate
Week 4: Full automation
```

### Method C: Fine-Tuning (Future)
- GPT-4 Fine-tuning: $8/M tokens (training)
- Claude: Not yet supported
- Requires 50-100 sample posts

---

## Keyword Sourcing

### Recommended: Long-Tail Keywords

**Why NOT Trending Keywords**:
- ❌ Too competitive
- ❌ Dominated by major media
- ❌ New blogs disadvantaged

**Why Long-Tail Keywords**:
- ✅ Lower competition
- ✅ Specific intent
- ✅ Higher conversion

### Keyword Sources

#### 1. Reddit API (Free)
```python
import praw

reddit = praw.Reddit(...)
subreddit = reddit.subreddit("technology")
for post in subreddit.hot(limit=10):
    if post.score > 500:
        keywords.append(post.title)
```

#### 2. Google Trends API
```python
from pytrends.request import TrendReq

pytrends = TrendReq()
pytrends.build_payload(['startup funding'], timeframe='today 7-d')
trends = pytrends.interest_over_time()
```

#### 3. YouTube Data API
```python
# Analyze high-view video comments
# Extract "how to..." question patterns
```

#### 4. Answer The Public (Free: 2 searches/day)
- Real search query data
- Question-format keywords

---

## Gradual Scaling Strategy

### ⚠️ WARNING: Don't Start with 9 Posts/Day

**Risks**:
- Google penalty
- AdSense rejection
- Traffic-less content pile-up

### ✅ Recommended: Gradual Expansion

```
Month 1-3: 1-2 posts/day (manual quality)
Month 4-6: 3-5 posts/day (semi-automated)
Month 7+:   9 posts/day (full automation)
```

---

## Implementation Timeline

### Phase 1: Foundation ✅
- [x] Site structure complete
- [x] Category system
- [x] Multilingual support
- [x] Bug fixes
- [x] Topic queue system
- [x] Content generation script

### Phase 2: Automation (In Progress)
- [ ] Style Guide generation
- [ ] GitHub Actions workflow
- [ ] Quality gate implementation
- [ ] AI reviewer implementation
- [ ] Error notification system

### Phase 3: Optimization (Future)
- [ ] Prompt Caching integration
- [ ] Image auto-generation (DALL-E)
- [ ] Auto SEO meta generation
- [ ] A/B testing

---

## Alternative Architecture (Future Consideration)

### n8n + GitHub Actions
```
n8n (Self-hosted: $5/month)
  ├─ Keyword Research (Reddit/Google Trends)
  ├─ Workflow management
  ├─ Error notifications (Slack/Email)
  └─ Webhook → Trigger GitHub Actions

GitHub Actions
  ├─ Run Python scripts
  ├─ Call Claude API (9 drafts)
  └─ Git commit & push
```

**Advantages**:
- ✅ Visual workflow
- ✅ Error handling GUI
- ✅ Slack notifications
- ✅ Heavy tasks offloaded to GitHub

**Disadvantages**:
- ❌ n8n server cost ($5-20/month)
- ❌ Complex initial setup

---

## References

- GitHub Actions Documentation: https://docs.github.com/actions
- Claude API: https://docs.anthropic.com/
- Prompt Caching: https://docs.anthropic.com/claude/docs/prompt-caching
