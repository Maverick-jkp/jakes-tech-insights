# Error Handling Improvements

**Date**: 2026-01-20
**Branch**: `feature/improve-error-handling`
**Status**: Completed

## Overview

This document describes improvements made to error handling in critical workflow scripts to improve reliability, debugging capability, and graceful failure handling.

## Goals

1. ✅ Improve error logging with clear, actionable messages
2. ✅ Add proper exception handling for common failure scenarios
3. ✅ Ensure workflows fail gracefully without breaking subsequent tasks
4. ✅ Mask sensitive information (API keys) in all error logs
5. ✅ Provide context for debugging (file paths, IDs, error types)

## Files Modified

### 1. [scripts/generate_posts.py](../scripts/generate_posts.py)

**Changes Made:**

#### Initialization Error Handling
- **Before**: Generic `ValueError` on missing API key
- **After**: Detailed error message with setup instructions, safe_print for logging
- **Location**: Lines 274-280

#### API Client Initialization
- **Before**: No error handling around Anthropic client creation
- **After**: Try-catch with masked error logging
- **Location**: Lines 283-294

#### Draft Generation API Calls
- **Before**: No error handling around API call
- **After**:
  - Try-catch around API call with detailed context (topic ID, keyword)
  - Validation of response content
  - Masked error messages
- **Location**: Lines 319-346

#### Draft Editing API Calls
- **Before**: No validation or error handling
- **After**:
  - Input validation (empty draft check)
  - Try-catch with context
  - Response validation
- **Location**: Lines 372-412

#### Unsplash API Error Handling
- **Before**: Generic exception catch
- **After**: Specific exception handling for:
  - `requests.exceptions.Timeout` - Request timeout
  - `requests.exceptions.HTTPError` - HTTP errors with status codes
  - `requests.exceptions.RequestException` - Network errors
  - `json.JSONDecodeError` - JSON parsing errors
  - Generic `Exception` - Unexpected errors
- **Location**: Lines 969-993, 1040-1058

#### Main Loop Error Handling
- **Before**: Single generic exception catch
- **After**:
  - Step-by-step logging (5 steps)
  - Separate error handling for metadata generation (non-critical)
  - Separate error handling for image fetch (non-critical)
  - Specific exception types:
    - `KeyError` - Missing required fields
    - `ValueError` - Invalid data
    - `IOError` - Filesystem errors
    - Generic `Exception` - Unexpected errors
  - Queue update failures don't break the process
- **Location**: Lines 1215-1292

**Benefits:**
- Clearer error messages help identify root cause quickly
- Non-critical failures (images, metadata) don't stop post generation
- All errors are logged with context for debugging
- API keys and secrets are always masked

---

### 2. [scripts/keyword_curator.py](../scripts/keyword_curator.py)

**Changes Made:**

#### Initialization Error Handling
- **Before**: Generic `ValueError` on missing API key
- **After**:
  - Detailed error messages with setup instructions
  - Try-catch around Anthropic client initialization
  - Graceful handling of missing queue file (creates empty queue)
- **Location**: Lines 130-161

#### RSS Feed Fetching
- **Before**: Generic exception catch
- **After**: Specific handling for:
  - `requests.exceptions.Timeout` - Request timeout
  - `requests.exceptions.HTTPError` - HTTP errors
  - `xml.etree.ElementTree.ParseError` - XML parsing errors
  - Generic `Exception` - Unexpected errors
- **Location**: Lines 232-244

#### Google Custom Search API
- **Before**: Generic `requests.exceptions.RequestException`
- **After**: Specific handling for:
  - `requests.exceptions.Timeout` - Request timeout
  - `requests.exceptions.HTTPError` - HTTP errors with special handling for rate limiting (429)
  - `json.JSONDecodeError` - Invalid JSON response
  - `requests.exceptions.RequestException` - Network errors
  - Generic `Exception` - Unexpected errors
- **Location**: Lines 329-346

#### Claude API Call for Keyword Generation
- **Before**: JSON parsing error only
- **After**:
  - Try-catch around API call with critical error handling
  - Response validation
  - Enhanced JSON parsing error with context
  - All errors exit with clear messages
- **Location**: Lines 445-481

#### Queue Saving
- **Before**: No error handling
- **After**:
  - Ensure parent directory exists
  - Specific handling for:
    - `IOError` - Filesystem errors
    - Generic `Exception` - Unexpected errors
- **Location**: Lines 173-187

**Benefits:**
- Clear distinction between critical and non-critical errors
- Rate limiting (429) errors are specifically identified
- Queue operations are more robust with directory creation
- All API calls have proper error handling

---

### 3. [scripts/quality_gate.py](../scripts/quality_gate.py)

**Changes Made:**

#### File Reading Error Handling
- **Before**: No error handling
- **After**: Specific handling for:
  - `FileNotFoundError` - Missing file
  - `IOError` - Cannot read file
  - Generic `Exception` - Unexpected errors
  - Returns error result instead of crashing
- **Location**: Lines 69-100

#### Markdown Parsing Error Handling
- **Before**: No error handling
- **After**: Try-catch with graceful fallback to treating entire content as body
- **Location**: Lines 103-110

#### Main Function - Loading Generated Files
- **Before**: Simple file existence check
- **After**: Specific handling for:
  - `json.JSONDecodeError` - Invalid JSON
  - `IOError` - Cannot read file
  - Clear messages distinguishing error from empty list
- **Location**: Lines 344-366

#### Report Saving Error Handling
- **Before**: No error handling
- **After**: Try-catch with IOError handling, continues on failure
- **Location**: Lines 422-437

**Benefits:**
- Quality gate never crashes due to missing/corrupted files
- Clear error messages help diagnose issues
- Report saving failures don't break the quality check process
- Empty file list is handled as valid (not an error)

---

## Error Handling Patterns

### Pattern 1: Critical vs Non-Critical Errors

**Critical Errors** (stop execution):
- Missing API keys
- API client initialization failures
- Invalid JSON responses from Claude API
- Missing required fields in data

**Non-Critical Errors** (log and continue):
- Image fetch failures (use placeholder)
- Metadata generation failures (use defaults)
- Queue update failures (log warning)
- Report saving failures (log warning)

### Pattern 2: Structured Error Logging

All error messages follow this structure:
```
❌ ERROR: <brief description>
   Context: <relevant IDs, paths>
   Error: <masked error message>
```

For warnings:
```
⚠️  WARNING: <brief description>
   Context: <relevant IDs, paths>
   Error: <masked error message>
```

### Pattern 3: Error Message Masking

All error messages are passed through `mask_secrets()` to prevent leaking:
- API keys
- Bearer tokens
- Access tokens
- Environment variables

### Pattern 4: Specific Exception Handling

Instead of catching generic `Exception`, we now catch specific exceptions first:
1. Most specific (e.g., `requests.exceptions.Timeout`)
2. Less specific (e.g., `requests.exceptions.HTTPError`)
3. Generic (e.g., `requests.exceptions.RequestException`)
4. Catch-all (e.g., `Exception`)

This provides better error messages and more appropriate handling.

## Testing Recommendations

### Test Scenarios

1. **Missing API Keys**
   - Remove `ANTHROPIC_API_KEY` from environment
   - Run `python scripts/generate_posts.py`
   - Should see clear error message with setup instructions

2. **Network Timeouts**
   - Simulate slow network
   - Run keyword curator
   - Should see timeout errors but continue with fallback

3. **Invalid JSON Responses**
   - (Difficult to test without API mocking)
   - Error should be caught and logged clearly

4. **Missing Files**
   - Remove `generated_files.json`
   - Run `python scripts/quality_gate.py`
   - Should see clear error message

5. **Corrupted Queue File**
   - Corrupt `data/topics_queue.json`
   - Run keyword curator
   - Should fall back to empty queue

## Logging Improvements

### Before
```
Error: <exception message>
Failed: <exception message>
```

### After
```
❌ ERROR: API call failed during draft generation
   Topic: 001-en-tech-ai-coding
   Keyword: AI coding assistant
   Error: Connection timeout after 30s
```

## Best Practices Applied

1. **Always mask secrets** - All error messages go through `mask_secrets()`
2. **Provide context** - Include topic ID, file path, keyword, etc.
3. **Fail gracefully** - Non-critical features degrade gracefully
4. **Specific exceptions** - Catch specific exceptions before generic ones
5. **Clear messages** - Error messages explain what went wrong and what to do
6. **Progress tracking** - Step-by-step logging for long operations
7. **Validation** - Check for empty/null responses before using them
8. **Resource cleanup** - Ensure files are closed even on error (using `with` statement)

## Impact

### Reliability
- Workflows no longer crash on transient errors (timeouts, rate limits)
- Missing images or metadata don't stop content generation
- Queue corruption is handled gracefully

### Debuggability
- Clear error messages with context
- Error types are explicit (timeout vs network vs parsing)
- API keys are always masked in logs

### Maintainability
- Consistent error handling patterns across all scripts
- Specific exception handling makes issues easier to locate
- Documentation of error scenarios

## Future Improvements

Consider adding in the future:
1. **Retry logic with exponential backoff** for transient failures
2. **Structured logging** (JSON logs) for better parsing
3. **Error rate monitoring** to detect systemic issues
4. **Dead letter queue** for failed topics to retry later
5. **Alert thresholds** (e.g., if >50% of posts fail)

## Related Files

- [scripts/utils/security.py](../scripts/utils/security.py) - Secret masking utilities
- [scripts/topic_queue.py](../scripts/topic_queue.py) - Queue management
- [.github/workflows/daily-content.yml](../.github/workflows/daily-content.yml) - CI/CD workflow

## Summary

These improvements ensure that:
- ✅ Errors are logged clearly with actionable messages
- ✅ Sensitive data is never exposed in logs
- ✅ Workflows fail gracefully and continue where possible
- ✅ Debugging is faster with context-rich error messages
- ✅ Common failure scenarios are handled appropriately

The changes maintain backward compatibility while significantly improving robustness and observability.
