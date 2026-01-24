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

## Dependencies

**Required Python packages:**
- `feedparser==6.0.10` - Google Trends RSS feed parsing
- `pyyaml==6.0` - Topic queue JSON/YAML handling
- `requests==2.31.0` - HTTP requests (if needed)

**Installation:**
```bash
pip install -r requirements.txt
```

**Verification:**
```bash
python -c "import feedparser, yaml; print('✓ All dependencies installed')"
```

**Note**: This skill does NOT require Claude API (no API costs).

---

## Quick Start

```bash
# View queue status
python scripts/topic_queue.py stats

# Curate new keywords (manual filtering required)
python scripts/keyword_curator.py --count 15

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

1. **pending** - Ready to be processed
2. **in_progress** - Currently generating
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
      "created_at": "2026-01-23T18:00:00+09:00"
    }
  ]
}
```

---

## Queue Operations

### View Status

```bash
python scripts/topic_queue.py stats

# Output:
# Total topics: 74
# Pending: 14
# In progress: 0
# Completed: 60
```

### Add Topic

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

### Cleanup Stuck Topics

```bash
# Reset topics stuck for 24+ hours
python scripts/topic_queue.py cleanup 24
```

---

## Keyword Curation

### Google Trends Sources

**RSS Feeds**:
- **Korea (KR)**: Google Trends Korea
- **US (EN)**: Google Trends US
- **Japan (JP)**: Google Trends Japan

### Curation Process

```bash
# Step 1: Fetch trends
python scripts/keyword_curator.py --count 15

# Step 2: Manual filtering (script prompts)
# Keep: y
# Skip: n

# Step 3: Review additions
# Script confirms all added keywords
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

---

## Categories

**Valid categories** (8 total):

1. **tech** - Technology, AI, software
2. **business** - Entrepreneurship, startups
3. **lifestyle** - Productivity, health, travel
4. **society** - Social issues, culture
5. **entertainment** - Media, gaming
6. **sports** - Fitness, athletic events
7. **finance** - Investing, economics
8. **education** - Learning, courses

---

## Priority System

| Priority | When to Use |
|----------|-------------|
| 10 | Urgent / breaking news |
| 8-9 | High interest / trending |
| 5-7 | Normal / evergreen |
| 3-4 | Low interest / backup |

**Default**: 8 (trending keywords from Google Trends)

---

## Queue Health Monitoring

### Ideal Queue State

**Pending topics**: 15-30
- Too few (< 10): Risk of queue empty
- Too many (> 50): Backlog piling up

**In progress**: 0-3
- 0 = Good (no active generation)
- > 3 = Stuck (needs cleanup)

**Completed**: Growing by 9/day (3 runs × 3 posts)

---

## Common Issues

### Issue 1: Queue Empty

**Symptom**: 0 pending topics

**Fix**:
```bash
# Immediate: Curate keywords
python scripts/keyword_curator.py --count 15
```

### Issue 2: Topics Stuck

**Symptom**: Topics in `in_progress` for hours/days

**Fix**:
```bash
# View stuck topics
python scripts/topic_queue.py stats

# Reset (24+ hours)
python scripts/topic_queue.py cleanup 24
```

---

## Automation

**GitHub Actions**: `.github/workflows/daily-keywords.yml`
**Schedule**: Fridays, 17:05 KST
**Count**: 15 keywords per run

**Content Generation**: `.github/workflows/daily-content.yml`
**Schedule**: 6 AM, 12 PM, 6 PM KST
**Consumption**: 9 topics/day (3 runs × 3 posts)

---

## Advanced Topics

For detailed information, see:
- **Queue Management**: `resources/queue-management.md` - State machine, operations
- **Curation Guide**: `resources/curation-guide.md` - Keyword selection, filtering
- **Best Practices**: `resources/best-practices.md` - Maintenance, distribution

---

## Testing

```bash
# Test add topic
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

**Skill Version**: 1.2
**Last Updated**: 2026-01-24
**Maintained By**: Jake's Tech Insights project
