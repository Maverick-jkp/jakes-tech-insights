---
name: keyword-curation
description: Google Trends-based keyword research and topic queue state management (pending → in_progress → completed). Use when curating new keywords from Google Trends (KR/US/JP), adding topics to queue, checking queue status, or fixing stuck topics. Includes duplicate prevention and priority management (1-10 scale).
---

# Keyword Curation Skill

Google Trends-based keyword research and topic queue state management for content generation.

---

## When to Use This Skill

**Activate this skill when:**
- User requests "keywords", "topic queue", "curate keywords", or "add topic"
- Need to fetch trending keywords from Google Trends
- Managing topic queue (check status, add/remove topics)
- Fixing stuck topics (in_progress for 24+ hours)
- Checking queue health (pending count, priority distribution)

**Do NOT use this skill for:**
- Generating content from keywords → Use `content-generation` skill
- Validating content quality → Use `quality-validation` skill
- Hugo operations → Use `hugo-operations` skill

**Examples:**
- "Curate new keywords"
- "Add topic to queue"
- "Check queue status"
- "Fix stuck topics"

---

## Skill Boundaries

**This skill handles:**
- ✅ Google Trends keyword fetching (KR/US/JP)
- ✅ Topic queue state management (pending/in_progress/completed)
- ✅ Manual topic addition with priority
- ✅ Stuck topic cleanup (24+ hours)
- ✅ Queue health monitoring
- ✅ Duplicate prevention

**Defer to other skills:**
- ❌ Content generation → Use `content-generation` skill
- ❌ Quality validation → Use `quality-validation` skill
- ❌ Hugo operations → Use `hugo-operations` skill
- ❌ Automated curation → GitHub Actions workflow

---

## Quick Start

```bash
# View queue status
python scripts/topic_queue.py stats

# Curate new keywords (manual filtering required)
python scripts/keyword_curator.py --count 15

# Add topic manually
python3 << 'EOF'
import sys
from pathlib import Path
sys.path.insert(0, str(Path('scripts')))
from topic_queue import add_topic

add_topic(
    keyword="AI trends 2026",
    category="tech",
    language="en",
    priority=8
)
EOF

# Fix stuck topics
python scripts/topic_queue.py cleanup 24
```

---

## Topic Queue State Machine

### States

```
pending → in_progress → completed
             ↓
           failed (retry)
```

1. **pending** - Ready to be processed (default)
2. **in_progress** - Currently generating (reserved by `reserve_topics()`)
3. **completed** - Successfully published
4. **failed** - Generation failed (will auto-retry)

### File Structure

**Location**: `data/topics_queue.json`

**Format**:
```json
{
  "topics": [
    {
      "id": "uuid-1234",
      "keyword": "AI trends 2026",
      "category": "tech",
      "language": "en",
      "priority": 8,
      "status": "pending",
      "created_at": "2026-01-23T18:00:00+09:00",
      "updated_at": "2026-01-23T18:00:00+09:00"
    }
  ]
}
```

---

## Queue Operations

### View Status

```bash
# Show statistics
python scripts/topic_queue.py stats

# Sample output:
# Total topics: 74
# Pending: 14
# In progress: 0
# Completed: 60
# Failed: 0
```

### Add Topic

**Method 1: Python script**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('scripts')))
from topic_queue import add_topic

add_topic(
    keyword="Your Keyword",
    category="tech",  # or business, lifestyle, etc.
    language="en",    # or ko, ja
    priority=8        # 1-10 (10 = highest)
)
```

**Method 2: Keyword curator** (recommended)
```bash
# Fetch from Google Trends + manual filtering
python scripts/keyword_curator.py --count 15
```

### Reserve Topics

**Automatic** (done by `generate_posts.py`):
```python
from topic_queue import reserve_topics

# Get top 3 pending topics
topics = reserve_topics(count=3)

# Moves pending → in_progress
# Returns: [topic1, topic2, topic3]
```

### Mark Completed

**Automatic** (done by `generate_posts.py`):
```python
from topic_queue import mark_completed

# After successful generation
mark_completed(topic_id="uuid-1234")

# Moves in_progress → completed
```

### Mark Failed

**Automatic** (done by `generate_posts.py`):
```python
from topic_queue import mark_failed

# After generation error
mark_failed(topic_id="uuid-1234", error="API timeout")

# Moves in_progress → failed
# Will auto-retry on next run
```

### Cleanup Stuck Topics

**Manual** (for stuck topics):
```bash
# Reset topics stuck for 24+ hours
python scripts/topic_queue.py cleanup 24

# Reset all stuck topics
python scripts/topic_queue.py cleanup 0
```

**Effect**: Moves `in_progress` → `pending` (for retry)

---

## Keyword Curation

### Google Trends Sources

**RSS Feeds**:
- **Korea (KR)**: Google Trends Korea
- **US (EN)**: Google Trends US
- **Japan (JP)**: Google Trends Japan

**Fetched keywords**: 15-20 per run

### Curation Process

**Step 1: Fetch trends**
```bash
python scripts/keyword_curator.py --count 15
```

**Step 2: Manual filtering** (required)

The script shows each keyword and asks:
```
Keyword: "AI trends 2026"
Source: US Trends
Category suggestion: tech
Language: en

Keep this keyword? (y/n):
```

**Step 3: Review and confirm**

After filtering, confirms additions:
```
Selected 12 out of 15 keywords.
Adding to queue...

✅ Added: AI trends 2026 (tech, en, priority 8)
✅ Added: Cloud computing (tech, en, priority 7)
...
```

### Filtering Criteria

**Keep if**:
- ✅ Relevant to blog topics (tech, business, lifestyle, etc.)
- ✅ Trending / high search volume
- ✅ Suitable for 800-2000 word article
- ✅ Not already in queue (auto-checked)

**Skip if**:
- ❌ Irrelevant (celebrity gossip, sports scores)
- ❌ Too specific (city-specific events)
- ❌ Too broad (single-word topics)
- ❌ Duplicate (already in queue)
- ❌ Not suitable for blog format

---

## Categories

**Valid categories** (8 total):

1. **tech** - Technology, AI, software
2. **business** - Entrepreneurship, startups, management
3. **lifestyle** - Productivity, health, travel
4. **society** - Social issues, culture, trends
5. **entertainment** - Media, gaming, content creation
6. **sports** - Fitness, athletic events
7. **finance** - Investing, economics, personal finance
8. **education** - Learning, courses, skills

**Auto-suggestion**: Keyword curator suggests category based on keyword

**Manual override**: You can change during curation

---

## Priority System

**Priority scale**: 1-10

| Priority | When to Use |
|----------|-------------|
| 10 | Urgent / breaking news |
| 8-9 | High interest / trending |
| 5-7 | Normal / evergreen |
| 3-4 | Low interest / backup |
| 1-2 | Filler content |

**Default**: 8 (trending keywords from Google Trends)

**Queue processing**: Highest priority first

---

## Duplicate Prevention

### Automatic Check

When adding topic, automatically checks:
- ✅ Keyword + language combination
- ✅ Status: Only checks `completed` topics
- ⚠️ Similar keywords NOT checked (manual review needed)

**Example**:
```python
# Will be rejected (duplicate):
add_topic("AI trends", "tech", "en")  # Already completed

# Will be accepted (different language):
add_topic("AI trends", "tech", "ko")  # Not completed in Korean
```

### Manual Check

```bash
# Search for keyword in queue
python scripts/topic_queue.py search "AI trends"

# Shows all topics matching "AI trends" (any status)
```

---

## Queue Health Monitoring

### Ideal Queue State

**Pending topics**: 15-30
- Too few (< 10): Risk of queue empty
- Too many (> 50): Backlog piling up

**In progress**: 0-3
- 0 = Good (no active generation)
- 1-3 = Normal (generation in progress)
- > 3 = Stuck (needs cleanup)

**Completed**: Growing
- Should increase by 9/day (3 runs × 3 posts)

**Failed**: 0
- Any failed topics = investigate and retry

### Queue Refill Schedule

**Automated** (GitHub Actions):
- **Schedule**: Fridays, 17:05 KST
- **Workflow**: `.github/workflows/daily-keywords.yml`
- **Count**: 15 keywords

**Manual** (when queue low):
```bash
# Check pending count
python scripts/topic_queue.py stats | grep Pending

# If < 10, curate more
python scripts/keyword_curator.py --count 15
```

---

## Automation

### GitHub Actions Workflow

**File**: `.github/workflows/daily-keywords.yml`

**Schedule**: `5 17 * * 5` (Fridays 17:05 KST, 08:05 UTC)

**Steps**:
1. Fetch Google Trends
2. Auto-filter (basic relevance)
3. Add to queue
4. Commit changes
5. Push to repo

**Note**: Manual curation still required (better quality)

### Content Generation Workflow

**File**: `.github/workflows/daily-content.yml`

**Schedule**: `0 -3,3,9 * * *` (6 AM, 12 PM, 6 PM KST)

**Steps**:
1. Reserve 3 topics from queue
2. Generate posts
3. Mark completed
4. Create PR

**Queue consumption**: 9 topics/day (3 runs × 3 posts)

---

## Common Issues

### Issue 1: Queue Empty

**Symptom**: `python scripts/topic_queue.py stats` shows 0 pending

**Impact**: Content generation will fail (no topics to process)

**Fix**:
```bash
# Immediate: Curate keywords
python scripts/keyword_curator.py --count 15

# Long-term: Check automation
# GitHub Actions → daily-keywords.yml → last run status
```

### Issue 2: Topics Stuck in Progress

**Symptom**: Topics stay `in_progress` for hours/days

**Causes**:
- Generation script crashed
- API timeout
- Server reboot during generation

**Fix**:
```bash
# View stuck topics
python scripts/topic_queue.py stats

# Reset stuck topics (24+ hours)
python scripts/topic_queue.py cleanup 24

# Re-run generation
python scripts/generate_posts.py --count 3
```

### Issue 3: Duplicate Keywords

**Symptom**: Same keyword appearing multiple times

**Causes**:
- Different languages (intentional)
- Typo / variation (e.g., "AI trend" vs "AI trends")
- Manual addition without checking

**Fix**:
```bash
# Search for duplicates
python scripts/topic_queue.py search "keyword"

# If true duplicate, manually remove from JSON
vim data/topics_queue.json
# Delete duplicate entry
```

### Issue 4: Low-Quality Keywords

**Symptom**: Irrelevant keywords in queue

**Causes**:
- Automated curation without manual filter
- Insufficient filtering criteria

**Fix**:
```bash
# Manual review of pending
python scripts/topic_queue.py list pending

# Remove low-quality topics
# Edit data/topics_queue.json manually
# Or wait for them to fail during generation
```

---

## Best Practices

### Keyword Selection

**Good keywords**:
- ✅ "AI trends 2026" (specific, timely, broad enough)
- ✅ "Remote work productivity tips" (actionable, useful)
- ✅ "Cloud computing comparison" (informative, searchable)

**Bad keywords**:
- ❌ "AI" (too broad, single word)
- ❌ "Seoul weather today" (too specific, temporal)
- ❌ "Celebrity name" (gossip, not blog-worthy)

### Queue Maintenance

**Weekly**:
- ✅ Check queue status (Friday before automation)
- ✅ Ensure 15+ pending topics
- ✅ Review and remove low-quality pending

**Daily**:
- ✅ Monitor automation runs (GitHub Actions)
- ✅ Check for stuck topics (> 24 hours in_progress)
- ✅ Verify completed count increasing

**Monthly**:
- ✅ Archive old completed topics (> 90 days)
- ✅ Review keyword performance (which topics generated best content)
- ✅ Adjust curation criteria if needed

### Category Distribution

**Target balance**:
- Tech: 30-40%
- Business: 20-30%
- Lifestyle: 15-20%
- Society: 10-15%
- Others: < 10% each

**Check distribution**:
```bash
# Count by category
jq '.topics[] | select(.status=="pending") | .category' data/topics_queue.json | sort | uniq -c
```

---

## Testing

### Test 1: Add Topic

```bash
# Add test topic
python3 << 'EOF'
import sys
from pathlib import Path
sys.path.insert(0, str(Path('scripts')))
from topic_queue import add_topic

add_topic(
    keyword="Test Keyword",
    category="tech",
    language="en",
    priority=5
)
print("✅ Topic added")
EOF

# Verify
python scripts/topic_queue.py stats
# Should show +1 pending
```

### Test 2: Reserve and Complete

```python
from topic_queue import reserve_topics, mark_completed

# Reserve
topics = reserve_topics(count=1)
print(f"Reserved: {topics[0]['keyword']}")

# Mark completed
mark_completed(topics[0]['id'])
print(f"✅ Marked completed")
```

### Test 3: Cleanup

```bash
# Manually set topic to in_progress with old timestamp
vim data/topics_queue.json
# Change status to "in_progress"
# Change updated_at to 2 days ago

# Run cleanup
python scripts/topic_queue.py cleanup 24

# Verify reset to pending
python scripts/topic_queue.py stats
```

---

## Advanced Usage

### Bulk Add Topics

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('scripts')))
from topic_queue import add_topic

keywords = [
    ("AI trends 2026", "tech", "en", 8),
    ("Remote work tips", "business", "en", 7),
    ("Travel hacks", "lifestyle", "en", 6),
]

for keyword, category, lang, priority in keywords:
    add_topic(keyword, category, lang, priority)
    print(f"✅ Added: {keyword}")
```

### Export Queue Data

```bash
# Export pending topics
jq '.topics[] | select(.status=="pending") | {keyword, category, language, priority}' data/topics_queue.json > pending_topics.json

# Export completed (last 30 days)
jq '.topics[] | select(.status=="completed" and (.updated_at | fromdateiso8601 > (now - 2592000)))' data/topics_queue.json > recent_completed.json
```

### Analyze Performance

```bash
# Count by status
jq '.topics | group_by(.status) | map({status: .[0].status, count: length})' data/topics_queue.json

# Average priority
jq '.topics[] | select(.status=="pending") | .priority' data/topics_queue.json | awk '{sum+=$1; n++} END {print sum/n}'

# Top categories
jq '.topics[] | select(.status=="pending") | .category' data/topics_queue.json | sort | uniq -c | sort -rn
```

---

## Related Skills

- **content-generation**: Uses queue for post generation
- **quality-validation**: Validates generated content
- **hugo-operations**: Previews generated posts

---

## References

- **Architecture**: `.claude/docs/architecture.md`
- **Development**: `.claude/docs/development.md`
- **Commands**: `.claude/docs/commands.md`

---

**Skill Version**: 1.0
**Last Updated**: 2026-01-23
**Maintained By**: Jake's Tech Insights project
