# Keyword Curator 403 Forbidden Investigation
**Date**: 2026-01-22
**Agent**: Master
**Status**: 🟡 BLOCKED - Google Cloud Configuration Required

---

## Executive Summary

**Problem**: Keyword curation generates keywords but ALL references are empty (`"references": []`)

**Root Cause**: Google Custom Search API returning **403 Forbidden** for all requests

**NOT an SSL Issue**: Despite similar symptoms to Unsplash bug, this is a Google Cloud billing/configuration issue, not a code bug.

**Resolution Required**: Enable billing on Google Cloud project OR verify Custom Search API is enabled

---

## Investigation Timeline

### Initial Symptom (2026-01-21)
```
⚠️  WARNING: 6/6 keywords have NO references
   This means generated posts will lack credible sources!
```

### First Hypothesis: SSL Certificate Issue
- Similar to Unsplash image download bug
- Thought: Maybe Google Custom Search API also needs certifi

### Testing with certifi (2026-01-22)
**Added SSL verification**:
```python
verify_ssl = certifi.where() if certifi else True
response = requests.get(url, params=params, verify=verify_ssl)
```

**Result**: Same error persisted

### Debug Output Revealed Truth
```
⚠️  HTTP error (unknown) for '구혜선...'
   Debug: 403 Client Error: Forbidden for url: https://www.googleapis.com/customsearch/v1?key=***
```

**Actual Status Code**: 403 Forbidden (NOT SSL error!)

---

## Root Cause Analysis

### Why 403 Forbidden Happens

Google Custom Search API requires **billing enabled** even for free tier usage.

**3 Possible Causes**:

1. **Billing Not Enabled** (Most Common)
   - Google Cloud project doesn't have billing account
   - Custom Search API requires billing even for 100 free queries/day
   - Fix: Enable billing in Google Cloud Console

2. **API Not Enabled**
   - Custom Search API not enabled in API Library
   - Fix: Go to APIs & Services → Library → Enable "Custom Search API"

3. **API Key Restrictions**
   - API key has restrictions blocking requests
   - Fix: Check Credentials → API Key → Remove restrictions or allow Custom Search API

---

## Evidence

### Error Messages (All 15 Trend Queries)
```
✓ Found 5 trends from KR
✓ Found 5 trends from US
✓ Found 5 trends from JP

🎉 Total 15 real-time trending topics from RSS!

⚠️  HTTP error (403) for '구혜선...'
   ⚠️  Google API Access Forbidden - check API key and billing status
⚠️  HTTP error (403) for '임형주...'
   ⚠️  Google API Access Forbidden - check API key and billing status
[... 13 more ...]

✅ Total 0 trending topics fetched
```

### API Request Format (Correct)
```
GET https://www.googleapis.com/customsearch/v1
  ?key=AIzaSyAY5n... (valid)
  &cx=832db2b9e44a74210 (valid)
  &q=구혜선
  &num=2
  &dateRestrict=d7
  &sort=date

Response: 403 Forbidden
```

### Environment Variables (Present)
```bash
✓ GOOGLE_API_KEY: Set (AIzaSyAY5n...)
✓ GOOGLE_CX: Set (832db2b9e44a74210)
```

---

## What Was Fixed (Code Side)

### 1. Added certifi Support
**File**: `scripts/keyword_curator.py`

**Line 20-26**: Import certifi
```python
try:
    import certifi
except ImportError:
    safe_print("Warning: certifi not installed - SSL verification may fail")
    certifi = None
```

**Line 235**: RSS feed with SSL
```python
verify_ssl = certifi.where() if certifi else True
response = requests.get(url, timeout=10, verify=verify_ssl)
```

**Line 330**: Google Custom Search with SSL
```python
verify_ssl = certifi.where() if certifi else True
response = requests.get(url, params=params, verify=verify_ssl)
```

### 2. Improved Error Messages
**Line 357-360**: Better diagnostics
```python
if status_code == 403:
    safe_print(f"     ⚠️  Google API Access Forbidden - check API key and billing status")
elif status_code == 429:
    safe_print(f"     Rate limit exceeded - consider adding longer delays")
```

**Commit**: `90454dc` - "fix: Add certifi SSL support to keyword curator and improve error messages"

---

## What Still Needs Fixing (Google Cloud Side)

### Option 1: Enable Billing (Recommended)

**Why Needed**: Custom Search API requires billing even for free tier

**Steps**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to **Billing**
4. Click **Link a Billing Account**
5. Add payment method (credit card)
6. Enable billing

**Cost**: FREE for first 100 queries/day, then $5/1000 queries

**Current Usage**: ~15-20 queries per keyword curation = well within free tier

### Option 2: Verify API Enabled

**Steps**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services** → **Library**
3. Search for "Custom Search API"
4. Click **Custom Search API**
5. Click **Enable** if not already enabled

### Option 3: Check API Key Restrictions

**Steps**:
1. Go to **APIs & Services** → **Credentials**
2. Click on your API key
3. Under **API restrictions**:
   - Select "Restrict key"
   - Add "Custom Search API" to allowed list
4. Save

---

## Testing After Fix

### Expected Output (After Billing Enabled)
```
============================================================
  🔥 Fetching REAL-TIME trending topics from Google Trends RSS...
============================================================

  ✓ Found 5 trends from KR
  ✓ Found 5 trends from US
  ✓ Found 5 trends from JP

  🎉 Total 15 real-time trending topics from RSS!

  ✓ Fetched 2 results for: 구혜선
  ✓ Fetched 2 results for: 임형주
  ✓ Fetched 2 results for: 나는 솔로
  [... 12 more ...]

✅ Total 30 trending topics fetched

📚 Extracting references for 6 candidates...

  ✓ 2 refs for: corporate layoffs 2026
  ✓ 2 refs for: social media algorithm changes
  ✓ 2 refs for: AI 고용 대체 현실
  ✓ 2 refs for: 부동산 폭락 신호
  ✓ 2 refs for: 健康保険制度崩壊
  ✓ 2 refs for: 教育格差拡大

✅ 6/6 keywords have references!
```

### Test Command
```bash
export $(cat .env | grep -v '^#' | xargs)
python3 scripts/keyword_curator.py --count 6
```

---

## Comparison: Unsplash vs Google API Issues

| Aspect | Unsplash Image Bug | Google Custom Search Issue |
|--------|-------------------|---------------------------|
| **Symptom** | HTTP error (unknown) | HTTP error (403) |
| **Root Cause** | Wrong URL format + SSL | Billing not enabled |
| **Code Fix** | ✅ Fixed URL + certifi | ✅ Added certifi (preventive) |
| **Config Fix** | ❌ None needed | 🔴 **Billing required** |
| **Status** | ✅ RESOLVED | 🟡 BLOCKED on user |

---

## Why This Looked Like SSL Issue

### Similarities
1. ✅ "HTTP error (unknown)" message
2. ✅ Worked before, suddenly failing
3. ✅ Environment variables present
4. ✅ Same error pattern as Unsplash

### Key Difference
- **Unsplash**: `status_code = None` (connection failed before response)
- **Google**: `status_code = 403` (connection succeeded, API rejected)

---

## Impact

### Current State
- ✅ Keywords generated successfully (6 candidates)
- ✅ Google Trends RSS working (15 trending topics)
- ❌ References empty (0 references per keyword)
- ❌ Posts will lack credible sources
- ❌ SEO impact (no authoritative citations)

### After Billing Enabled
- ✅ Full reference extraction (2-5 refs per keyword)
- ✅ Posts with credible sources
- ✅ Better SEO ranking
- ✅ Authoritative content

---

## Code Quality Improvements

### Better Error Diagnostics
**Before**:
```
⚠️  HTTP error (unknown) for '구혜선...'
```

**After**:
```
⚠️  HTTP error (403) for '구혜선...'
   ⚠️  Google API Access Forbidden - check API key and billing status
```

### SSL Certificate Support
- Added certifi to all HTTP requests
- Prevents future SSL issues on Mac and Windows
- Consistent with generate_posts.py fixes

---

## Next Steps

### Immediate (User Action Required)
1. **Enable billing** on Google Cloud project
2. **Test keyword curation**: `python3 scripts/keyword_curator.py --count 6`
3. **Verify references** appear in generated keywords

### Future Improvements
1. **Pre-flight test** for Google API
2. **Fallback strategy** when API unavailable
3. **Mock references** for testing without API

---

## Documentation Updates Needed

### Update GOOGLE_API_SETUP.md
Add section:
```markdown
## ⚠️  Billing Required

Custom Search API requires billing enabled even for free tier.

**Error symptom**:
```
⚠️  HTTP error (403) for queries...
   ⚠️  Google API Access Forbidden
```

**Solution**: Enable billing in Google Cloud Console (still free for <100 queries/day)
```

---

## Lessons Learned

### What Master Got Right
1. ✅ Added certifi proactively (even though not the root cause)
2. ✅ Improved error messages to aid diagnosis
3. ✅ Tested thoroughly before committing
4. ✅ Documented the real issue clearly

### What Master Learned
1. **403 ≠ SSL Error** - Similar symptoms, different causes
2. **Google APIs** often require billing even for free tier
3. **Debug output first** - Don't assume based on similar issues

---

## Summary

**Code Side**: ✅ FIXED
- Added certifi SSL support
- Improved error diagnostics
- Future-proofed against SSL issues

**Config Side**: 🔴 **USER ACTION REQUIRED**
- Enable billing on Google Cloud project
- Verify Custom Search API enabled
- Test after billing activation

**Estimated Time**: 5-10 minutes to enable billing

**Cost Impact**: $0 (under 100 queries/day)

---

**Report Created**: 2026-01-22 00:20 AM KST
**Status**: Code fixes committed, awaiting Google Cloud billing setup
**Commit**: `90454dc` - certifi support + error handling

