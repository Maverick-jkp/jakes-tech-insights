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

## Dependencies

**Required Python packages:**
- `pyyaml==6.0` - YAML frontmatter parsing
- `python-dateutil==2.8.2` - Date validation

**Installation:**
```bash
pip install -r requirements.txt
```

**Verification:**
```bash
python -c "import yaml, dateutil; print('✓ All dependencies installed')"
```

**Note**: This skill does NOT require Claude API (no API costs).

---

## Quick Start

```bash
# Run quality gate on all content
python scripts/quality_gate.py

# View results
cat quality_report.json

# Run AI reviewer (optional, requires API)
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

**English**: "revolutionary", "game-changer", "cutting-edge", "it's important to note", "in today's digital landscape"

**Korean**: "물론", "혁신적", "게임체인저", "디지털 시대", "중요한 점은"

**Japanese**: "もちろん", "革新的", "ゲームチェンジャー", "重要なのは", "結論として"

**Check**:
- Searches content for blacklisted phrases
- FAIL if any found
- Reports phrase and line number

**Full list**: See [resources/ai-phrases.md](resources/ai-phrases.md)

### 3. SEO Validation

**Meta Description**:
- ✅ Exists in frontmatter
- ✅ Length: 120-160 characters
- ❌ FAIL if missing or out of range

**Featured Image**:
- ✅ Exists in frontmatter
- ⚠️ WARN if missing (not blocking)

**Keyword Density**:
- Target: 5-7 natural mentions (not enforced)

### 4. References Check

**Requirements**:
- ✅ ## References section exists
- ✅ 2+ external links
- ✅ FAIL if missing

### 5. Frontmatter Validation

**Required Fields**:
```yaml
title: "Post Title"
date: 2026-01-24T18:00:00+09:00  # KST timezone
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
  "timestamp": "2026-01-24T21:50:00+09:00",
  "files_checked": 63,
  "passed": 60,
  "failed": 3,
  "warnings": 5,
  "details": [
    {
      "file": "content/en/tech/2026-01-24-ai-trends.md",
      "status": "PASS",
      "checks": {
        "word_count": {"status": "PASS", "value": 1050},
        "ai_phrases": {"status": "PASS", "found": []},
        "seo": {"status": "PASS", "description_length": 145},
        "references": {"status": "PASS", "count": 3},
        "frontmatter": {"status": "PASS"}
      }
    }
  ]
}
```

**Exit code**:
- `0` - All checks passed
- `1` - Critical failures (blocks deployment)

---

## AI Reviewer (Optional)

**Cost**: ~$0.02 per review (Claude API)

**5-Criteria Scoring** (1-10 scale):
1. **Authenticity** - Human tone, natural language
2. **Value** - Practical insights, actionable advice
3. **Engagement** - Clear structure, compelling flow
4. **Technical Accuracy** - Correct information
5. **SEO Quality** - Keyword integration, meta description

**Recommendation Thresholds**:
- **≥ 8.0**: APPROVE (publish immediately)
- **6.0-7.9**: REVISE (minor improvements)
- **< 6.0**: REJECT (major rewrite)

**Details**: See [resources/ai-reviewer.md](resources/ai-reviewer.md)

---

## Common Failures & Fixes

### Failure 1: Word Count Too Low

**Error**: `Word count 650 below minimum 800`

**Fix**:
```python
# In scripts/generate_posts.py, line ~1100
max_tokens=12000  # Increase to 14000

# Or update system prompt
"Write 900-1200 words..."
```

### Failure 2: AI Phrases Detected

**Error**: `Found blacklisted phrase: "revolutionary" at line 15`

**Fix (Immediate)**: Manual edit
```bash
vim content/en/tech/2026-01-24-post.md
# Remove "revolutionary", replace with specific term
```

**Fix (Prevent)**: Update prompt in `scripts/generate_posts.py`

### Failure 3: Missing References

**Error**: `No References section found`

**Fix (Immediate)**:
```markdown
## References
1. [Source 1](https://example.com)
2. [Source 2](https://example.com)
```

### Failure 4: Meta Description Out of Range

**Error**: `Meta description 95 chars, should be 120-160`

**Fix**:
```yaml
description: "Expand this to 120-160 characters with relevant keywords and compelling hook"
```

---

## Integration with CI/CD

**GitHub Actions**: `.github/workflows/daily-content.yml`

**Steps**:
```yaml
- name: Quality gate (blocking)
  run: python scripts/quality_gate.py

- name: AI review (non-blocking)
  run: python scripts/ai_reviewer.py || true
```

**Behavior**:
- ✅ Quality gate failure → BLOCKS PR creation
- ⚠️ AI reviewer → INFORMATIONAL only (doesn't block)

---

## Testing

```bash
# Create test post with known issues
cat > content/en/tech/test-post.md <<EOF
---
title: "Test Post"
date: 2026-01-24T18:00:00+09:00
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

# Fix issues and re-run
```

---

## Advanced Topics

For detailed information, see:
- **AI Phrases**: [resources/ai-phrases.md](resources/ai-phrases.md) - Complete blacklist
- **AI Reviewer**: [resources/ai-reviewer.md](resources/ai-reviewer.md) - 5-criteria scoring details
- **Extending Checks**: [resources/extending.md](resources/extending.md) - Add new validation rules

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

**Skill Version**: 1.2
**Last Updated**: 2026-01-24
**Maintained By**: Jake's Tech Insights project
