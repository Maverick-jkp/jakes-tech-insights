# Skill Evaluations

Systematic test cases and success criteria for all skills.

---

## Purpose

Evaluation files provide:
- **Test cases** - Expected behavior for common queries
- **Success criteria** - Measurable outcomes for validation
- **Performance benchmarks** - Expected timing and resource usage
- **Edge cases** - Boundary conditions and error scenarios
- **Regression tests** - Tests for previously fixed issues

---

## Structure

Each evaluation file (`{skill-name}.json`) contains:

```json
{
  "skill": "skill-name",
  "version": "1.2",
  "test_cases": [
    {
      "id": "skill-001",
      "name": "Test name",
      "query": "User query",
      "expected_behavior": ["step1", "step2"],
      "success_criteria": {
        "metric": "expected_value"
      }
    }
  ],
  "performance_benchmarks": {
    "metric": "expected_value"
  },
  "edge_cases": [
    {
      "scenario": "description",
      "expected": "expected_behavior"
    }
  ],
  "regression_tests": [
    {
      "issue": "problem_description",
      "fix": "solution_applied",
      "test": "verification_method"
    }
  ]
}
```

---

## Files

- **content-generation.json** - Content generation pipeline tests
- **quality-validation.json** - Quality gate and AI reviewer tests
- **hugo-operations.json** - Hugo build and server tests
- **keyword-curation.json** - Topic queue management tests

---

## Usage

### Manual Testing

```bash
# Run a specific test case
# Example: content-generation test cg-001
python scripts/generate_posts.py --count 1

# Verify success criteria
cat quality_report.json | jq '.passed'
```

### Automated Testing

```bash
# Run all skill tests
pytest tests/test_skills.py

# Run specific skill
pytest tests/test_skills.py::test_content_generation
```

### CI/CD Integration

```yaml
# .github/workflows/skill-tests.yml
- name: Run skill evaluations
  run: pytest tests/test_skills.py --json-report
```

---

## Updating Evaluations

**When to update**:
- Adding new functionality
- Fixing bugs (add regression test)
- Changing success criteria
- Performance improvements

**How to update**:
1. Edit `{skill-name}.json`
2. Add/modify test cases
3. Update version number in evaluation file
4. Update skill CHANGELOG.md
5. Run tests to verify

---

## Test Case IDs

**Format**: `{skill-abbreviation}-{number}`

**Examples**:
- `cg-001` - content-generation test 001
- `qv-002` - quality-validation test 002
- `ho-003` - hugo-operations test 003
- `kc-004` - keyword-curation test 004

---

## Success Criteria Format

**Boolean checks**:
```json
"success_criteria": {
  "file_created": true,
  "no_errors": true
}
```

**Value checks**:
```json
"success_criteria": {
  "word_count": ">=800",
  "exit_code": 0,
  "files_created": 3
}
```

**Enum checks**:
```json
"success_criteria": {
  "status": "one of [PASS, FAIL, WARN]",
  "recommendation": "APPROVE"
}
```

---

## Performance Benchmarks

Track expected performance for regression detection:

```json
"performance_benchmarks": {
  "execution_time": "30-60 seconds",
  "api_calls": 2,
  "cost": "$0.09",
  "token_usage": "~8000 tokens"
}
```

**Alert if**:
- Execution time exceeds 2x expected
- API calls increase without code changes
- Cost increases unexpectedly

---

## Edge Cases

Document boundary conditions and error handling:

```json
"edge_cases": [
  {
    "scenario": "Empty queue",
    "expected": "Error: No pending topics"
  },
  {
    "scenario": "Missing API key",
    "expected": "Error: ANTHROPIC_API_KEY not set"
  }
]
```

---

## Regression Tests

Track fixed issues to prevent reoccurrence:

```json
"regression_tests": [
  {
    "issue": "Word count too low",
    "fix": "Increased max_tokens to 12000",
    "test": "Verify all posts >=800 words"
  }
]
```

**Add new regression test when**:
- Bug fixed in production
- User-reported issue resolved
- Quality issue corrected

---

## Related

- **Skills**: `.claude/skills/` - Skill documentation
- **Tests**: `tests/test_skills.py` - Pytest test suite
- **CI/CD**: `.github/workflows/skill-tests.yml` - Automated testing

---

**Version**: 1.0
**Last Updated**: 2026-01-24
**Maintained By**: Jake's Tech Insights project
