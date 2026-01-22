# CTO Agent - Examples

This file contains detailed examples for CTO agent work patterns.

## Example 1: CI/CD Optimization

```
User: "GitHub Actions execution time is too long"

CTO Analysis:
1. Current workflow analysis
   - daily-content.yml: Average 15 minutes
   - test.yml: Average 5 minutes
   - Bottlenecks: pytest execution, Hugo build

2. Optimization strategy
   - Add caching (pip, Hugo)
   - Parallel execution (test matrix)
   - Conditional execution (changed files only)

3. Expected improvements
   - daily-content.yml: 15min → 8min (47% improvement)
   - test.yml: 5min → 3min (40% improvement)

Action:
- Create feature/optimize-ci-cd branch
- Modify workflow files
- Run benchmarks and verify
```

**Technical Review Report**:
```markdown
## CI/CD Optimization: GitHub Actions

### Current Status
- Architecture: Sequential job execution
- Issues: Long execution time, no caching
- Performance: 15-20 minutes per workflow

### Proposed Solution

**Option 1: Add Caching**
- Pros: Easy to implement, 40-50% time reduction
- Cons: Cache invalidation complexity
- Estimated work: 2-3 hours

**Option 2: Parallel Matrix Execution**
- Pros: 60% time reduction for tests
- Cons: More complex setup, resource usage
- Estimated work: 4-5 hours

### Recommendation
Implement both options:
1. Add pip and Hugo caching (Phase 1)
2. Implement test matrix (Phase 2)

### Next Steps
1. Update .github/workflows/daily-content.yml
2. Add cache configuration
3. Benchmark before/after
```

---

## Example 2: Architecture Refactoring

```
User: "Scripts are too complex, please refactor"

CTO Analysis:
1. Current structure
   - 21 independent scripts
   - Code duplication exists
   - Lack of modularization

2. Proposed structure
   scripts/
   ├── core/           # Core logic
   │   ├── topic_queue.py
   │   ├── content_generator.py
   │   └── image_processor.py
   ├── utils/          # Utilities
   │   ├── security.py
   │   ├── validation.py
   │   └── logging.py
   └── workflows/      # Workflows
       ├── daily_content.py
       └── quality_check.py

3. Migration plan
   Phase 1: Extract utils module
   Phase 2: Refactor core modules
   Phase 3: Integrate workflows

Action:
- Write ADR document
- Get user approval
- Gradual migration
```

**Architecture Decision Record (ADR)**:
```markdown
# ADR: Script Architecture Refactoring

## Status
Proposed

## Context
Current script structure has grown organically to 21+ files with:
- Code duplication (especially error handling)
- No clear module boundaries
- Difficult to test and maintain

## Decision
Restructure scripts into three-layer architecture:
1. Core layer: Business logic
2. Utils layer: Shared utilities
3. Workflows layer: Orchestration

## Consequences
**Positive**:
- Better testability (isolated modules)
- Reduced duplication
- Clear dependencies
- Easier onboarding

**Negative**:
- Migration effort required
- Potential for breaking changes
- Learning curve for new structure

## Migration Strategy
1. Create new structure alongside old (no breaking changes)
2. Migrate one module at a time
3. Update imports gradually
4. Deprecate old structure after full migration
```

---

## Example 3: Performance Optimization

```
User: "Website build is slow"

CTO Analysis:
1. Measurement (Before)
   - Build time: 45 seconds
   - Image processing: 30 seconds (bottleneck)
   - Template rendering: 15 seconds

2. Optimization plan
   - Image optimization: WebP conversion, caching
   - Template optimization: Reduce partial includes
   - Content optimization: Paginate large lists

3. Expected results
   - Build time: 45s → 20s (56% improvement)
   - Image processing: 30s → 10s (67% improvement)

Action:
- Create feature/optimize-build branch
- Implement optimizations
- Benchmark and verify
```

**Performance Optimization Report**:
```markdown
## Performance Optimization: Build Time

### Measurement Results (Before)
- Build time: 45.3s
- Image processing: 30.1s
- Template rendering: 15.2s

### Optimization Actions
1. Image Processing Optimization
   - Changes: Add WebP caching, skip regeneration
   - Improvement: 67% faster

2. Template Optimization
   - Changes: Reduce partial includes, inline critical partials
   - Improvement: 20% faster

### Measurement Results (After)
- Build time: 19.8s (56.3% improvement)
- Image processing: 9.9s (67.1% improvement)
- Template rendering: 9.9s (34.9% improvement)

### Trade-offs
- Increased complexity in image caching logic
- Cache invalidation requires manual intervention
- Disk space increased by ~50MB for cached images

### Recommendations
- Monitor cache size monthly
- Add automated cache cleanup (>30 days)
- Document cache invalidation process
```

---

## Example 4: API Integration

```
User: "Add Unsplash API for image fetching"

CTO Work:
1. API Research
   - Unsplash API documentation review
   - Rate limits: 50 requests/hour (free tier)
   - Authentication: Access key required

2. Implementation design
   - Keyword translation (KO→EN)
   - Progressive keyword fallback
   - Error handling and retry logic
   - Metadata storage

3. Code structure
   scripts/fetch_images_for_posts.py:
   - fetch_image(keyword, lang)
   - translate_keyword(korean_text)
   - download_and_convert_webp(url)
   - save_metadata(post_id, image_info)

Action:
- Implement in feature/unsplash-integration
- Add tests with mocked API
- Document API usage and limits
```

**API Integration Guide**:
```markdown
## Unsplash API Integration

### Configuration
```bash
# .env file
UNSPLASH_ACCESS_KEY=your_key_here
```

### Usage
```python
from scripts.fetch_images_for_posts import fetch_image

# Fetch image with fallback
result = fetch_image(
    keyword="인공지능",
    lang="ko",
    fallback_keywords=["AI", "technology"]
)

# Returns:
{
    "url": "https://images.unsplash.com/...",
    "author": "John Doe",
    "download_location": "https://...",
    "webp_path": "static/images/posts/001.webp"
}
```

### Error Handling
- Rate limit exceeded → Wait and retry
- No results found → Use fallback keywords
- Download failed → Log error, skip image

### Rate Limit Management
- Free tier: 50 requests/hour
- Track usage in logs
- Implement exponential backoff
- Cache successful results

### Testing
```python
@patch('requests.get')
def test_fetch_image(mock_get):
    mock_get.return_value.json.return_value = {...}
    result = fetch_image("test")
    assert result is not None
```
```

---

## Example 5: Python Script Development

```
User: "Create topic queue management system"

CTO Implementation:

1. Requirements
   - JSON-based queue (topics_queue.json)
   - State management: pending → in_progress → completed
   - Priority-based reservation
   - Failure handling with retry

2. API Design
   ```python
   class TopicQueue:
       def __init__(self, queue_file: str)
       def reserve_topics(count: int, priority_min: int = 0) -> List[Dict]
       def mark_completed(topic_id: str) -> bool
       def mark_failed(topic_id: str, reason: str) -> bool
       def get_stats() -> Dict
   ```

3. Implementation
   - Type hints for all functions
   - Comprehensive docstrings
   - Error handling with logging
   - Atomic file operations (prevent corruption)

4. Testing
   - Unit tests with fixtures
   - Edge cases (empty queue, invalid IDs)
   - Integration tests with actual JSON
```

**Code Implementation**:
```python
# scripts/topic_queue.py
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class TopicQueue:
    """
    Manages topic queue with state machine.

    States: pending → in_progress → completed
                    ↓ (on failure)
                  pending (with retry count)
    """

    def __init__(self, queue_file: str):
        """
        Initialize topic queue.

        Args:
            queue_file: Path to queue JSON file

        Raises:
            FileNotFoundError: If queue file doesn't exist
            ValueError: If queue file is invalid JSON
        """
        self.queue_file = Path(queue_file)
        if not self.queue_file.exists():
            raise FileNotFoundError(f"Queue file not found: {queue_file}")

        self._load_queue()

    def reserve_topics(
        self,
        count: int,
        priority_min: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Reserve topics by priority (high to low).

        Args:
            count: Number of topics to reserve
            priority_min: Minimum priority threshold (0-10)

        Returns:
            List of reserved topics (status changed to in_progress)

        Raises:
            ValueError: If count is negative

        Example:
            >>> queue = TopicQueue("queue.json")
            >>> topics = queue.reserve_topics(count=3, priority_min=5)
            >>> len(topics) <= 3
            True
        """
        if count < 0:
            raise ValueError("Count must be non-negative")

        # Filter pending topics by priority
        pending = [
            t for t in self.data["topics"]
            if t["status"] == "pending" and t["priority"] >= priority_min
        ]

        # Sort by priority (descending)
        pending.sort(key=lambda x: x["priority"], reverse=True)

        # Reserve top N
        reserved = []
        for topic in pending[:count]:
            topic["status"] = "in_progress"
            topic["reserved_at"] = datetime.utcnow().isoformat()
            reserved.append(topic)

        self._save_queue()
        logger.info(f"Reserved {len(reserved)} topics")
        return reserved

    def mark_completed(self, topic_id: str) -> bool:
        """Mark topic as completed."""
        topic = self._find_topic(topic_id)
        if not topic:
            logger.warning(f"Topic not found: {topic_id}")
            return False

        topic["status"] = "completed"
        topic["completed_at"] = datetime.utcnow().isoformat()
        self._save_queue()
        logger.info(f"Marked completed: {topic_id}")
        return True

    def mark_failed(self, topic_id: str, reason: str) -> bool:
        """Mark topic as failed, reset to pending with retry."""
        topic = self._find_topic(topic_id)
        if not topic:
            logger.warning(f"Topic not found: {topic_id}")
            return False

        topic["status"] = "pending"
        topic["retry_count"] = topic.get("retry_count", 0) + 1
        topic["last_failure"] = {
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }
        self._save_queue()
        logger.info(f"Marked failed: {topic_id} (retry: {topic['retry_count']})")
        return True

    def _load_queue(self):
        """Load queue from file."""
        with open(self.queue_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def _save_queue(self):
        """Save queue to file atomically."""
        # Write to temp file first
        temp_file = self.queue_file.with_suffix('.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

        # Atomic rename
        temp_file.replace(self.queue_file)

    def _find_topic(self, topic_id: str) -> Optional[Dict]:
        """Find topic by ID."""
        for topic in self.data["topics"]:
            if topic["id"] == topic_id:
                return topic
        return None
```

**Tests**:
```python
# tests/test_topic_queue.py
import pytest
from scripts.topic_queue import TopicQueue

@pytest.fixture
def sample_queue(tmp_path):
    """Create sample queue file."""
    queue_file = tmp_path / "queue.json"
    data = {
        "topics": [
            {"id": "1", "priority": 3, "status": "pending"},
            {"id": "2", "priority": 9, "status": "pending"},
            {"id": "3", "priority": 5, "status": "pending"}
        ]
    }
    with open(queue_file, 'w') as f:
        json.dump(data, f)
    return str(queue_file)

def test_reserve_topics_by_priority(sample_queue):
    """Test that topics are reserved by priority (high to low)."""
    queue = TopicQueue(sample_queue)

    reserved = queue.reserve_topics(count=2)

    assert len(reserved) == 2
    assert reserved[0]["priority"] == 9  # Highest
    assert reserved[1]["priority"] == 5  # Second
    assert reserved[0]["status"] == "in_progress"

def test_mark_completed(sample_queue):
    """Test marking topic as completed."""
    queue = TopicQueue(sample_queue)

    result = queue.mark_completed("1")

    assert result is True
    topic = queue._find_topic("1")
    assert topic["status"] == "completed"
    assert "completed_at" in topic
```

---

**Last Updated**: 2026-01-20
**Related**: [CTO.md](CTO.md)
