#!/usr/bin/env python3
"""
Cleanup expired trending keywords from the topic queue.

This script removes pending trend keywords that have exceeded their expiry period.
- Only affects keywords with status="pending" and keyword_type="trend"
- Does not touch in_progress or completed keywords
- Does not touch evergreen keywords (they have no expiry)
"""

import json
from datetime import datetime, timedelta
from pathlib import Path


def cleanup_expired_keywords(expiry_days: int = 3) -> dict:
    """
    Remove expired trending keywords from the queue.

    Args:
        expiry_days: Number of days before a trend keyword expires (default: 3)

    Returns:
        dict: Statistics about cleanup (removed count, remaining count)
    """
    queue_file = Path(__file__).parent.parent / "data" / "topics_queue.json"

    if not queue_file.exists():
        print(f"⚠️  Queue file not found: {queue_file}")
        return {"removed": 0, "remaining": 0}

    # Load queue
    with open(queue_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    topics = data.get("topics", [])
    original_count = len(topics)

    # Current time
    now = datetime.now()
    cutoff_time = now - timedelta(days=expiry_days)

    # Filter out expired trending keywords
    removed = []
    remaining = []

    for topic in topics:
        # Only check pending trend keywords
        if topic.get("status") != "pending":
            remaining.append(topic)
            continue

        if topic.get("keyword_type") != "trend":
            remaining.append(topic)
            continue

        # Check expiry
        created_at_str = topic.get("created_at")
        if not created_at_str:
            remaining.append(topic)
            continue

        try:
            created_at = datetime.fromisoformat(created_at_str)

            if created_at < cutoff_time:
                # Expired - remove it
                removed.append(topic)
            else:
                # Still fresh - keep it
                remaining.append(topic)
        except (ValueError, TypeError):
            # Invalid date format - keep it to be safe
            remaining.append(topic)
            continue

    # Update queue with remaining topics
    data["topics"] = remaining

    with open(queue_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\n{'='*60}")
    print(f"  🗑️  Cleanup Complete (Expiry: {expiry_days} days)")
    print(f"{'='*60}\n")
    print(f"  Original count: {original_count}")
    print(f"  Removed (expired): {len(removed)}")
    print(f"  Remaining: {len(remaining)}")

    if removed:
        print(f"\n  🗑️  Removed keywords:")
        for topic in removed:
            keyword = topic.get("keyword", "unknown")
            created = topic.get("created_at", "unknown")[:10]
            print(f"    - {keyword} (created: {created})")

    print()

    return {
        "removed": len(removed),
        "remaining": len(remaining),
        "removed_keywords": [t.get("keyword") for t in removed]
    }


if __name__ == "__main__":
    import sys

    # Allow custom expiry days via command line
    expiry_days = 3
    if len(sys.argv) > 1:
        try:
            expiry_days = int(sys.argv[1])
        except ValueError:
            print(f"⚠️  Invalid expiry days: {sys.argv[1]}, using default: 3")

    cleanup_expired_keywords(expiry_days)
