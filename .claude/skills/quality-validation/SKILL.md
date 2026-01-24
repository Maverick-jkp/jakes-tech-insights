---
name: quality-validation
description: Automated content quality validation with word count checks (800-2000 words), AI phrase blacklist detection, SEO validation (meta descriptions, images), and frontmatter verification. Use when validating generated content, checking posts before deployment, or ensuring quality standards compliance. Non-blocking warnings for minor issues.
---

# Quality Validation Skill

Automated content validation with word count, AI phrase detection, SEO checks, and frontmatter validation.

---

## When to Use This Skill

**Activate this skill when:**
- User requests "quality check", "validate content", or "run quality gate"
- Need to verify posts meet quality standards before publishing
- Checking for AI-generated phrases (blacklist detection)
- Validating SEO requirements (meta descriptions, images)
- Verifying frontmatter completeness and correctness

**Do NOT use this skill for:**
- Generating new content → Use `content-generation` skill
- Hugo build operations → Use `hugo-operations` skill
- Topic queue management → Use `keyword-curation` skill

**Examples:**
- "Run quality checks on recent posts"
- "Validate content quality"
- "Check if posts pass quality gate"

---

## Skill Boundaries

**This skill handles:**
- ✅ Word count validation (800-2000 words for EN/KO, 3000-7500 chars for JA)
- ✅ AI phrase blacklist detection
- ✅ SEO validation (meta descriptions, keywords, images)
- ✅ Frontmatter verification (YAML syntax, required fields)
- ✅ References section check (2+ external links)
- ✅ Quality report generation (JSON format)

**Defer to other skills:**
- ❌ Content generation → Use `content-generation` skill
- ❌ Fixing content issues → Manual editing or regeneration
- ❌ Hugo build → Use `hugo-operations` skill
- ❌ Topic queue → Use `keyword-curation` skill

---

## Quick Start

```bash
# Run quality gate on all content
python scripts/quality_gate.py

# View results
cat quality_report.json

# Run AI reviewer (optional)
python scripts/ai_reviewer.py
cat ai_review_report.json
```

---

## Quality Gate Checks

### 1. Word Count Validation

**Requirements**:

| Language | Minimum | Target | Maximum |
|----------|---------|--------|---------|
| English  | 800     | 900-1,200 | 2,000 |
| Korean   | 800     | 900-1,200 | 2,000 |
| Japanese | 3,000 chars | 4,000-5,000 chars | 7,500 chars |

**Check**:
- Counts words (EN/KO) or characters (JA)
- FAIL if below minimum
- WARN if above maximum
- PASS if within range

### 2. AI Phrase Blacklist

**English Banned Phrases**:
- "revolutionary"
- "game-changer"
- "cutting-edge"
- "it's important to note"
- "in today's digital landscape"
- "in conclusion" (unless in conclusion section)
- "in summary" (unless in conclusion section)

**Korean Banned Phrases**:
- "물론"
- "혁신적"
- "게임체인저"
- "디지털 시대"
- "중요한 점은"

**Japanese Banned Phrases**:
- "もちろん"
- "革新的"
- "ゲームチェンジャー"
- "重要なのは"
- "結論として"

**Check**:
- Searches content for blacklisted phrases
- FAIL if any found
- Reports phrase and line number

**Full list**: `scripts/quality_gate.py` lines ~50-100

### 3. SEO Validation

**Meta Description**:
- ✅ Exists in frontmatter
- ✅ Length: 120-160 characters
- ❌ FAIL if missing or out of range

**Keyword Density**:
- Target: 5-7 natural mentions
- Not enforced (guidance only)
- Avoid keyword stuffing

**Featured Image**:
- ✅ Exists in frontmatter
- ⚠️ WARN if missing (not blocking)
- Should be Unsplash URL

**Image Alt Text**:
- ✅ Should describe image
- ✅ Include keyword naturally
- Not currently validated (future enhancement)

### 4. References Check

**Requirements**:
- ✅ ## References section exists
- ✅ 2+ external links
- ✅ Reputable sources

**Check**:
- Searches for "## References" heading
- FAIL if missing
- Counts external links
- WARN if < 2 links

### 5. Frontmatter Validation

**Required Fields**:
```yaml
title: "Post Title"
date: 2026-01-23T18:00:00+09:00  # KST timezone
categories: ["category"]
tags: ["tag1", "tag2"]
description: "120-160 char description"
image: "https://images.unsplash.com/..."
imageCredit: "Photo by [Name](URL)"
lang: "en"  # or "ko" or "ja"
```

**Check**:
- ✅ Valid YAML syntax
- ✅ All required fields present
- ✅ Date format correct (ISO 8601 with KST)
- ✅ Category valid (8 categories)
- ✅ Language valid (en/ko/ja)

---

## Quality Report Format

**Location**: `quality_report.json`

**Structure**:
```json
{
  "timestamp": "2026-01-23T21:50:00+09:00",
  "files_checked": 63,
  "passed": 60,
  "failed": 3,
  "warnings": 5,
  "details": [
    {
      "file": "content/en/tech/2026-01-23-ai-trends.md",
      "status": "PASS",
      "checks": {
        "word_count": {"status": "PASS", "value": 1050},
        "ai_phrases": {"status": "PASS", "found": []},
        "seo": {"status": "PASS", "description_length": 145},
        "references": {"status": "PASS", "count": 3},
        "frontmatter": {"status": "PASS"}
      }
    },
    {
      "file": "content/en/tech/2026-01-22-bad-post.md",
      "status": "FAIL",
      "checks": {
        "word_count": {"status": "FAIL", "value": 650, "minimum": 800},
        "ai_phrases": {"status": "FAIL", "found": ["revolutionary"]},
        "seo": {"status": "PASS", "description_length": 135},
        "references": {"status": "PASS", "count": 2},
        "frontmatter": {"status": "PASS"}
      }
    }
  ]
}
```

---

## AI Reviewer (Optional)

### 5-Criteria Scoring

**1. Authenticity (1-10)**:
- Human tone (not robotic)
- Natural language
- Personal perspective (when appropriate)
- Avoids AI clichés

**2. Value (1-10)**:
- Practical insights
- Actionable advice
- Real-world examples
- Depth of analysis

**3. Engagement (1-10)**:
- Clear structure
- Compelling introduction
- Logical flow
- Strong conclusion

**4. Technical Accuracy (1-10)**:
- Correct information
- Up-to-date facts
- Proper terminology
- No misleading claims

**5. SEO Quality (1-10)**:
- Keyword integration
- Meta description quality
- Heading structure
- Link quality

### Recommendation Thresholds

**Average Score**:
- **≥ 8.0**: APPROVE (publish immediately)
- **6.0-7.9**: REVISE (minor improvements needed)
- **< 6.0**: REJECT (major rewrite needed)

### AI Review Report

**Location**: `ai_review_report.json`

**Structure**:
```json
{
  "timestamp": "2026-01-23T21:55:00+09:00",
  "file": "content/en/tech/2026-01-23-ai-trends.md",
  "scores": {
    "authenticity": 8.5,
    "value": 8.0,
    "engagement": 9.0,
    "technical_accuracy": 8.5,
    "seo_quality": 8.0
  },
  "average": 8.4,
  "recommendation": "APPROVE",
  "feedback": [
    "Strong human tone with natural language",
    "Practical insights with real-world examples",
    "Excellent structure and flow",
    "Accurate technical information",
    "Good SEO integration"
  ],
  "suggestions": [
    "Consider adding one more real-world example in section 2"
  ]
}
```

---

## Common Failures & Fixes

### Failure 1: Word Count Too Low

**Error**: `Word count 650 below minimum 800`

**Cause**: Draft agent didn't generate enough content

**Fix**:
```python
# In scripts/generate_posts.py, line ~1100
max_tokens=12000  # Increase to 14000

# Or update system prompt to request longer content
"Write 900-1200 words..."
```

### Failure 2: AI Phrases Detected

**Error**: `Found blacklisted phrase: "revolutionary" at line 15`

**Cause**: Draft agent used banned phrase

**Fix 1** (Immediate): Manual edit
```bash
# Edit the file
vim content/en/tech/2026-01-23-post.md
# Remove "revolutionary", replace with specific term
```

**Fix 2** (Prevent future): Update prompt
```python
# In scripts/generate_posts.py, add to system prompt:
"NEVER use these words: revolutionary, game-changer, cutting-edge,
it's important to note, in today's digital landscape"
```

### Failure 3: Missing References

**Error**: `No References section found`

**Cause**: Editor agent didn't add references

**Fix 1** (Immediate): Manual add
```markdown
## References
1. [Source 1](https://example.com)
2. [Source 2](https://example.com)
```

**Fix 2** (Prevent future): Verify editor prompt
```python
# In scripts/generate_posts.py, Editor agent:
"You MUST include a ## References section with 2+ external links"
```

### Failure 4: Meta Description Out of Range

**Error**: `Meta description 95 chars, should be 120-160`

**Cause**: Description too short/long

**Fix** (Immediate): Edit frontmatter
```yaml
description: "Expand this to 120-160 characters with relevant keywords and compelling hook"
```

---

## Integration with CI/CD

### GitHub Actions Workflow

**File**: `.github/workflows/daily-content.yml`

**Steps**:
```yaml
- name: Run tests
  run: pytest

- name: Generate content
  run: python scripts/generate_posts.py --count 3

- name: Quality gate (blocking)
  run: python scripts/quality_gate.py

- name: AI review (non-blocking)
  run: python scripts/ai_reviewer.py || true

- name: Create PR
  if: success()
  run: gh pr create ...
```

**Behavior**:
- ✅ Quality gate failure → BLOCKS PR creation
- ⚠️ AI reviewer → INFORMATIONAL only (doesn't block)

### Manual Validation

```bash
# Before committing
python scripts/quality_gate.py

# If failures, fix them
vim content/en/tech/2026-01-23-post.md

# Re-run until pass
python scripts/quality_gate.py

# Optional: AI review
python scripts/ai_reviewer.py

# If approved, commit
git add content/
git commit -m "feat: Add AI trends article"
```

---

## Testing

### Test Quality Gate

```bash
# Create test post with known issues
cat > content/en/tech/test-post.md <<EOF
---
title: "Test Post"
date: 2026-01-23T18:00:00+09:00
categories: ["tech"]
tags: ["test"]
description: "Too short"
image: ""
lang: "en"
---

This revolutionary post is too short.
EOF

# Run quality gate (should fail)
python scripts/quality_gate.py
# Expected: FAIL (word count, AI phrase, description length, missing image, no references)

# Fix issues
vim content/en/tech/test-post.md

# Re-run (should pass)
python scripts/quality_gate.py
```

### Test AI Reviewer

```bash
# Run on recent post
python scripts/ai_reviewer.py

# Check results
cat ai_review_report.json

# Verify scoring is reasonable
jq '.average' ai_review_report.json
# Should be 6.0-10.0
```

---

## Extending Quality Checks

### Add New AI Phrase

**File**: `scripts/quality_gate.py`

**Location**: Lines ~50-100

```python
AI_PHRASES_EN = [
    "revolutionary",
    "game-changer",
    # Add here:
    "paradigm shift",
    "disruptive innovation",
]
```

### Add New Validation Rule

**Example**: Check for minimum heading count

```python
# In scripts/quality_gate.py

def check_heading_count(content):
    """Ensure 3-4 ## headings."""
    headings = re.findall(r'^## ', content, re.MULTILINE)
    count = len(headings)

    if count < 3:
        return {"status": "FAIL", "count": count, "minimum": 3}
    elif count > 4:
        return {"status": "WARN", "count": count, "recommended": "3-4"}
    else:
        return {"status": "PASS", "count": count}
```

---

## Related Skills

- **content-generation**: Generate posts (runs quality gate automatically)
- **hugo-operations**: Preview posts locally
- **keyword-curation**: Manage topic queue

---

## References

- **Quality Standards**: `.claude/docs/quality-standards.md`
- **Architecture**: `.claude/docs/architecture.md`
- **Troubleshooting**: `.claude/docs/troubleshooting.md`

---

**Skill Version**: 1.1
**Last Updated**: 2026-01-24
**Maintained By**: Jake's Tech Insights project
