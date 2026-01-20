# Jake's Tech Insights - Automation Setup Context

> Last Updated: 2026-01-20
> Status: ✅ All automation systems operational + Security hardening complete

## Executive Summary

Complete automation system for multilingual tech blog generating 9 posts/day across 8 categories using Google Trends RSS and Custom Search API.

**Daily Operations:**
- 17:05 KST: Curate 20 trending keywords (3-day expiry)
- 18:10 KST: Generate 3 posts
- 06:00 KST: Generate 3 posts
- 12:00 KST: Generate 3 posts

---

## 1. System Architecture

### Categories (8 Total)
- Tech 💻
- Business 💼
- Society 🌍
- Entertainment 🎬
- Lifestyle 🌱
- Sports ⚽ (NEW)
- Finance 💰 (NEW)
- Education 📖 (NEW)

### Languages (3 Total)
- English (en-us)
- Korean (ko-kr)
- Japanese (ja-jp)

### Content Pipeline
```
Google Trends RSS → Keyword Curator → Topic Queue → Post Generator → Hugo Site
     (KR/US/JP)        (Claude API)      (JSON)      (Claude + Unsplash)   (Static)
```

---

## 2. Key Files Reference

### Configuration
- **[hugo.toml](../hugo.toml)**: Site config with 8 categories × 3 languages navigation
- **[daily-keywords.yml](../.github/workflows/daily-keywords.yml)**: Keyword curation automation (17:05 KST)
- **[daily-content.yml](../.github/workflows/daily-content.yml)**: Content generation automation (3x daily)

### Python Scripts
- **[keyword_curator.py](../scripts/keyword_curator.py)**: Fetches RSS trends, curates 20 keywords with Claude
- **[generate_posts.py](../scripts/generate_posts.py)**: Generates multilingual posts with Unsplash images
- **[cleanup_expired.py](../scripts/cleanup_expired.py)**: Removes trends older than 3 days
- **[topic_queue.py](../scripts/topic_queue.py)**: Queue management utilities

### Security & Validation (NEW - 2026-01-20)
- **[utils/security.py](../scripts/utils/security.py)**: API key masking for logs (`safe_print`, `mask_secrets`)
- **[utils/validation.py](../scripts/utils/validation.py)**: Input validation (path traversal prevention, length checks)
- **[utils/validate_queue.py](../scripts/utils/validate_queue.py)**: Queue validation script

### Data Files
- **[topics_queue.json](../data/topics_queue.json)**: Pending/in-progress/completed keywords
- **[used_images.json](../data/used_images.json)**: Track Unsplash image IDs to prevent duplication

### Layouts
- **[index.html](../layouts/index.html)**: Homepage with floating category widget (lines 639-971)
- **[all-posts.html](../layouts/_default/all-posts.html)**: All posts page with 8-category filters

---

## 3. Critical Implementation Details

### RSS Trending Integration
**File**: [keyword_curator.py](../scripts/keyword_curator.py) (lines 199-233)

```python
def fetch_trending_from_rss(self) -> List[str]:
    """Fetch trending topics from Google Trends RSS feeds"""
    rss_urls = {
        "KR": "https://trends.google.co.kr/trending/rss?geo=KR",
        "US": "https://trends.google.co.kr/trending/rss?geo=US",
        "JP": "https://trends.google.co.kr/trending/rss?geo=JP"
    }

    trending_queries = []
    for geo, url in rss_urls.items():
        # Fetch top 10 from each region (30 total input)
        # Parse XML and extract titles
```

### Image Deduplication System
**File**: [generate_posts.py](../scripts/generate_posts.py) (lines 800-866)

**Keyword-Based Image Search** (lines 800-866):
```python
# Translation dictionary for meaningful keywords
keyword_translations = {
    # Korean
    '나라사랑카드': 'patriot card credit card',
    '카드': 'card credit',
    '연령': 'age limit',
    '전세': 'housing lease deposit',
    '배달': 'delivery food',
    # Japanese
    '奨学金': 'scholarship student loan',
    '投資': 'investment financial',
    # ... more translations
}

# Extract meaningful keywords from title and translate
for ko_word, en_translation in keyword_translations.items():
    if ko_word in clean_keyword:
        translated_keywords.append(en_translation)

# Build flexible, contextual query
base_keywords = ' '.join(translated_keywords[:2])
context = category_context.get(category, category)
query = f"{base_keywords} {context}".strip()

# Search Unsplash with contextual keywords
```

**Image Tracking** (lines 868-900):
```python
# Load previously used image IDs from JSON
used_images = set(json.load(open('data/used_images.json')))

# Find first unused image from Unsplash results
for result in data['results']:
    if result['id'] not in used_images:
        photo = result
        used_images.add(result['id'])
        break

# Fallback: Random from top 5 if all used
if photo is None:
    photo = random.choice(data['results'][:5])

# Save updated tracking file
json.dump(list(used_images), open('data/used_images.json', 'w'))
```

**File**: [daily-content.yml](../.github/workflows/daily-content.yml) (line 91)
```yaml
git add data/used_images.json  # Commit tracking file to persist across runs
```

**Benefits of Keyword-Based Search**:
- Images are contextually relevant to post topic (not just generic category images)
- Reduced duplication rate (diverse search queries = diverse image pool)
- "나라사랑카드" → searches "credit card" instead of generic "business"
- "전세보증금" → searches "housing lease deposit" instead of generic "finance"

### Keyword Expiry Management
**File**: [keyword_curator.py](../scripts/keyword_curator.py) (line 575)

```python
if topic['keyword_type'] == 'trend':
    topic['expiry_days'] = 3  # Auto-cleanup after 3 days (code default)
```

**File**: [cleanup_expired.py](../scripts/cleanup_expired.py) (lines 16-75)
- **Daily workflow uses**: `cleanup_expired.py 1` (1 day expiry)
- Removes pending trends older than 1 day (fresh daily rotation)
- Does NOT touch in_progress/completed keywords
- Does NOT touch evergreen keywords

### Google Custom Search Integration
**File**: [generate_posts.py](../scripts/generate_posts.py) (lines 679-764)

```python
# Search with date filter: last 7 days, sorted by date
params = {
    'key': GOOGLE_API_KEY,
    'cx': GOOGLE_CX,
    'q': search_query,
    'dateRestrict': 'd7',
    'sort': 'date',
    'num': 5
}

# Rate limit: 100 queries/day
# Used for keyword curation: ~20 topics × 5 refs = 100 queries/day
# Content generation uses 0 Google API queries (only Claude API)
```

### Floating Widget Grid Layout
**File**: [index.html](../layouts/index.html) (lines 639-971)

**CSS** (lines 639-668):
```css
.category-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;  /* 2 columns */
    gap: 0.25rem;
}

.category-grid a {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.72rem;
}

.category-grid .cat-icon {
    flex-shrink: 0;  /* Prevent icon wrapping */
    width: 1.1em;
    text-align: center;
}

.category-grid .cat-text {
    flex: 1;
    white-space: nowrap;  /* Keep text on same line */
}
```

**HTML Structure** (lines 951-971):
```html
<div class="category-grid">
  <a href="/categories/tech/">
    <span class="cat-icon">💻</span>
    <span class="cat-text">Tech</span>
  </a>
  <a href="/categories/business/">
    <span class="cat-icon">💼</span>
    <span class="cat-text">Business</span>
  </a>
  <!-- ... 6 more categories ... -->
</div>
```

### Security Hardening (2026-01-20)

**Secrets Masking** - All scripts now use `safe_print()`:
```python
from utils.security import safe_print, mask_secrets

# Automatically masks API keys in output
safe_print(f"API Error: {response}")
# Output: API key ***MASKED_API_KEY*** is invalid
```

**Input Validation** - All external inputs validated:
```python
from utils.validation import validate_keyword, validate_category

# Prevents path traversal, injection attacks
error = validate_keyword("../../etc/passwd")
# Returns: "Keyword contains invalid characters"
```

**GitHub Actions Masking** - Explicit secret masking in workflows:
```yaml
run: |
  echo "::add-mask::${{ secrets.ANTHROPIC_API_KEY }}"
  echo "::add-mask::${{ secrets.UNSPLASH_ACCESS_KEY }}"
```

---

## 4. Automation Schedule Details

### Daily Keyword Curation
**File**: [daily-keywords.yml](../.github/workflows/daily-keywords.yml)

```yaml
schedule:
  - cron: '5 8 * * *'  # 17:05 KST (08:05 UTC)

# Generates 20 keywords with 3-day expiry
# Uses trending topics from RSS as input
```

### Daily Content Generation
**File**: [daily-content.yml](../.github/workflows/daily-content.yml)

```yaml
schedule:
  - cron: '10 9 * * *'   # 18:10 KST (1hr after keywords)
  - cron: '0 21 * * *'   # 06:00 KST (next morning)
  - cron: '0 3 * * *'    # 12:00 KST (noon)

# Each run generates 3 posts (1 per language)
# Total: 9 posts/day across all categories
```

### Typical Daily Flow
```
17:05 - Fetch 30 RSS trends → Claude curates 20 keywords → Save to queue
18:10 - Pick 3 keywords → Generate EN/KO/JA posts → Fetch images → Deploy
06:00 - Pick 3 keywords → Generate EN/KO/JA posts → Fetch images → Deploy
12:00 - Pick 3 keywords → Generate EN/KO/JA posts → Fetch images → Deploy
17:05 - Cleanup expired trends → Curate 20 new keywords → Repeat
```

---

## 5. GitHub Secrets Required

Must be configured in repository settings:

| Secret Name | Purpose | Usage Limit |
|------------|---------|-------------|
| `ANTHROPIC_API_KEY` | Claude API for content generation | Prompt caching enabled |
| `UNSPLASH_ACCESS_KEY` | Fetch blog post images | 50 requests/hour |
| `GOOGLE_API_KEY` | Custom Search API for references | 100 queries/day |
| `GOOGLE_CX` | Custom Search Engine ID | - |

**Verification Command**:
```bash
# Check if secrets are configured (run in Actions)
echo "ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY:0:10}..."
echo "GOOGLE_API_KEY: ${GOOGLE_API_KEY:0:10}..."
echo "GOOGLE_CX: ${GOOGLE_CX}"
```

---

## 6. Important Design Decisions

### Why 3-Day Expiry for Trends?
Trending topics become stale quickly. 3-day expiry ensures queue stays fresh with current events while allowing enough time for content generation across all schedules.

### Why 2-Column Grid Layout?
With 8 categories, a single column would make the floating widget too tall. 2-column grid keeps it compact while maintaining readability on desktop screens.

### Why Separate RSS Fetch + Curation?
RSS provides ~30 raw trending queries. Claude API curates these into 20 well-distributed, unique keywords across 8 categories with proper Korean/English/Japanese terminology.

### Why Track Used Images Persistently?
Unsplash returns similar results for similar queries. Without persistent tracking across workflow runs, we'd see duplicate images within days.

### Why 1-Hour Buffer After Keywords?
Daily-content workflow runs 1 hour after daily-keywords to ensure fresh keywords are available in the queue before post generation starts.

---

## 7. Common Issues & Solutions

### Issue: API Key Not Found
**Error**: `ANTHROPIC_API_KEY not found`
**Solution**: Verify GitHub Secrets are configured in repository settings

### Issue: Image Duplication
**Symptom**: Same Unsplash image appearing on multiple posts
**Solution**: Check [used_images.json](../data/used_images.json) is being committed after each run

### Issue: Category Filter Not Working
**Location**: [all-posts.html](../layouts/_default/all-posts.html) (line 410)
**Check**: Ensure new categories are in the `where .Type "in"` slice

### Issue: Floating Widget Overflow
**Location**: [index.html](../layouts/index.html) (lines 639-668)
**Solution**: Adjust `grid-template-columns` to `1fr 1fr 1fr` for 3-column layout if needed

### Issue: Expired Keywords Not Cleaning Up
**Check**: [cleanup_expired.py](../scripts/cleanup_expired.py) runs before keyword curation
**Verify**: [daily-keywords.yml](../.github/workflows/daily-keywords.yml) includes cleanup step

---

## 8. Recent Changes Log

### 2026-01-20 (Morning): Floating Widget Bug Fix
- **Bug Report**: Article landing pages showed incorrect 4x4 grid instead of 2x4 grid with all 8 categories
  - Homepage floating widget worked correctly (2x4 grid with 8 categories)
  - Article pages (single.html) only showed 5 categories without grid CSS
  - Missing categories: Sports ⚽, Finance 💰, Education 📖

- **Root Cause**: Template inconsistency between index.html and single.html
  - [index.html](../layouts/index.html) had complete grid CSS and all 8 categories
  - [single.html](../layouts/_default/single.html) only had 5 categories hardcoded, no grid CSS

- **Solution**: Updated [single.html:233-285](../layouts/_default/single.html)
  - Lines 233-266: Added 2-column grid CSS matching index.html
    * `.category-grid { display: grid; grid-template-columns: 1fr 1fr; }`
    * Flexbox alignment for icon + text (`.cat-icon`, `.cat-text`)
  - Lines 267-285: Added all 8 categories with language-specific URLs
    * English: `/categories/tech/`, `/categories/business/`, etc.
    * Korean/Japanese: `/ko/categories/tech/`, `/ja/categories/tech/`, etc.

- **Deployment**: Cloudflare Pages automatic deployment
  - Committed changes (d229e54)
  - Cloudflare automatically builds with Hugo on git push
  - **IMPORTANT**: Local Hugo server NOT needed (Cloudflare handles build)

- **Lesson Learned**: Never try to run local Hugo server
  - Project is deployed on Cloudflare Pages (serverless build)
  - Workflow: Edit files → Git commit → Push → Cloudflare auto-builds
  - Claude previously made same mistake (trying to run local Hugo)
  - User reminder: "전에도 한 번 로컬서버 시도했었는데 니가 필요없다고 했었어"

### 2026-01-20 (Early Morning): References Null Issue Root Cause Fix
- **Problem Diagnosis**: All 45 keywords had `references: null` despite Google API working
  - Root cause: Claude was reinterpreting RSS queries into different keywords
  - Example: RSS Query "서수남" (singer) → Claude keyword "독립기념관 관장 해임 후폭풍" (different news)
  - Matching failed: {"독립기념관", "관장", "해임", "후폭풍"} ∩ {"서수남"} = {} (empty set)
  - Result: `references = []` → `null` in JSON

- **Solution**: Modified [keyword_curator.py](../scripts/keyword_curator.py) prompt
  - Lines 30-47: Added "Use Query as-is for keyword. Never reinterpret or rewrite"
  - Lines 54-55: Enforce keyword = raw_search_title = Query (identical)
  - Lines 84-85: Emphasized exact Query usage without reinterpretation
  - Now: RSS Query "서수남" → Claude keyword "서수남" (no reinterpretation)
  - Matching succeeds: {"서수남"} ∩ {"서수남"} = {"서수남"} ✓

- **Google API Quota Optimization**: Reduced from 105 to 30 queries/day
  - [keyword_curator.py:201](../scripts/keyword_curator.py): RSS 7 → 5 per region (21 → 15 keywords)
  - [keyword_curator.py:267](../scripts/keyword_curator.py): Search results 5 → 2
  - [keyword_curator.py:372](../scripts/keyword_curator.py): References stored 3 → 2
  - [keyword_curator.py:16, 272-273](../scripts/keyword_curator.py): Added rate limiting (time.sleep(1.0))
  - [daily-keywords.yml:45](../.github/workflows/daily-keywords.yml): COUNT default 20 → 15
  - Final: 15 keywords × 2 results = 30 queries/day (70% quota remaining)

- **Keyword Type Enforcement**: 100% trend keywords only
  - [keyword_curator.py:70-71](../scripts/keyword_curator.py): Forced trend-only generation in prompt
  - Removed evergreen keyword generation completely

### 2026-01-19 (Evening Continued): URL Validation for Fake References
- **URL Validation System**: Added automatic detection and removal of fake reference URLs
  - Created `has_fake_reference_url()` function in [generate_posts.py:1033-1047](../scripts/generate_posts.py)
  - Detects patterns: example.com, .gov/[text]-202X, .org/[text]-survey, .gov/[text]-compliance
  - Automatically removes entire References section if fake URLs detected
  - Prevents Claude API from generating plausible-looking but non-existent URLs
  - Tested with 7 test cases including real IRS, GitHub, Unsplash URLs
- **Manual Cleanup**: Removed fake references from 4 existing posts
  - Cryptocurrency Tax Trap 2026: 3 fake .gov URLs
  - MLK Day Market Closure: Fixed missing image (added 166KB cryptocurrency image)
  - Japanese lifestyle post: 3 example.com URLs
  - AI Supercomputing Platform: 3 example.com URLs

### 2026-01-19 (Evening): Image Search & References Improvements
- **Keyword-Based Image Search**: Changed from generic category queries to contextual keyword extraction
  - Added Korean/Japanese → English translation dictionary
  - Example: "나라사랑카드" → "credit card" instead of generic "business"
  - Significantly reduced image duplication risk
- **References Section**: Changed to optional (skip if not present, no fake URLs)
  - Removed fake example.com references from 11 existing posts
  - Now only adds References section if Claude API provides real sources
- **Image Tracking**: Fixed used_images.json to properly track all Unsplash IDs
  - Created fix_duplicate_images.py to extract IDs from existing posts
  - Updated from 19 → 58 unique tracked IDs

### 2026-01-19 (Morning): Category Expansion & RSS Integration
- Added 3 new categories (Sports, Finance, Education)
- Integrated Google Trends RSS feeds (KR/US/JP)
- Implemented image deduplication tracking
- Changed keyword expiry from 21 days → 3 days
- Restructured floating widget to 2-column grid layout
- Fixed icon/text alignment with explicit span wrappers
- Updated all layouts and navigation for 8 categories

### Previous: Initial Automation Setup
- Hugo multilingual site structure
- Claude API integration with prompt caching
- Unsplash image fetching
- Google Custom Search API for references
- GitHub Actions automation workflows

---

## 9. File Path Quick Reference

```
jakes-tech-insights/
├── .github/workflows/
│   ├── daily-keywords.yml       # Keyword curation (17:05 KST)
│   └── daily-content.yml        # Content generation (3x daily)
├── content/
│   ├── en/                      # English posts
│   ├── ko/                      # Korean posts
│   └── ja/                      # Japanese posts
├── data/
│   ├── topics_queue.json        # Keyword queue with status
│   └── used_images.json         # Unsplash image tracking
├── docs/
│   └── AUTOMATION_CONTEXT.md    # This file
├── layouts/
│   ├── index.html               # Homepage + floating widget
│   └── _default/all-posts.html  # All posts with filters
├── scripts/
│   ├── keyword_curator.py       # RSS → Claude → Queue
│   ├── generate_posts.py        # Queue → Posts + Images
│   ├── cleanup_expired.py       # Remove old trends
│   ├── fix_duplicate_images.py  # Extract Unsplash IDs from posts
│   └── topic_queue.py           # Queue utilities
└── hugo.toml                    # Site configuration
```

---

## 10. Testing & Validation

### Manual Workflow Trigger
```bash
# Test keyword curation
gh workflow run daily-keywords.yml -f count=5

# Test content generation
gh workflow run daily-content.yml -f count=3
```

### Local Testing
```bash
# Test keyword curator
cd scripts
export ANTHROPIC_API_KEY="your-key"
python keyword_curator.py --count 5

# Test post generator
export GOOGLE_API_KEY="your-key"
export GOOGLE_CX="your-cx"
export UNSPLASH_ACCESS_KEY="your-key"
python generate_posts.py --count 3

# Preview site locally
hugo server -D
```

### Verification Checklist
- [ ] All 8 categories appear in navigation (EN/KO/JA)
- [ ] Floating widget shows 2-column grid with aligned icons
- [ ] All-posts page has 8 filter buttons
- [ ] [topics_queue.json](../data/topics_queue.json) populates with trending keywords
- [ ] [used_images.json](../data/used_images.json) grows with each post
- [ ] Posts include 5 Google Search references
- [ ] GitHub Actions run on schedule without errors

---

## Contact & Maintenance

**Project Owner**: Jake Park
**Repository**: jakes-tech-insights
**Deployment**: Cloudflare Pages (https://jakes-tech-insights.pages.dev)

**For Issues**:
1. Check GitHub Actions logs
2. Verify API keys in repository secrets
3. Review [topics_queue.json](../data/topics_queue.json) for keyword status
4. Check [used_images.json](../data/used_images.json) for image tracking

---

**Last Verified**: 2026-01-20
**Next Review**: When adding new categories or changing automation schedule

## Pending Verification (2026-01-20)

### At 17:05 KST (Daily Keywords Workflow)
- [ ] Workflow runs without errors
- [ ] Generates exactly 15 keywords
- [ ] All keywords have `references` (not null)
- [ ] Keywords match RSS queries exactly (no reinterpretation)
- [ ] Google API uses exactly 30 queries (check Cloud Console)
- [ ] No 429 (Too Many Requests) errors

### At 18:00 KST (Daily Content Workflow)
- [ ] Posts generated successfully
- [ ] References section properly included (when available)
- [ ] Fake URL validation working (removes bad URLs)
- [ ] Images contextually relevant to keywords
