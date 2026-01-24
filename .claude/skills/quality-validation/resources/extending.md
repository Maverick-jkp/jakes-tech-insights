# Extending Quality Checks

Guide for adding new validation rules to the quality gate.

---

## Overview

**Quality gate script**: `scripts/quality_gate.py`

Current checks (6 total):
1. Word count validation
2. AI phrase blacklist
3. SEO validation (meta description)
4. References section
5. Frontmatter validation
6. Featured image (warning only)

---

## Adding a New Check

### Example: Minimum Heading Count

**Goal**: Ensure 3-4 ## headings in each post

**Step 1: Add check function**

Location: `scripts/quality_gate.py` (add near other check functions)

```python
def check_heading_count(content):
    """
    Ensure 3-4 ## headings (not including title).

    Args:
        content (str): Markdown content

    Returns:
        dict: {"status": "PASS/WARN/FAIL", "count": int}
    """
    # Find all ## headings (not #)
    headings = re.findall(r'^## ', content, re.MULTILINE)
    count = len(headings)

    if count < 3:
        return {
            "status": "FAIL",
            "count": count,
            "minimum": 3,
            "message": f"Only {count} sections, need at least 3"
        }
    elif count > 4:
        return {
            "status": "WARN",
            "count": count,
            "recommended": "3-4",
            "message": f"{count} sections may be too many"
        }
    else:
        return {
            "status": "PASS",
            "count": count
        }
```

**Step 2: Add to validation pipeline**

Location: `scripts/quality_gate.py` main validation loop

```python
def validate_post(file_path):
    """Run all checks on a post."""
    # ... existing checks ...

    # Add new check
    heading_result = check_heading_count(content)
    results["checks"]["heading_count"] = heading_result

    # Update overall status
    if heading_result["status"] == "FAIL":
        results["status"] = "FAIL"

    return results
```

**Step 3: Update report format**

The check result is automatically included in `quality_report.json`:

```json
{
  "file": "content/en/tech/post.md",
  "status": "FAIL",
  "checks": {
    "word_count": {"status": "PASS", "value": 1050},
    "heading_count": {"status": "FAIL", "count": 2, "minimum": 3}
  }
}
```

**Step 4: Test**

```bash
# Create test post with 2 headings
cat > content/en/tech/test-headings.md <<'EOF'
---
title: "Test"
---

## Section 1
Content here.

## Section 2
Content here.
EOF

# Run quality gate (should fail)
python scripts/quality_gate.py

# Expected: FAIL (heading_count check)

# Fix post (add Section 3)
# Re-run (should pass)
```

---

## Check Types

### 1. Blocking Checks (FAIL)

Stop deployment if failed.

**Current blocking checks**:
- Word count below minimum
- AI phrases detected
- Meta description missing/wrong length
- No References section
- Invalid frontmatter

**When to make blocking**:
- Critical quality issue
- Will cause deployment errors
- Must be fixed before publish

### 2. Warning Checks (WARN)

Informational only, don't block deployment.

**Current warning checks**:
- Word count above maximum
- Featured image missing
- Too many headings (from example above)

**When to make warning**:
- Nice to have, not critical
- Subjective quality measure
- May have valid exceptions

---

## Common Check Patterns

### Pattern 1: Count-Based

Check if count is within range.

```python
def check_something_count(content):
    items = re.findall(r'pattern', content)
    count = len(items)

    if count < MIN:
        return {"status": "FAIL", "count": count}
    elif count > MAX:
        return {"status": "WARN", "count": count}
    else:
        return {"status": "PASS", "count": count}
```

### Pattern 2: Presence Check

Check if something exists.

```python
def check_something_exists(content):
    if "expected pattern" in content:
        return {"status": "PASS"}
    else:
        return {"status": "FAIL", "message": "Missing expected pattern"}
```

### Pattern 3: Format Validation

Check if format is correct.

```python
def check_something_format(value):
    if re.match(r'^expected-format$', value):
        return {"status": "PASS"}
    else:
        return {
            "status": "FAIL",
            "message": f"Invalid format: {value}"
        }
```

---

## Example: Check for Code Blocks

**Goal**: Ensure tech posts include at least 1 code block

```python
def check_code_blocks(content, category):
    """
    Tech posts should include code examples.

    Args:
        content (str): Markdown content
        category (str): Post category

    Returns:
        dict: {"status": "PASS/WARN", "count": int}
    """
    # Only check tech category
    if category != "tech":
        return {"status": "PASS", "message": "Not a tech post"}

    # Find code blocks (```...```)
    code_blocks = re.findall(r'```[\s\S]*?```', content)
    count = len(code_blocks)

    if count == 0:
        return {
            "status": "WARN",
            "count": 0,
            "message": "Tech post without code examples"
        }
    else:
        return {
            "status": "PASS",
            "count": count
        }
```

**Add to pipeline**:
```python
# In validate_post()
category = frontmatter.get("categories", [""])[0]
code_result = check_code_blocks(content, category)
results["checks"]["code_blocks"] = code_result
```

---

## Example: Check Link Quality

**Goal**: Ensure external links are from reputable sources

```python
def check_link_quality(content):
    """
    Check if external links are from known good sources.

    Returns:
        dict: {"status": "PASS/WARN", "suspicious": list}
    """
    # Extract all URLs
    urls = re.findall(r'https?://[^\s\)]+', content)

    # Reputable domains
    GOOD_DOMAINS = [
        "github.com", "stackoverflow.com", "medium.com",
        "dev.to", "wikipedia.org", "arxiv.org"
    ]

    suspicious = []
    for url in urls:
        domain = url.split('/')[2]  # Extract domain
        if not any(good in domain for good in GOOD_DOMAINS):
            suspicious.append(url)

    if suspicious:
        return {
            "status": "WARN",
            "suspicious": suspicious,
            "message": f"Found {len(suspicious)} links from unknown sources"
        }
    else:
        return {"status": "PASS", "link_count": len(urls)}
```

---

## Testing New Checks

### Unit Test

Create test cases in `tests/test_quality_gate.py`:

```python
def test_heading_count():
    """Test heading count validation."""

    # Test: Too few headings (should fail)
    content = """
## Section 1
Text here.

## Section 2
Text here.
"""
    result = check_heading_count(content)
    assert result["status"] == "FAIL"
    assert result["count"] == 2

    # Test: Right number of headings (should pass)
    content = """
## Section 1
## Section 2
## Section 3
"""
    result = check_heading_count(content)
    assert result["status"] == "PASS"
    assert result["count"] == 3
```

### Integration Test

```bash
# Create test post
mkdir -p content/en/tech
cat > content/en/tech/test-new-check.md <<'EOF'
---
title: "Test Post"
date: 2026-01-24T18:00:00+09:00
categories: ["tech"]
tags: ["test"]
description: "Test post for new validation check"
lang: "en"
---

## Section 1
Content here.

## Section 2
Content here.
EOF

# Run quality gate
python scripts/quality_gate.py

# Check report
jq '.details[] | select(.file | contains("test-new-check"))' quality_report.json
```

---

## Best Practices

### 1. Make Checks Specific

**Bad**: "Content quality is low"
**Good**: "Post has only 2 sections, need at least 3"

### 2. Provide Actionable Feedback

Include what's wrong and how to fix it:
```python
{
    "status": "FAIL",
    "count": 2,
    "minimum": 3,
    "message": "Only 2 sections. Add 1-2 more ## headings."
}
```

### 3. Use Appropriate Severity

- **FAIL**: Must fix before deploy
- **WARN**: Nice to fix, not critical
- **PASS**: All good

### 4. Test Edge Cases

- Empty content
- Malformed markdown
- Missing frontmatter
- Unicode characters

---

## Related

- **AI Phrases**: `resources/ai-phrases.md` - Blacklist management
- **AI Reviewer**: `resources/ai-reviewer.md` - Optional scoring
- **Quality Standards**: `.claude/docs/quality-standards.md` - Overall criteria

---

**Version**: 1.2
**Last Updated**: 2026-01-24
**Maintained By**: Jake's Tech Insights project
