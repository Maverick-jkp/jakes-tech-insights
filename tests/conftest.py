"""
Shared pytest fixtures for all tests.
"""
import json
import pytest
from pathlib import Path
from typing import Dict, List

@pytest.fixture
def sample_queue() -> Dict:
    """Load sample topic queue for testing."""
    fixture_path = Path(__file__).parent / "fixtures" / "sample_queue.json"

    if fixture_path.exists():
        with open(fixture_path, 'r') as f:
            return json.load(f)

    # Default sample queue
    return {
        "topics": [
            {
                "id": "001-en-tech-test-keyword",
                "keyword": "Test Keyword",
                "category": "tech",
                "lang": "en",
                "language": "en",
                "priority": 8,
                "status": "pending",
                "expiry_days": 3,
                "trend_type": "evergreen",
                "retry_count": 0,
                "created_at": "2026-01-20T12:00:00+09:00",
                "reserved_at": None,
                "completed_at": None
            }
        ]
    }

@pytest.fixture
def temp_queue_file(tmp_path, sample_queue):
    """Create a temporary queue file for testing."""
    queue_file = tmp_path / "test_queue.json"

    with open(queue_file, 'w') as f:
        json.dump(sample_queue, f)

    return str(queue_file)

@pytest.fixture
def sample_post_content() -> str:
    """Sample blog post content for testing."""
    return """---
title: "Test Post"
date: 2026-01-20T12:00:00+09:00
description: "This is a test post for unit testing."
categories: ["tech"]
tags: ["testing", "python"]
image: cover.jpg
---

This is a test post with some content.

## Section 1

Some content here.

## Section 2

More content here.

## Conclusion

Final thoughts.
"""

@pytest.fixture
def mock_anthropic_response():
    """Mock Anthropic API response."""
    return {
        "content": [
            {
                "text": "Generated content here..."
            }
        ],
        "usage": {
            "input_tokens": 1000,
            "output_tokens": 2000
        }
    }
