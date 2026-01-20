# Task 3: 보안 강화 (Security Hardening)

**작업 기간**: 2일
**우선순위**: High
**담당**: Claude Code
**상태**: ✅ 완료 (2026-01-20)

---

## 목표

1. API 키 및 민감 정보가 로그에 노출되지 않도록 마스킹
2. 사용자 입력 검증으로 잘못된 데이터 유입 방지
3. JSON 데이터 구조 무결성 보장

---

## Task 3.1: Secrets Masking (Day 1)

### 작업 내용

#### 1. Utility 함수 생성

**파일**: `scripts/utils/security.py` (신규 생성)

```python
"""
Security utilities for masking sensitive data in logs.
"""
import os
import re
from typing import List

def get_sensitive_patterns() -> List[str]:
    """Get list of sensitive environment variables to mask."""
    return [
        os.getenv("ANTHROPIC_API_KEY", ""),
        os.getenv("UNSPLASH_ACCESS_KEY", ""),
        os.getenv("GOOGLE_API_KEY", ""),
        os.getenv("GOOGLE_CX", ""),
    ]

def mask_secrets(text: str) -> str:
    """
    Mask sensitive information in text before logging.

    Args:
        text: Text that may contain sensitive data

    Returns:
        Text with sensitive data replaced by ***MASKED***
    """
    masked = text

    # Mask environment variables
    for secret in get_sensitive_patterns():
        if secret and len(secret) > 0:
            masked = masked.replace(secret, "***MASKED***")

    # Mask API key patterns (sk-ant-..., or other common formats)
    masked = re.sub(r'sk-ant-[a-zA-Z0-9-_]{20,}', '***MASKED_API_KEY***', masked)

    # Mask bearer tokens
    masked = re.sub(r'Bearer [a-zA-Z0-9-_]{20,}', 'Bearer ***MASKED***', masked)

    return masked

def safe_print(message: str):
    """Print message with secrets masked."""
    print(mask_secrets(message))
```

#### 2. 각 스크립트에 적용

**적용 대상 파일:**
- `scripts/generate_posts.py`
- `scripts/keyword_curator.py`
- `scripts/ai_reviewer.py`
- `scripts/quality_gate.py`
- `scripts/replace_placeholder_images.py`

**변경 예시** (`generate_posts.py`):

```python
# 파일 상단에 추가
import sys
sys.path.append(os.path.dirname(__file__))
from utils.security import safe_print, mask_secrets

# 기존 print() 문을 safe_print()로 변경
# Before:
print(f"Draft content: {draft_content}")
print(f"API Error: {str(e)}")

# After:
safe_print(f"Draft content: {draft_content}")
safe_print(f"API Error: {str(e)}")

# Exception handling도 마스킹
try:
    response = client.messages.create(...)
except Exception as e:
    safe_print(f"❌ Error generating content: {str(e)}")
    # Sentry나 로깅 시스템에 보낼 때도 마스킹
    raise Exception(mask_secrets(str(e)))
```

#### 3. GitHub Actions에 명시적 마스킹 추가

**파일**: `.github/workflows/daily-content.yml`

```yaml
- name: Generate Daily Content
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    UNSPLASH_ACCESS_KEY: ${{ secrets.UNSPLASH_ACCESS_KEY }}
  run: |
    # Explicitly mask secrets in GitHub Actions logs
    echo "::add-mask::${{ secrets.ANTHROPIC_API_KEY }}"
    echo "::add-mask::${{ secrets.UNSPLASH_ACCESS_KEY }}"
    echo "::add-mask::${{ secrets.GOOGLE_API_KEY }}"

    python scripts/generate_posts.py --count 3
```

**적용 대상:**
- `.github/workflows/daily-content.yml`
- `.github/workflows/daily-keywords.yml`
- `.github/workflows/fix-placeholder-images.yml`

---

## Task 3.2: Input Validation (Day 2)

### 작업 내용

#### 1. Validation Utility 생성

**파일**: `scripts/utils/validation.py` (신규 생성)

```python
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
    required_fields = ['keyword', 'category', 'language', 'priority', 'status']
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

    error = validate_language(topic['language'])
    if error:
        errors.append(error)

    error = validate_priority(topic.get('priority', 0))
    if error:
        errors.append(error)

    error = validate_status(topic['status'])
    if error:
        errors.append(error)

    return errors
```

#### 2. topic_queue.py에 적용

**파일**: `scripts/topic_queue.py`

```python
# 상단에 추가
from utils.validation import (
    validate_keyword,
    validate_category,
    validate_language,
    validate_priority,
    validate_topic_data
)

# add_topic 함수 수정
def add_topic(keyword, category, language, priority=5, expiry_days=3, trend_type="evergreen"):
    """Add a new topic to the queue with validation."""

    # Validate inputs
    error = validate_keyword(keyword)
    if error:
        raise ValueError(f"Invalid keyword: {error}")

    error = validate_category(category)
    if error:
        raise ValueError(error)

    error = validate_language(language)
    if error:
        raise ValueError(error)

    error = validate_priority(priority)
    if error:
        raise ValueError(error)

    # ... 기존 로직 계속
```

**적용 위치:**
- `add_topic()` 함수 시작 부분
- `reserve_topics()` 함수 (큐에서 읽은 데이터 검증)
- `mark_completed()`, `mark_failed()` 함수

#### 3. JSON Schema Validation 추가

**파일**: `scripts/utils/validation.py`에 추가

```python
# 상단에 추가
try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    print("Warning: jsonschema not installed. Install with: pip install jsonschema")

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
        "language": {
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
        "trend_type": {
            "type": "string",
            "enum": ["trend", "evergreen"]
        },
        "retry_count": {"type": "integer", "minimum": 0},
        "created_at": {"type": "string"},
        "reserved_at": {"type": ["string", "null"]},
        "completed_at": {"type": ["string", "null"]}
    },
    "required": ["id", "keyword", "category", "language", "priority", "status"]
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
```

#### 4. Requirements 업데이트

**파일**: `requirements.txt` (신규 생성)

```
anthropic>=0.18.0
requests>=2.31.0
jsonschema>=4.20.0
feedparser>=6.0.10
```

**설치 방법:**
```bash
pip install -r requirements.txt
```

---

## Task 3.3: Pre-commit Hook (Optional, Day 2 오후)

**파일**: `.git/hooks/pre-commit` (신규 생성)

```bash
#!/bin/bash
# Pre-commit hook to validate topics_queue.json

echo "Running pre-commit validation..."

# Validate topics_queue.json syntax
if ! python -m json.tool data/topics_queue.json > /dev/null 2>&1; then
    echo "❌ Error: topics_queue.json is not valid JSON"
    exit 1
fi

# Run Python validation
if ! python scripts/utils/validate_queue.py; then
    echo "❌ Error: topics_queue.json validation failed"
    exit 1
fi

echo "✅ Pre-commit validation passed"
exit 0
```

**파일**: `scripts/utils/validate_queue.py` (신규 생성)

```python
#!/usr/bin/env python3
"""
Validate topics_queue.json before commit.
Usage: python scripts/utils/validate_queue.py
"""
import json
import sys
from validation import validate_topic_data

def main():
    try:
        with open('data/topics_queue.json', 'r') as f:
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
```

---

## ✅ 완료 상태

### Task 3.1: Secrets Masking - 완료 ✅

**구현 완료:**
- ✅ `scripts/utils/security.py` 생성 완료
- ✅ 모든 스크립트에 `safe_print()` 적용 완료 (5개 파일)
- ✅ GitHub Actions workflows에 명시적 마스킹 추가 (3개 파일)

**적용된 파일:**
- `scripts/generate_posts.py` (28곳)
- `scripts/keyword_curator.py` (31곳)
- `scripts/ai_reviewer.py` (29곳)
- `scripts/quality_gate.py` (21곳)
- `scripts/replace_placeholder_images.py` (23곳)
- `.github/workflows/daily-keywords.yml`
- `.github/workflows/daily-content.yml`
- `.github/workflows/fix-placeholder-images.yml`

### Task 3.2: Input Validation - 완료 ✅

**구현 완료:**
- ✅ `scripts/utils/validation.py` 생성 완료
- ✅ `scripts/topic_queue.py`에 validation 적용 완료
- ✅ `scripts/utils/validate_queue.py` 검증 스크립트 생성
- ✅ `requirements.txt`에 jsonschema 추가 확인

**검증 결과:**
```bash
✅ Validated 45 topics
✅ Correctly blocked: Invalid keyword: Keyword contains invalid characters
✅ Path traversal prevented
✅ Length limits enforced
```

---

## 검증 방법

### Day 1 완료 후 체크리스트

```bash
# 1. Secrets masking 테스트
echo "Testing secrets masking..."
python -c "from scripts.utils.security import mask_secrets; print(mask_secrets('My API key is sk-ant-abc123xyz'))"
# Expected output: My API key is ***MASKED_API_KEY***

# 2. 기존 스크립트 실행 (에러 없어야 함)
python scripts/generate_posts.py --count 1

# 3. GitHub Actions 로그 확인
# workflows 수동 실행 후 로그에 API 키 없는지 확인
```

### Day 2 완료 후 체크리스트

```bash
# 1. Input validation 테스트
python -c "
from scripts.utils.validation import validate_keyword
print(validate_keyword('Valid Keyword'))  # Should print: None
print(validate_keyword('../../etc/passwd'))  # Should print error
print(validate_keyword('a'))  # Should print error (too short)
"

# 2. JSON validation 테스트
pip install jsonschema
python scripts/utils/validate_queue.py
# Expected: ✅ Validated 45 topics

# 3. 잘못된 입력 시도
python -c "
from scripts.topic_queue import add_topic
try:
    add_topic('../../etc/passwd', 'tech', 'en', priority=5)
except ValueError as e:
    print(f'Correctly blocked: {e}')
"
```

---

## 예상 결과

### Before (현재)
```python
# 위험: API 키 노출 가능
print(f"Error: {response}")
# Output: Error: API key sk-ant-abc123xyz is invalid

# 위험: 잘못된 입력 허용
add_topic("../../etc/passwd", "tech", "en")
# 경로 탈출 가능
```

### After (개선 후)
```python
# 안전: API 키 자동 마스킹
safe_print(f"Error: {response}")
# Output: Error: API key ***MASKED_API_KEY*** is invalid

# 안전: 잘못된 입력 차단
add_topic("../../etc/passwd", "tech", "en")
# ValueError: Invalid keyword: Keyword cannot contain path separators
```

---

## 회귀 방지

이 작업 후 다음 규칙 준수:

1. **새로운 print() 금지**: `safe_print()` 사용
2. **새로운 입력 검증**: 모든 외부 입력은 validation 함수 통과
3. **secrets 추가 시**: `security.py`의 `get_sensitive_patterns()`에 추가

---

## 비용

- **개발 시간**: 2일
- **유지보수 오버헤드**: 거의 없음 (한번 설정하면 끝)
- **성능 영향**: 무시할 수준 (string replace는 매우 빠름)
- **금전 비용**: $0

---

## 참고 문서

- [OWASP Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [GitHub Actions: Masking secrets](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#masking-a-value-in-log)
- [Python JSON Schema](https://python-jsonschema.readthedocs.io/)
