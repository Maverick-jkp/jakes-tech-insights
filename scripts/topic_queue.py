#!/usr/bin/env python3
"""
Topic Queue Manager with State Machine

States:
- pending: Ready to be processed
- in_progress: Currently being processed
- completed: Successfully processed
- failed: Failed processing (will be retried)

Usage:
    from topic_queue import reserve_topics, mark_completed, mark_failed

    topics = reserve_topics(count=3)
    for topic in topics:
        try:
            # Process topic...
            mark_completed(topic['id'])
        except Exception as e:
            mark_failed(topic['id'], str(e))
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict, Optional

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))
from utils.validation import (
    validate_keyword,
    validate_category,
    validate_language,
    validate_priority,
    validate_status,
    validate_topic_data
)


class TopicQueue:
    def __init__(self, queue_file: str = "data/topics_queue.json"):
        self.queue_file = Path(queue_file)
        self._ensure_queue_file()

    def _ensure_queue_file(self):
        """Create queue file if it doesn't exist"""
        if not self.queue_file.exists():
            self.queue_file.parent.mkdir(parents=True, exist_ok=True)
            self._save_queue({"topics": []})

    def _load_queue(self) -> Dict:
        """Load queue from file"""
        with open(self.queue_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_queue(self, data: Dict):
        """Save queue to file"""
        with open(self.queue_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def reserve_topics(self, count: int = 3, priority_min: int = 1) -> List[Dict]:
        """
        Reserve topics by moving them from pending to in_progress

        Args:
            count: Number of topics to reserve
            priority_min: Minimum priority level (1-10)

        Returns:
            List of reserved topics
        """
        data = self._load_queue()

        # Find pending topics sorted by priority (high to low) and created_at
        pending = [
            t for t in data['topics']
            if t['status'] == 'pending' and t.get('priority', 5) >= priority_min
        ]
        pending.sort(key=lambda x: (-x.get('priority', 5), x.get('created_at', '')))

        # Reserve top N topics
        reserved = []
        now = datetime.now(timezone.utc).isoformat()

        for topic in pending[:count]:
            # Validate topic data before reserving
            errors = validate_topic_data(topic)
            if errors:
                # Skip invalid topics
                print(f"⚠️  Skipping invalid topic {topic.get('id', 'unknown')}: {errors}")
                continue

            topic['status'] = 'in_progress'
            topic['reserved_at'] = now
            topic['retry_count'] = topic.get('retry_count', 0)
            reserved.append(topic)

        self._save_queue(data)
        return reserved

    def mark_completed(self, topic_id: str):
        """Mark a topic as completed"""
        data = self._load_queue()

        for topic in data['topics']:
            if topic['id'] == topic_id:
                topic['status'] = 'completed'
                topic['completed_at'] = datetime.now(timezone.utc).isoformat()
                break

        self._save_queue(data)

    def mark_failed(self, topic_id: str, error_message: str = ""):
        """
        Mark a topic as failed and move back to pending for retry

        Args:
            topic_id: Topic ID
            error_message: Error description
        """
        data = self._load_queue()

        for topic in data['topics']:
            if topic['id'] == topic_id:
                topic['status'] = 'pending'  # Rollback to pending
                topic['retry_count'] = topic.get('retry_count', 0) + 1
                topic['last_error'] = error_message
                topic['last_failed_at'] = datetime.now(timezone.utc).isoformat()

                # Remove reservation timestamp
                topic.pop('reserved_at', None)
                break

        self._save_queue(data)

    def cleanup_stuck_topics(self, hours: int = 24):
        """
        Reset topics stuck in in_progress state for too long

        Args:
            hours: Number of hours before considering a topic stuck
        """
        data = self._load_queue()
        now = datetime.now(timezone.utc)
        threshold = now - timedelta(hours=hours)

        for topic in data['topics']:
            if topic['status'] == 'in_progress':
                reserved_at_str = topic.get('reserved_at', '')
                if reserved_at_str:
                    reserved_at = datetime.fromisoformat(reserved_at_str)
                    if reserved_at < threshold:
                        topic['status'] = 'pending'
                        topic['retry_count'] = topic.get('retry_count', 0) + 1
                        topic['last_error'] = f"Stuck in progress for {hours}+ hours"
                        topic.pop('reserved_at', None)

        self._save_queue(data)

    def add_topic(self, keyword: str, category: str, lang: str,
                  priority: int = 5, metadata: Optional[Dict] = None):
        """
        Add a new topic to the queue

        Args:
            keyword: Topic keyword/title
            category: Category (tech/business/lifestyle/society/entertainment/sports/finance/education)
            lang: Language code (en/ko/ja)
            priority: Priority 1-10 (higher = more important)
            metadata: Additional metadata dict

        Raises:
            ValueError: If validation fails
        """
        # Validate inputs
        error = validate_keyword(keyword)
        if error:
            raise ValueError(f"Invalid keyword: {error}")

        error = validate_category(category)
        if error:
            raise ValueError(error)

        error = validate_language(lang)
        if error:
            raise ValueError(error)

        error = validate_priority(priority)
        if error:
            raise ValueError(error)

        data = self._load_queue()

        # Generate ID
        topic_id = f"{len(data['topics']) + 1:03d}-{lang}-{category}-{keyword[:20].replace(' ', '-').lower()}"

        topic = {
            "id": topic_id,
            "keyword": keyword,
            "category": category,
            "lang": lang,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "retry_count": 0
        }

        if metadata:
            topic.update(metadata)

        # Final validation of complete topic
        errors = validate_topic_data(topic)
        if errors:
            raise ValueError(f"Topic validation failed: {', '.join(errors)}")

        data['topics'].append(topic)
        self._save_queue(data)
        return topic_id

    def get_stats(self) -> Dict:
        """Get queue statistics"""
        data = self._load_queue()
        stats = {
            "total": len(data['topics']),
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "by_category": {"tech": 0, "business": 0, "lifestyle": 0, "society": 0, "entertainment": 0, "sports": 0, "finance": 0, "education": 0},
            "by_language": {"en": 0, "ko": 0, "ja": 0}
        }

        for topic in data['topics']:
            status = topic.get('status', 'pending')
            stats[status] = stats.get(status, 0) + 1

            category = topic.get('category', 'tech')
            stats['by_category'][category] = stats['by_category'].get(category, 0) + 1

            lang = topic.get('lang', 'en')
            stats['by_language'][lang] = stats['by_language'].get(lang, 0) + 1

        return stats


# Global instance
_queue = None

def get_queue() -> TopicQueue:
    """Get or create global queue instance"""
    global _queue
    if _queue is None:
        _queue = TopicQueue()
    return _queue


# Convenience functions
def reserve_topics(count: int = 3, priority_min: int = 1) -> List[Dict]:
    """Reserve topics for processing"""
    return get_queue().reserve_topics(count, priority_min)


def mark_completed(topic_id: str):
    """Mark topic as completed"""
    get_queue().mark_completed(topic_id)


def mark_failed(topic_id: str, error_message: str = ""):
    """Mark topic as failed"""
    get_queue().mark_failed(topic_id, error_message)


def cleanup_stuck_topics(hours: int = 24):
    """Clean up stuck topics"""
    get_queue().cleanup_stuck_topics(hours)


def add_topic(keyword: str, category: str, lang: str,
              priority: int = 5, metadata: Optional[Dict] = None) -> str:
    """Add new topic to queue"""
    return get_queue().add_topic(keyword, category, lang, priority, metadata)


def get_stats() -> Dict:
    """Get queue statistics"""
    return get_queue().get_stats()


if __name__ == "__main__":
    # CLI interface
    import sys

    if len(sys.argv) < 2:
        print("Usage: python topic_queue.py [stats|cleanup|reserve]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "stats":
        stats = get_stats()
        print(json.dumps(stats, indent=2))

    elif command == "cleanup":
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        cleanup_stuck_topics(hours)
        print(f"Cleaned up topics stuck for {hours}+ hours")

    elif command == "reserve":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        topics = reserve_topics(count)
        print(json.dumps(topics, indent=2, ensure_ascii=False))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
