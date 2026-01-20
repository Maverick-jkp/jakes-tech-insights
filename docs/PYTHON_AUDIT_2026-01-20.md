# Python Scripts Security Audit Report
**Date**: 2026-01-20
**Auditor**: CTO Agent
**Trigger**: Post-incident audit following `safe_print()` bug in quality_gate.py

---

## Executive Summary

**Audit Scope**: All Python scripts in `scripts/` directory (19 files total)
**Critical Issues Found**: 2
**High Priority Issues**: 12
**Medium Priority Issues**: 8
**Total Issues**: 22

**Recommendation**: 🔴 **IMMEDIATE ACTION REQUIRED**
- Fix critical bugs before next deployment
- Implement security wrapper enforcement across all scripts

---

## Critical Issues (Fix Immediately)

### 🔴 CRITICAL-001: Missing Required Parameter in ai_reviewer.py

**File**: `scripts/ai_reviewer.py`
**Line**: 335
**Severity**: Critical

**Issue**:
```python
safe_print()  # ❌ Missing required 'message' parameter
```

**Impact**:
- Causes immediate script failure: `TypeError: safe_print() missing 1 required positional argument: 'message'`
- Identical to today's incident in quality_gate.py
- Breaks AI review functionality

**Root Cause**: Same pattern as quality_gate.py - attempting to print empty line without message parameter

**Fix**:
```python
safe_print("")  # ✅ Provide empty string as message
```

**Status**: ⏳ Pending fix

---

### 🔴 CRITICAL-002: API Key Exposure via Direct print() Statements

**Files Affected**:
- `scripts/fetch_images_for_posts.py` (17 occurrences)
- `scripts/cleanup_expired.py` (7 occurrences)
- `scripts/chatgpt-review.py` (multiple occurrences)
- `scripts/convert_to_page_bundles.py`
- `scripts/copy_images_to_bundles.py`
- `scripts/fix_duplicate_images.py`
- `scripts/fix_placeholder_image.py`
- `scripts/measure_image_performance.py`
- `scripts/redownload_optimized_images.py`
- `scripts/replace_image_via_api.py`
- `scripts/test_queue.py`
- `scripts/update_image_paths.py`
- `scripts/upload_workflows.py`

**Severity**: Critical (API Key Exposure Risk)

**Issue**: Multiple scripts use `print()` directly instead of `safe_print()`, bypassing the security wrapper that masks API keys and secrets.

**Examples**:
```python
# ❌ INSECURE - API keys in error messages will be exposed
print(f"❌ Error: {e}")  # scripts/fetch_images_for_posts.py:114

# ✅ SECURE - API keys automatically masked
safe_print(f"❌ Error: {str(e)}")
```

**Impact**:
- If errors contain API keys, they will be logged in plaintext
- Violates security policy established in `utils/security.py`
- Risk of accidental API key exposure in CI/CD logs

**Total Count**: ~100+ direct `print()` statements across 13 files

**Recommendation**:
1. Replace all `print()` with `safe_print()` in all scripts
2. Add pre-commit hook to prevent `print()` in production code
3. Update `.gitattributes` to enforce security wrapper usage

**Status**: ⏳ Pending systematic fix

---

## High Priority Issues

### ⚠️ HIGH-001: Inconsistent Error Handling in mask_secrets()

**File**: `scripts/utils/security.py`
**Lines**: 30-32
**Severity**: High

**Issue**:
```python
for secret in get_sensitive_patterns():
    if secret and len(secret) > 0:  # Redundant check
        masked = masked.replace(secret, "***MASKED***")
```

**Problem**:
- `if secret and len(secret) > 0` is redundant (empty string is falsy)
- Should also check if secret is None before calling len()
- Potential `TypeError` if environment variable returns None

**Fix**:
```python
for secret in get_sensitive_patterns():
    if secret:  # Simplified - empty strings and None are both falsy
        masked = masked.replace(secret, "***MASKED***")
```

---

### ⚠️ HIGH-002: No Input Validation on file_path Parameter

**Files**:
- `scripts/quality_gate.py:65`
- `scripts/ai_reviewer.py:178`

**Issue**: Functions accept file paths without validation, vulnerable to path traversal attacks

**Recommendation**: Add validation using `scripts/utils/validation.py` patterns

---

### ⚠️ HIGH-003: Hardcoded API Endpoints

**File**: `scripts/keyword_curator.py:867`
```python
url = "https://api.unsplash.com/search/photos"
```

**File**: `scripts/generate_posts.py:877`
```python
url = "https://api.unsplash.com/search/photos"
```

**Issue**: Hardcoded URLs make testing and mocking difficult

**Recommendation**: Move to configuration file or environment variables

---

### ⚠️ HIGH-004: Unsafe JSON Parsing Without Schema Validation

**File**: `scripts/keyword_curator.py:424`
```python
try:
    candidates = json.loads(content)
except json.JSONDecodeError as e:
    # No schema validation after parsing
```

**Impact**: Could accept malformed data that causes downstream issues

**Recommendation**: Use `validate_topic_data()` after parsing JSON

---

### ⚠️ HIGH-005: Missing Timeout on Network Requests

**Files**: Multiple
**Examples**:
- `scripts/keyword_curator.py:283` - No timeout on requests.get()
- `scripts/generate_posts.py:879` - Has timeout (good!)

**Issue**: Some network requests missing timeout parameter, could hang indefinitely

**Fix**: Add `timeout=10` to all requests.get() calls

---

### ⚠️ HIGH-006: Broad Exception Catching

**File**: `scripts/keyword_curator.py:423-428`
```python
except Exception as e:  # Too broad!
    safe_print(f"⚠️  Image fetch failed: {str(e)}")
    return None
```

**Issue**: Catches all exceptions including KeyboardInterrupt, SystemExit

**Recommendation**: Catch specific exceptions (requests.RequestException, ValueError, etc.)

---

### ⚠️ HIGH-007: Insecure File Path Construction

**File**: `scripts/generate_posts.py:993-996`
```python
slug = keyword.lower()
slug = ''.join(c if c.isalnum() or c.isspace() else '' for c in slug)
slug = slug.replace(' ', '-')[:50]
```

**Issue**: Limited sanitization, no validation against path traversal

**Recommendation**: Use `validate_keyword()` from validation.py before file operations

---

### ⚠️ HIGH-008: No Rate Limiting on API Calls

**File**: `scripts/keyword_curator.py:268-306`

**Issue**: Google Custom Search API calls in loop with only 1 second delay

**Problem**:
- Could exhaust API quota quickly
- No exponential backoff on failures

**Recommendation**: Implement proper rate limiting and retry logic with exponential backoff

---

### ⚠️ HIGH-009: SQL Injection Risk (Future)

**Files**: All scripts using topic queue

**Current Status**: ✅ Safe (using JSON, not SQL)

**Risk**: If migrating to SQL database in future, current string interpolation patterns are unsafe

**Recommendation**: Document safe query patterns for future migrations

---

### ⚠️ HIGH-010: Missing Input Validation on User Input

**File**: `scripts/keyword_curator.py:488-517`
```python
user_input = input("선택: ").strip()
```

**Issue**: User input directly parsed without comprehensive validation

**Recommendation**: Add input sanitization and bounds checking

---

### ⚠️ HIGH-011: Insecure Temporary File Handling

**File**: `scripts/generate_posts.py:889-916`

**Issue**: `used_images.json` file read/write without file locking

**Risk**: Race condition if multiple scripts run simultaneously

**Recommendation**: Use file locking (fcntl on Unix, msvcrt on Windows) or atomic writes

---

### ⚠️ HIGH-012: No Secrets Detection in Generated Content

**File**: `scripts/generate_posts.py:1086-1090`

**Issue**: Generated content is not scanned for accidentally included API keys before saving

**Recommendation**: Run `mask_secrets()` on generated content as final check

---

## Medium Priority Issues

### ℹ️ MEDIUM-001: Inconsistent Error Messages

Multiple files have inconsistent error message formats (some with emojis, some without)

**Recommendation**: Establish standard error message format

---

### ℹ️ MEDIUM-002: Magic Numbers in Code

**Examples**:
- `scripts/quality_gate.py:239` - Hardcoded length thresholds (120-160)
- `scripts/generate_posts.py:966` - Image size `w=1200&q=85`

**Recommendation**: Move to configuration constants

---

### ℹ️ MEDIUM-003: Missing Type Hints

Many functions lack type hints, making static analysis difficult

**Recommendation**: Add type hints to all function signatures

---

### ℹ️ MEDIUM-004: No Unit Tests

**Observation**: No test files found in `scripts/` directory

**Recommendation**: Add unit tests for critical functions (especially security.py)

---

### ℹ️ MEDIUM-005: Duplicate Code

Similar image fetching logic appears in:
- `scripts/generate_posts.py`
- `scripts/fetch_images_for_posts.py`
- `scripts/replace_placeholder_images.py`

**Recommendation**: Extract to shared utility function

---

### ℹ️ MEDIUM-006: Inefficient String Concatenation

**File**: `scripts/keyword_curator.py:314-317`
```python
trends_summary = "\n\n".join([...])  # Good!
```

Some files use += in loops (less efficient)

**Recommendation**: Use join() consistently

---

### ℹ️ MEDIUM-007: Missing Docstrings

Several functions lack comprehensive docstrings

**Recommendation**: Add docstrings following Google style guide

---

### ℹ️ MEDIUM-008: Hardcoded Date Formats

Multiple date format strings (`"%Y-%m-%d"`, `"%Y-%m-%dT%H:%M:%S"`) scattered across files

**Recommendation**: Define constants for date formats

---

## Security Best Practices Analysis

### ✅ Things Done Well

1. **Secrets Masking**: `utils/security.py` provides robust API key masking
2. **Input Validation**: `utils/validation.py` has comprehensive validation functions
3. **Consistent API Key Loading**: Using `os.environ.get()` with fallbacks
4. **Timezone Awareness**: Using `timezone.utc` in topic_queue.py
5. **Parameter Sanitization**: Keyword cleaning before file path generation

### ❌ Areas for Improvement

1. **Inconsistent Security Wrapper Usage**: Many scripts use `print()` instead of `safe_print()`
2. **No Pre-commit Hooks**: Nothing prevents insecure code from being committed
3. **Missing Security Documentation**: No `SECURITY.md` file
4. **No Automated Security Scanning**: Consider adding bandit or safety checks to CI/CD

---

## Detailed File Analysis

### scripts/quality_gate.py
- **Status**: ✅ Fixed (safe_print bug resolved in previous commit)
- **Lines**: 396
- **Issues**: 0 critical, 2 medium (magic numbers, missing tests)

### scripts/generate_posts.py
- **Status**: ⚠️ Needs review
- **Lines**: 1188
- **Issues**: 0 critical, 5 high (API key exposure via error messages, no rate limiting)
- **safe_print usage**: ✅ Correct (59 occurrences, all with parameters)

### scripts/keyword_curator.py
- **Status**: ⚠️ Needs review
- **Lines**: 645
- **Issues**: 0 critical, 6 high
- **safe_print usage**: ✅ Correct (40 occurrences)

### scripts/topic_queue.py
- **Status**: ✅ Good
- **Lines**: 317
- **Issues**: 0 critical, 1 high (broad exception catching)
- **safe_print usage**: N/A (no user-facing output)

### scripts/cleanup_expired.py
- **Status**: 🔴 High Risk
- **Lines**: 119
- **Issues**: 1 critical (uses print() instead of safe_print)
- **print() usage**: ❌ 7 occurrences (should be safe_print)

### scripts/ai_reviewer.py
- **Status**: 🔴 Critical
- **Lines**: 372
- **Issues**: 1 critical (safe_print() missing parameter at line 335)
- **safe_print usage**: 42 occurrences, 1 BROKEN

### scripts/fetch_images_for_posts.py
- **Status**: 🔴 High Risk
- **Lines**: ~300
- **Issues**: 1 critical (uses print() extensively)
- **print() usage**: ❌ 17 occurrences

### scripts/utils/security.py
- **Status**: ⚠️ Needs improvement
- **Lines**: 51
- **Issues**: 0 critical, 1 high (redundant check)
- **Function**: Defines safe_print() correctly

### scripts/utils/validation.py
- **Status**: ✅ Excellent
- **Lines**: 180
- **Issues**: 0
- **Best Practice**: Comprehensive input validation

### scripts/utils/validate_queue.py
- **Status**: ✅ Good
- **Lines**: 47
- **Issues**: 0

### Other Scripts
All other scripts (chatgpt-review.py, convert_to_page_bundles.py, etc.) have similar issues with direct `print()` usage.

---

## Recommended Actions

### Immediate (Today)

1. ✅ **Fix ai_reviewer.py line 335**
   ```python
   # Change: safe_print()
   # To: safe_print("")
   ```

2. ✅ **Create tracking issue for print() → safe_print() migration**

### This Week

3. **Replace all print() with safe_print()** in production scripts
   - Priority order: fetch_images_for_posts.py, cleanup_expired.py, chatgpt-review.py
   - Use find/replace with manual review

4. **Add pre-commit hook** to prevent direct print() usage
   ```bash
   # .git/hooks/pre-commit
   if git diff --cached | grep -E "^\+.*print\("; then
     echo "Error: Direct print() detected. Use safe_print() instead."
     exit 1
   fi
   ```

5. **Add security section to README.md**

### This Month

6. **Implement automated security scanning**
   - Add `bandit` to CI/CD: `pip install bandit && bandit -r scripts/`
   - Add `safety` for dependency scanning: `safety check`

7. **Add unit tests for security.py**
   - Test mask_secrets() with various API key formats
   - Test safe_print() with different input types

8. **Create SECURITY.md**
   - Document security practices
   - Provide vulnerability reporting process

9. **Refactor duplicate code**
   - Extract image fetching to shared utility
   - Create shared error handling utility

### Future Considerations

10. **Consider migrating to logging module** instead of print-based approach
11. **Implement structured logging** (JSON logs for better parsing)
12. **Add API request monitoring** (track rate limits, failures)

---

## Appendix A: Pattern Search Results

### safe_print() with no arguments
```
scripts/ai_reviewer.py:335:            safe_print()  # ❌ CRITICAL BUG
```

### Direct print() statements (sample)
```
scripts/fetch_images_for_posts.py:22:    print("❌ Error: UNSPLASH_ACCESS_KEY not set")
scripts/cleanup_expired.py:84:    print(f"\n{'='*60}")
scripts/chatgpt-review.py:45:    print(json.dumps(review, indent=2))
```

(Full list: 100+ occurrences across 13 files)

---

## Appendix B: Testing Recommendations

### Unit Tests Needed

1. **security.py**
   - `test_mask_secrets_with_anthropic_key()`
   - `test_mask_secrets_with_unsplash_key()`
   - `test_mask_secrets_with_url_tokens()`
   - `test_safe_print_masks_secrets()`

2. **validation.py**
   - `test_validate_keyword_blocks_path_traversal()`
   - `test_validate_category_rejects_invalid()`
   - `test_validate_topic_data_complete()`

3. **topic_queue.py**
   - `test_reserve_topics_state_transition()`
   - `test_mark_failed_increments_retry_count()`

### Integration Tests Needed

1. **End-to-end content generation** with API key in error
2. **Queue operations** with concurrent access
3. **Image fetching** with rate limiting

---

## Appendix C: Code Quality Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total Python Files | 19 | - | - |
| Total Lines of Code | ~5000 | - | - |
| Critical Issues | 2 | 0 | 🔴 |
| High Priority Issues | 12 | <5 | ⚠️ |
| Files Using safe_print() | 6/19 (32%) | 100% | 🔴 |
| Files with Type Hints | 3/19 (16%) | >80% | 🔴 |
| Files with Unit Tests | 0/19 (0%) | >60% | 🔴 |
| Functions with Docstrings | ~40% | >90% | ⚠️ |

---

## Conclusion

This audit revealed **2 critical security issues** and **12 high-priority issues** across the Python codebase. The most urgent issue is the `safe_print()` bug in ai_reviewer.py (line 335), which will cause immediate script failure - identical to today's incident.

The second critical issue is widespread use of direct `print()` statements instead of the security wrapper `safe_print()`, creating API key exposure risk in error logs.

**Next Steps**:
1. Fix ai_reviewer.py immediately (1 line change)
2. Create tracking issue for print() → safe_print() migration
3. Implement pre-commit hook to prevent future violations
4. Schedule systematic code review for security improvements

**Estimated Remediation Time**:
- Critical fixes: 1 hour
- High priority fixes: 2-3 days
- Medium priority fixes: 1 week
- Full remediation: 2-3 weeks

---

**Audit Completed**: 2026-01-20
**Report Generated By**: CTO Agent
**Next Review**: After critical fixes are deployed
