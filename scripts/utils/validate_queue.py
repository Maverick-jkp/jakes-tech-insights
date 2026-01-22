#!/usr/bin/env python3
"""
Validate topics_queue.json before commit.
Usage: python scripts/utils/validate_queue.py
"""
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from validation import validate_topic_data

def main():
    try:
        queue_file = Path('data/topics_queue.json')

        if not queue_file.exists():
            print("❌ data/topics_queue.json not found")
            sys.exit(1)

        with open(queue_file, 'r') as f:
            queue = json.load(f)

        errors_found = False

        for topic in queue.get('topics', []):
            errors = validate_topic_data(topic)
            if errors:
                print(f"❌ Topic '{topic.get('id', 'unknown')}' has errors:")
                for error in errors:
                    print(f"   - {error}")
                errors_found = True

        if errors_found:
            sys.exit(1)

        print(f"✅ Validated {len(queue.get('topics', []))} topics")
        sys.exit(0)

    except Exception as e:
        print(f"❌ Validation failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
