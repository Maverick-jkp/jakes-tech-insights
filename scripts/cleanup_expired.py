#!/usr/bin/env python3
"""
Cleanup expired trending keywords from the topic queue.

This script removes trend keywords that have exceeded their expiry period.
- Affects both "pending" and "completed" keywords with keyword_type="trend"
- Does not touch "in_progress" keywords (actively being processed)
- Does not touch evergreen keywords (they have no expiry)
- Removes completed keywords without timestamps (orphaned old data)
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
        status = topic.get("status")
        keyword_type = topic.get("keyword_type")

        # Always keep in_progress keywords (actively being processed)
        if status == "in_progress":
            remaining.append(topic)
            continue

        # Always keep evergreen keywords (no expiry)
        if keyword_type != "trend":
            remaining.append(topic)
            continue

        # For trend keywords (both pending and completed), check expiry
        # Use added_at (when keyword was added to queue) or created_at as fallback
        timestamp_str = topic.get("added_at") or topic.get("created_at")

        # Remove old keywords without timestamps (orphaned data from before added_at field)
        if not timestamp_str:
            if status == "completed":
                # Completed keywords without timestamp are old - remove them
                removed.append(topic)
            else:
                # Pending keywords without timestamp - keep to be safe
                remaining.append(topic)
            continue

        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            # Use date only for comparison (ignore time)
            timestamp_date = timestamp.date()
            cutoff_date = cutoff_time.date()

            if timestamp_date < cutoff_date:
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
