"""
Input validation utilities for topic queue and content generation.
"""
import re
from typing import Optional, List

# Allowed categories (from hugo.toml)
VALID_CATEGORIES = [
    'tech', 'business', 'lifestyle', 'society',
    'entertainment', 'sports', 'finance', 'education'
]

# Allowed languages
VALID_LANGUAGES = ['en', 'ko', 'ja']

# Allowed statuses
VALID_STATUSES = ['pending', 'in_progress', 'completed', 'failed']

def validate_keyword(keyword: str) -> Optional[str]:
    """
    Validate keyword input.

    Returns:
        None if valid, error message string if invalid
    """
    # Length check
    if not keyword or len(keyword.strip()) < 2:
        return "Keyword must be at least 2 characters"

    if len(keyword) > 100:
        return "Keyword must be less than 100 characters"

    # Character whitelist: alphanumeric, Korean, Japanese, spaces, hyphens
    # Block: path separators, special chars that could cause injection
    if not re.match(r'^[\w\s가-힣ぁ-んァ-ヶー一-龯\-]+$', keyword):
        return "Keyword contains invalid characters"

    # Path traversal prevention
    if '..' in keyword or '/' in keyword or '\\' in keyword:
        return "Keyword cannot contain path separators"

    # Prevent excessively long words (potential DoS)
    words = keyword.split()
    if any(len(word) > 50 for word in words):
        return "Individual words in keyword cannot exceed 50 characters"

    return None

def validate_category(category: str) -> Optional[str]:
    """Validate category input."""
    if category not in VALID_CATEGORIES:
        return f"Category must be one of: {', '.join(VALID_CATEGORIES)}"
    return None

def validate_language(language: str) -> Optional[str]:
    """Validate language input."""
    if language not in VALID_LANGUAGES:
        return f"Language must be one of: {', '.join(VALID_LANGUAGES)}"
    return None

def validate_priority(priority: int) -> Optional[str]:
    """Validate priority input."""
    if not isinstance(priority, int):
        return "Priority must be an integer"

    if priority < 1 or priority > 10:
        return "Priority must be between 1 and 10"

    return None

def validate_status(status: str) -> Optional[str]:
    """Validate status input."""
    if status not in VALID_STATUSES:
        return f"Status must be one of: {', '.join(VALID_STATUSES)}"
    return None

def validate_topic_data(topic: dict) -> List[str]:
    """
    Validate entire topic dictionary.

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    # Required fields
    required_fields = ['keyword', 'category', 'lang', 'priority', 'status']
    for field in required_fields:
        if field not in topic:
            errors.append(f"Missing required field: {field}")

    if errors:  # If required fields missing, stop here
        return errors

    # Validate each field
    error = validate_keyword(topic['keyword'])
    if error:
        errors.append(f"Invalid keyword: {error}")

    error = validate_category(topic['category'])
    if error:
        errors.append(error)

    error = validate_language(topic['lang'])
    if error:
        errors.append(error)

    error = validate_priority(topic.get('priority', 0))
    if error:
        errors.append(error)

    error = validate_status(topic['status'])
    if error:
        errors.append(error)

    return errors


# JSON Schema validation (optional, requires jsonschema package)
try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

# Topic JSON schema
TOPIC_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^[0-9]{3}-[a-z]{2}-[a-z]+-[a-z0-9-]+$"
        },
        "keyword": {"type": "string", "minLength": 2, "maxLength": 100},
        "category": {
            "type": "string",
            "enum": VALID_CATEGORIES
        },
        "lang": {
            "type": "string",
            "enum": VALID_LANGUAGES
        },
        "priority": {
            "type": "integer",
            "minimum": 1,
            "maximum": 10
        },
        "status": {
            "type": "string",
            "enum": VALID_STATUSES
        },
        "expiry_days": {"type": "integer", "minimum": 1, "maximum": 30},
        "keyword_type": {
            "type": "string",
            "enum": ["trend", "evergreen"]
        },
        "retry_count": {"type": "integer", "minimum": 0},
        "created_at": {"type": "string"},
        "reserved_at": {"type": ["string", "null"]},
        "completed_at": {"type": ["string", "null"]}
    },
    "required": ["id", "keyword", "category", "lang", "priority", "status"]
}

def validate_topic_schema(topic: dict) -> Optional[str]:
    """
    Validate topic against JSON schema.

    Returns:
        None if valid, error message if invalid
    """
    if not JSONSCHEMA_AVAILABLE:
        return None  # Skip if jsonschema not installed

    try:
        jsonschema.validate(instance=topic, schema=TOPIC_SCHEMA)
        return None
    except jsonschema.ValidationError as e:
        return f"Schema validation failed: {e.message}"
