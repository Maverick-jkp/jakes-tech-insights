# QA Agent - Examples

This file contains detailed examples for QA agent work patterns.

## Example 1: New Feature Testing

```
User: "Added filter_by_category() function to topic_queue.py"

QA Work:
1. Test planning
   - Happy path: Filter by category
   - Edge case: Non-existent category
   - Edge case: Empty category

2. Test implementation
3. Coverage verification
   - filter_by_category: 100%
   - Overall topic_queue.py: 65% → 68%

Action:
- Add tests to tests/test_topic_queue.py
- Run pytest and verify pass
- Generate coverage report
```

**Test Implementation**:
```python
# tests/test_topic_queue.py
import pytest
from scripts.topic_queue import TopicQueue

class TestFilterByCategory:
    """Tests for filter_by_category function."""

    def test_filter_existing_category(self, temp_queue_file):
        """Test filtering by existing category."""
        # Arrange
        queue = TopicQueue(temp_queue_file)

        # Act
        results = queue.filter_by_category("tech")

        # Assert
        assert len(results) > 0
        assert all(t["category"] == "tech" for t in results)

    def test_filter_nonexistent_category(self, temp_queue_file):
        """Test filtering by non-existent category."""
        # Arrange
        queue = TopicQueue(temp_queue_file)

        # Act
        results = queue.filter_by_category("nonexistent")

        # Assert
        assert len(results) == 0

    def test_filter_empty_category(self, temp_queue_file):
        """Test filtering with empty category name."""
        # Arrange
        queue = TopicQueue(temp_queue_file)

        # Act & Assert
        with pytest.raises(ValueError, match="Category cannot be empty"):
            queue.filter_by_category("")

    def test_filter_case_insensitive(self, temp_queue_file):
        """Test that filtering is case-insensitive."""
        # Arrange
        queue = TopicQueue(temp_queue_file)

        # Act
        results_lower = queue.filter_by_category("tech")
        results_upper = queue.filter_by_category("TECH")

        # Assert
        assert len(results_lower) == len(results_upper)
```

**Test Report**:
```markdown
## Test Implementation Complete: filter_by_category

### Test Scope
**Test file**: tests/test_topic_queue.py: 4 new tests

**Test class**: TestFilterByCategory
- test_filter_existing_category
- test_filter_nonexistent_category
- test_filter_empty_category
- test_filter_case_insensitive

### Test Results
**Execution**:
- Total tests: 4
- Passed: 4 (100%)
- Failed: 0
- Execution time: 0.23s

**Coverage**:
- Overall: 68% (+3%)
- filter_by_category: 100%
- Untested lines: None

### Test Cases
1. **Happy path**: Filter existing category returns correct results
2. **Edge cases**:
   - Non-existent category returns empty list
   - Empty category name raises ValueError
   - Case-insensitive filtering
```

---

## Example 2: Bug Reproduction Testing

```
User: "reserve_topics() ignores priority"

QA Work:
1. Write bug reproduction test
2. Run test → Fails (confirms bug)
3. After developer fixes, re-run → Passes
4. Add as regression test

Action:
- Add reproduction test
- Report to developer
- Verify fix with regression test
```

**Bug Reproduction Test**:
```python
# tests/test_topic_queue.py
def test_reserve_topics_respects_priority(temp_queue_file):
    """
    Test that topics are reserved by priority (high to low).

    This is a regression test for bug where priority was ignored.
    """
    # Arrange: Create topics with different priorities
    queue_data = {
        "topics": [
            {"id": "1", "priority": 3, "status": "pending"},
            {"id": "2", "priority": 9, "status": "pending"},
            {"id": "3", "priority": 5, "status": "pending"}
        ]
    }

    queue_file = tmp_path / "queue.json"
    with open(queue_file, 'w') as f:
        json.dump(queue_data, f)

    queue = TopicQueue(str(queue_file))

    # Act
    reserved = queue.reserve_topics(count=2)

    # Assert
    assert len(reserved) == 2
    assert reserved[0]["id"] == "2"  # Priority 9 (highest)
    assert reserved[1]["id"] == "3"  # Priority 5 (second)
    assert reserved[0]["priority"] == 9
    assert reserved[1]["priority"] == 5

    # Verify status changed
    assert all(t["status"] == "in_progress" for t in reserved)
```

**Bug Report**:
```markdown
## Bug Reproduction: reserve_topics() Priority Issue

### Bug Description
reserve_topics() does not respect priority order when reserving topics.

### Steps to Reproduce
1. Create queue with topics of different priorities (3, 9, 5)
2. Call reserve_topics(count=2)
3. Expected: Returns topics with priority 9, 5 (high to low)
4. Actual: Returns topics in random order

### Reproduction Test
Created test: `test_reserve_topics_respects_priority`

### Test Result
**Before fix**: FAILED (confirmed bug)
**After fix**: PASSED (bug resolved)

### Recommendation
Keep this test as regression test to prevent future recurrence.
```

---

## Example 3: Coverage Improvement

```
User: "Increase test coverage to 70%"

QA Work:
1. Current coverage analysis
   - Overall: 58%
   - Untested modules identified

2. Coverage improvement plan
   - Module 1: topic_queue.py (60% → 75%)
   - Module 2: content_generator.py (45% → 70%)
   - Module 3: image_processor.py (50% → 65%)

3. Test writing
   - Add 15 new tests
   - Focus on untested functions

4. Results
   - Overall: 58% → 72% (goal achieved)

Action:
- Write tests for untested areas
- Generate coverage report
- Document improvements
```

**Coverage Analysis**:
```bash
# Before
$ pytest --cov=scripts --cov-report=term-missing

Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
scripts/topic_queue.py           120     48    60%   45-52, 78-85, 110-125
scripts/content_generator.py      95     52    45%   23-35, 67-89, 95-105
scripts/image_processor.py        80     40    50%   12-25, 56-78
-----------------------------------------------------------
TOTAL                            295    140    58%
```

**Improvement Plan**:
```python
# tests/test_topic_queue.py - Added tests
class TestTopicQueueEdgeCases:
    """Coverage improvement: Edge cases for topic queue."""

    def test_reserve_topics_with_zero_count(self, temp_queue_file):
        """Test reserve with count=0."""
        queue = TopicQueue(temp_queue_file)
        reserved = queue.reserve_topics(count=0)
        assert len(reserved) == 0

    def test_reserve_topics_exceeds_available(self, temp_queue_file):
        """Test reserve when count exceeds available topics."""
        queue = TopicQueue(temp_queue_file)
        # Queue has 5 topics
        reserved = queue.reserve_topics(count=100)
        assert len(reserved) <= 5

    def test_mark_completed_invalid_id(self, temp_queue_file):
        """Test mark_completed with invalid topic ID."""
        queue = TopicQueue(temp_queue_file)
        result = queue.mark_completed("invalid-id")
        assert result is False

    def test_mark_failed_increments_retry(self, temp_queue_file):
        """Test that mark_failed increments retry count."""
        queue = TopicQueue(temp_queue_file)

        # First failure
        queue.mark_failed("1", "API timeout")
        topic = queue._find_topic("1")
        assert topic["retry_count"] == 1

        # Second failure
        queue.mark_failed("1", "Network error")
        topic = queue._find_topic("1")
        assert topic["retry_count"] == 2

    def test_concurrent_access_safety(self, temp_queue_file):
        """Test that file writes are atomic."""
        queue = TopicQueue(temp_queue_file)

        # Simulate concurrent writes
        import threading

        def reserve_worker():
            queue.reserve_topics(count=1)

        threads = [threading.Thread(target=reserve_worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Verify queue file is not corrupted
        data = queue._load_queue()
        assert "topics" in data
```

**Coverage Report After**:
```bash
$ pytest --cov=scripts --cov-report=term-missing

Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
scripts/topic_queue.py           120     30    75%   110-119, 125
scripts/content_generator.py      95     28    70%   95-105
scripts/image_processor.py        80     28    65%   70-78
-----------------------------------------------------------
TOTAL                            295     86    72%
```

**Coverage Improvement Report**:
```markdown
## Coverage Improvement: 70% Goal Achieved

### Before
- Overall: 58%
- Untested modules: topic_queue (60%), content_generator (45%)
- Target: 70%

### Improvement Actions
1. topic_queue.py: 60% → 75% (+15%)
   - Added tests: 8
   - Covered functions: mark_completed, mark_failed, edge cases

2. content_generator.py: 45% → 70% (+25%)
   - Added tests: 5
   - Covered functions: validate_content, parse_response

3. image_processor.py: 50% → 65% (+15%)
   - Added tests: 4
   - Covered functions: download_image, convert_webp

### After
- Overall: 72% (goal 70% achieved ✓)
- All core modules >65%
- CI/CD quality gate passes

### Remaining Work
- image_processor.py: Currently 65%, target 70%
- One-time scripts excluded (fix_*.py)
```

---

## Example 4: Integration Testing

```
User: "Test full content generation workflow"

QA Work:
1. Integration test scope
   - Topic queue → Content generator → Image fetcher → Hugo post
   - End-to-end validation

2. Test strategy
   - Mock external APIs (Anthropic, Unsplash)
   - Use temporary directories
   - Verify file creation and format

3. Implementation
   - Create integration test fixture
   - Test entire pipeline
   - Verify output quality

Action:
- Create tests/integration/test_content_workflow.py
- Mock all external services
- Verify end-to-end functionality
```

**Integration Test**:
```python
# tests/integration/test_content_workflow.py
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

@pytest.fixture
def temp_project(tmp_path):
    """Create temporary project structure."""
    project = tmp_path / "project"
    project.mkdir()

    # Create directories
    (project / "data").mkdir()
    (project / "content" / "ko" / "posts").mkdir(parents=True)
    (project / "static" / "images").mkdir(parents=True)

    # Create queue file
    queue_file = project / "data" / "topics_queue.json"
    queue_data = {
        "topics": [
            {
                "id": "001-ko-tech-ai",
                "keyword": "인공지능",
                "category": "tech",
                "lang": "ko",
                "status": "pending",
                "priority": 5
            }
        ]
    }
    with open(queue_file, 'w', encoding='utf-8') as f:
        json.dump(queue_data, f, indent=2)

    return project

@patch('anthropic.Anthropic')
@patch('requests.get')
def test_full_content_generation_workflow(
    mock_requests,
    mock_anthropic,
    temp_project
):
    """
    Integration test: Full content generation workflow.

    Tests the complete pipeline:
    1. Reserve topic from queue
    2. Generate content with Claude API
    3. Fetch image from Unsplash
    4. Create Hugo post file
    """
    # Mock Anthropic API response
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="""
        ---
        title: "인공지능의 미래"
        date: 2026-01-20
        categories: ["tech"]
        tags: ["AI", "machine learning"]
        ---

        # 인공지능의 미래

        인공지능은 우리 삶을 변화시키고 있습니다...
        """)]
    )
    mock_anthropic.return_value = mock_client

    # Mock Unsplash API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [{
            "urls": {"raw": "https://example.com/image.jpg"},
            "user": {"name": "Test User"},
            "links": {"download_location": "https://example.com/download"}
        }]
    }
    mock_requests.return_value = mock_response

    # Import and run workflow
    from scripts.workflows import daily_content_workflow

    result = daily_content_workflow.run(
        project_dir=str(temp_project),
        count=1
    )

    # Verify results
    assert result["success"] is True
    assert result["posts_created"] == 1

    # Verify post file created
    post_files = list((temp_project / "content" / "ko" / "posts").glob("*.md"))
    assert len(post_files) == 1

    # Verify post content
    post_content = post_files[0].read_text(encoding='utf-8')
    assert "title:" in post_content
    assert "인공지능" in post_content

    # Verify image downloaded
    image_files = list((temp_project / "static" / "images").glob("*.webp"))
    assert len(image_files) == 1

    # Verify queue updated
    queue_file = temp_project / "data" / "topics_queue.json"
    with open(queue_file) as f:
        queue_data = json.load(f)

    topic = queue_data["topics"][0]
    assert topic["status"] == "completed"
    assert "completed_at" in topic
```

**Integration Test Report**:
```markdown
## Integration Test: Content Generation Workflow

### Test Scope
Full end-to-end workflow from topic queue to Hugo post

### Test Scenario
1. Reserve topic from queue (topic_queue.py)
2. Generate content via Claude API (content_generator.py)
3. Fetch image from Unsplash (image_processor.py)
4. Create Hugo markdown post (post_writer.py)
5. Update queue status (topic_queue.py)

### Test Results
**Execution**: PASSED
**Duration**: 1.2s

### Validation Points
- ✓ Topic reserved correctly
- ✓ API calls mocked (no actual API usage)
- ✓ Post file created in correct location
- ✓ Post content valid (frontmatter + body)
- ✓ Image downloaded and converted to WebP
- ✓ Queue status updated to "completed"

### Mock Verification
- ✓ Anthropic API called once with correct params
- ✓ Unsplash API called once with correct params
- ✓ No actual network calls made (100% mocked)

### Code Coverage
- Workflow functions: 95%
- Integration points: 100%
```

---

## Example 5: Fixture Management

```
User: "Tests are slow due to repeated setup"

QA Work:
1. Analyze test setup patterns
   - Repeated file creation
   - Duplicate mock configurations

2. Refactor to fixtures
   - Session-scoped fixtures for slow setup
   - Function-scoped for test isolation
   - Parametrized fixtures for variations

3. Results
   - Test execution time: 8.5s → 3.2s (62% faster)
   - Code duplication reduced

Action:
- Refactor conftest.py
- Create reusable fixtures
- Document fixture usage
```

**Optimized Fixtures**:
```python
# tests/conftest.py
import pytest
import json
from pathlib import Path

@pytest.fixture(scope="session")
def sample_queue_data():
    """
    Sample queue data (session-scoped, created once).

    Use this for read-only test data that doesn't change.
    """
    return {
        "topics": [
            {
                "id": "001-ko-tech-ai",
                "keyword": "인공지능",
                "category": "tech",
                "lang": "ko",
                "status": "pending",
                "priority": 5
            },
            {
                "id": "002-en-business-startup",
                "keyword": "Startup",
                "category": "business",
                "lang": "en",
                "status": "pending",
                "priority": 7
            }
        ]
    }

@pytest.fixture
def temp_queue_file(tmp_path, sample_queue_data):
    """
    Create temporary queue file (function-scoped).

    Each test gets a fresh copy for isolation.
    """
    queue_file = tmp_path / "queue.json"
    with open(queue_file, 'w', encoding='utf-8') as f:
        json.dump(sample_queue_data, f, indent=2)
    return str(queue_file)

@pytest.fixture
def mock_anthropic():
    """Mock Anthropic API client."""
    with patch('anthropic.Anthropic') as mock:
        mock_client = MagicMock()
        mock_client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="Generated content")]
        )
        mock.return_value = mock_client
        yield mock

@pytest.fixture(params=["ko", "en", "ja"])
def language(request):
    """Parametrized fixture for testing multiple languages."""
    return request.param

# Usage example:
def test_multilingual_content(language, temp_queue_file):
    """Test content generation for all languages."""
    result = generate_content(lang=language)
    assert result is not None
```

**Performance Comparison**:
```markdown
## Test Performance Improvement

### Before Refactoring
- Test execution time: 8.5s
- Repeated setup in each test
- Mock configuration duplicated 15 times

### After Refactoring
- Test execution time: 3.2s (62% faster)
- Setup centralized in fixtures
- Mock configuration reused via fixtures

### Fixture Strategy
- **Session-scoped**: Slow setup, shared data (sample_queue_data)
- **Function-scoped**: Test isolation (temp_queue_file)
- **Parametrized**: Test variations (language fixture)

### Benefits
- ✓ Faster test execution
- ✓ Less code duplication
- ✓ Better test isolation
- ✓ Easier to maintain
```

---

**Last Updated**: 2026-01-20
**Related**: [QA.md](QA.md)
