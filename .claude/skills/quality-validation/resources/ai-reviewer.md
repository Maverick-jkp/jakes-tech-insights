# AI Reviewer - 5-Criteria Scoring System

Optional AI-powered content quality review using Claude API.

---

## Overview

**Script**: `scripts/ai_reviewer.py`
**Model**: Claude Sonnet 4.5
**Output**: `ai_review_report.json`

**Status**: Optional (non-blocking)
- Quality gate failures → BLOCK deployment
- AI reviewer low scores → INFORMATIONAL only

---

## 5-Criteria Scoring

Each criterion scored 1-10 (10 = best).

### 1. Authenticity (1-10)

**What it measures**:
- Human tone (not robotic)
- Natural language flow
- Personal perspective when appropriate
- Avoids AI clichés and generic phrases

**Good examples**:
- Personal anecdotes
- Conversational transitions
- Natural question-answer flow
- Authentic opinions

**Bad examples**:
- "In today's digital landscape..."
- "It's important to note that..."
- Overly formal/stiff language
- Generic statements

---

### 2. Value (1-10)

**What it measures**:
- Practical insights user can apply
- Actionable advice (not just theory)
- Real-world examples
- Depth of analysis

**Good examples**:
- Step-by-step guides
- Code examples
- Case studies
- Specific metrics/numbers

**Bad examples**:
- Obvious advice ("work hard")
- No actionable steps
- Surface-level analysis
- Missing examples

---

### 3. Engagement (1-10)

**What it measures**:
- Clear structure (easy to scan)
- Compelling introduction (hooks reader)
- Logical flow between sections
- Strong conclusion with CTA

**Good examples**:
- Clear headings (H2, H3)
- Short paragraphs (2-4 sentences)
- Smooth transitions
- Questions that engage reader

**Bad examples**:
- Wall of text
- Random section order
- Weak introduction
- Abrupt ending

---

### 4. Technical Accuracy (1-10)

**What it measures**:
- Correct information
- Up-to-date facts (2026 context)
- Proper terminology
- No misleading claims

**Good examples**:
- Verified statistics
- Correct syntax/commands
- Latest API versions
- Honest limitations

**Bad examples**:
- Outdated information
- Wrong syntax
- Exaggerated claims
- Unverified facts

---

### 5. SEO Quality (1-10)

**What it measures**:
- Natural keyword integration (5-7 mentions)
- Quality meta description (120-160 chars)
- Proper heading structure (H1 → H2 → H3)
- Quality external links (references)

**Good examples**:
- Keywords in first 100 words
- Descriptive meta description
- Clear heading hierarchy
- 2+ reputable sources

**Bad examples**:
- Keyword stuffing
- Generic meta description
- Skipped heading levels
- No external links

---

## Recommendation Thresholds

**Average score** (5 criteria):
- **≥ 8.0**: **APPROVE** - Publish immediately
- **6.0-7.9**: **REVISE** - Minor improvements needed
- **< 6.0**: **REJECT** - Major rewrite needed

**Typical distribution**:
- Draft agent output: 6.5-7.5
- After editor agent: 7.5-8.5
- Manual refinement: 8.5-9.5

---

## AI Review Report Format

**Location**: `ai_review_report.json`

**Structure**:
```json
{
  "timestamp": "2026-01-24T21:55:00+09:00",
  "file": "content/en/tech/2026-01-24-ai-trends.md",
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
    "Good SEO integration without keyword stuffing"
  ],
  "suggestions": [
    "Consider adding one more code example in section 2",
    "Meta description could be more compelling"
  ]
}
```

---

## Usage

### Run AI Reviewer

```bash
# Review most recent post
python scripts/ai_reviewer.py

# View results
cat ai_review_report.json

# Check average score
jq '.average' ai_review_report.json
```

### Interpret Results

**APPROVE (≥ 8.0)**:
- Content ready to publish
- Minor tweaks optional
- Strong quality across all criteria

**REVISE (6.0-7.9)**:
- Identify weak criteria (< 7.0)
- Focus improvements on those areas
- Re-run reviewer after edits

**REJECT (< 6.0)**:
- Major quality issues
- Consider regenerating content
- Review Draft agent prompts

---

## Integration with Workflow

### GitHub Actions

**File**: `.github/workflows/daily-content.yml`

```yaml
- name: AI review (non-blocking)
  run: python scripts/ai_reviewer.py || true
  continue-on-error: true
```

**Behavior**:
- Runs after quality gate passes
- Low scores don't block PR creation
- Results included in PR description

### Manual Workflow

```bash
# After content generation
python scripts/generate_posts.py --count 3

# Run quality gate (blocking)
python scripts/quality_gate.py
# Must pass to continue

# Run AI reviewer (informational)
python scripts/ai_reviewer.py
# Review feedback, improve if needed

# Commit if satisfied
git add content/
git commit -m "feat: Add AI trends articles"
```

---

## Cost

**Per review**: ~$0.02 (Claude API)
**Daily cost**: $0.06 (3 reviews/day)
**Monthly cost**: ~$1.80

**Note**: AI reviewer is optional to minimize costs.

---

## Customizing Criteria

To adjust scoring weights or add criteria, edit `scripts/ai_reviewer.py`.

**Current weights** (all equal):
- Each criterion: 20% of final score
- Average: (sum of 5 scores) / 5

**To add 6th criterion**:
1. Add scoring logic in `scripts/ai_reviewer.py`
2. Update average calculation
3. Update this documentation

---

## Related

- **Quality Gate**: `quality-validation/SKILL.md` - Automated checks
- **AI Phrases**: `resources/ai-phrases.md` - Blacklist details
- **Standards**: `.claude/docs/quality-standards.md` - Overall quality criteria

---

**Version**: 1.2
**Last Updated**: 2026-01-24
**Maintained By**: Jake's Tech Insights project
