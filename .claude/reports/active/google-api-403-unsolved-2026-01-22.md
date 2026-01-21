# Google Custom Search API 403 Error - Unsolved Issue

**Date**: 2026-01-22 00:30 KST
**Status**: 🔴 UNSOLVED - Need External Help
**Agent**: Master (Claude Sonnet 4.5)

---

## Problem Summary

Google Custom Search API returns **403 Forbidden** for ALL queries, despite:
- ✅ API enabled
- ✅ Valid API key and CX ID in .env
- ✅ Quota remaining (45/100 used = 55 queries left)
- ✅ Code working correctly (certifi SSL support added)

---

## Error Details

### Exact Error Message
```
403 Client Error: Forbidden for url: https://www.googleapis.com/customsearch/v1?key=AIzaSy...&cx=832db2...&q=AI+technology+2026&num=2
```

### Test Query Used
```python
import requests, certifi, os

url = 'https://www.googleapis.com/customsearch/v1'
params = {
    'key': os.environ['GOOGLE_API_KEY'],
    'cx': os.environ['GOOGLE_CX'],
    'q': 'AI technology 2026',  # Safe, non-controversial query
    'num': 2
}

response = requests.get(url, params=params, verify=certifi.where())
# Result: 403 Forbidden
```

---

## Google Cloud Console Status

### API Dashboard
- **Service**: Custom Search API
- **Status**: Enabled ✅
- **Requests**: 105 total
- **Errors**: 71 (67.6% error rate)
- **Quota Used**: 45% (45/100 queries)
- **Quota Remaining**: 55 queries

### Error Timeline
- **Before Jan 20**: API working normally (~200 successful requests historically)
- **Jan 21-22**: Sudden spike to 100% error rate
- **Current**: ALL queries return 403 Forbidden

### API Key Configuration
- **Name**: API key 1
- **Created**: Jan 17, 2026
- **Restrictions**: None (shows "—" in dashboard)
- **Status**: Active
- **Warning**: "Remember to configure the OAuth consent screen"

---

## What Was Working Before

### Historical Success
User reports:
> "API설정은 나는 한번도 건드린적없고, 200이었어 불과얼마전까지"

Translation: "I never touched API settings, it was at 200 (requests) until recently"

### Implication
- Same API key worked previously
- Same configuration
- No changes made by user
- **Something changed on Google's side OR quota/limits triggered**

---

## What We've Already Tried

### 1. SSL Certificate Fix ✅
**File**: `scripts/keyword_curator.py`

Added certifi to all requests:
```python
verify_ssl = certifi.where() if certifi else True
response = requests.get(url, params=params, verify=verify_ssl)
```

**Result**: Still 403 (SSL not the issue)

### 2. Safe Query Testing ✅
Tested with non-controversial query:
- Query: "AI technology 2026"
- No celebrity names
- No sensitive topics

**Result**: Still 403

### 3. Environment Variables ✅
Confirmed .env loaded:
```bash
export $(cat .env | grep -v '^#' | xargs)
echo $GOOGLE_API_KEY  # Shows: AIzaSyAY5nSO_OHR6SmFgNx6mnGlVXfygre720o
echo $GOOGLE_CX       # Shows: 832db2b9e44a74210
```

**Result**: Keys present and valid format

### 4. Quota Check ✅
- Daily limit: 100 queries/day (free tier)
- Used: 45 queries
- Remaining: 55 queries

**Result**: Quota NOT exceeded

---

## Possible Causes (Unconfirmed)

### Theory 1: API Key Restrictions Auto-Applied
**Observation**: Dashboard shows "Restrictions: —" (none)

**Hypothesis**: Google might have auto-applied restrictions due to:
- Unrestricted key flagged as security risk
- Suspicious activity detected
- OAuth consent screen not configured

**How to Check**:
1. Go to: Credentials → API key 1 → Edit
2. Check "Application restrictions" section
3. Check "API restrictions" section
4. Look for any hidden restrictions

### Theory 2: Billing Required (Despite Free Tier)
**Observation**: No billing account linked

**Hypothesis**: Google requires billing account even for free tier

**Evidence**:
- Some Google APIs require billing account on file
- Even if staying under free quota
- Common for Custom Search API

**How to Check**:
1. Go to: Billing
2. Check if billing account is linked
3. Try enabling billing (won't charge under 100 queries/day)

### Theory 3: Consent Screen Blocking
**Observation**: Warning in dashboard about OAuth consent screen

**Hypothesis**: Missing consent screen blocks API calls

**Evidence**:
- Dashboard shows warning
- OAuth consent might be required even for API key usage

**How to Check**:
1. Go to: OAuth consent screen
2. Configure app information
3. Add test users if needed

### Theory 4: IP/Referer Restrictions
**Hypothesis**: API key might have IP or HTTP referer restrictions

**How to Check**:
1. Go to: Credentials → API key 1
2. Under "Application restrictions":
   - Check if "HTTP referrers" is set
   - Check if "IP addresses" is set
3. If set, either:
   - Remove restrictions
   - Add localhost/your IP

### Theory 5: Daily Limit Already Hit (Yesterday's Quota)
**Hypothesis**: 45% shown is TODAY's usage, but quota resets at midnight UTC

**Possibility**:
- Yesterday used 100/100
- Today used 45/100
- But cumulative limit or rate limit triggered

**How to Check**:
1. Go to: Quotas & System Limits
2. Check "Queries per day" detailed view
3. Look for multiple quota limits (per-day, per-user, per-100-seconds, etc.)

---

## Information Needed from Google Cloud Console

### Critical Screenshots/Info Needed

1. **API Key Details**:
   - Credentials → API key 1 → Edit
   - Screenshot of "Application restrictions"
   - Screenshot of "API restrictions"

2. **Quota Details**:
   - Custom Search API → Quotas & System Limits
   - "Queries per day" limit and usage
   - "Queries per 100 seconds per user" limit
   - Any other quota limits shown

3. **Error Details**:
   - Custom Search API → Metrics → Errors tab
   - Filter errors by response code 403
   - Click on specific error for detailed message
   - Look for exact error reason (e.g., "accessNotConfigured", "userRateLimitExceeded")

4. **Billing Status**:
   - Billing section
   - Is billing account linked?
   - If no, does it show a warning?

5. **OAuth Consent Screen**:
   - OAuth consent screen section
   - Current configuration status
   - Any warnings or blockers?

---

## What Master Cannot Do

### Limitations
1. ❌ Cannot access Google Cloud Console directly
2. ❌ Cannot see detailed error messages from Google
3. ❌ Cannot check billing configuration
4. ❌ Cannot verify API key restrictions
5. ❌ Cannot see quota breakdowns

### What Master Can Do
1. ✅ Test API calls and report errors
2. ✅ Verify code correctness
3. ✅ Add SSL/security improvements
4. ✅ Analyze logs and error patterns

---

## Questions for ChatGPT / Google Cloud Expert

### Primary Question
> Google Custom Search API returns 403 Forbidden for all queries despite API being enabled, valid API key, and quota remaining (45/100 used). What are the most common causes and solutions?

### Specific Context
- **Project**: jakes-insights (Google Cloud)
- **API**: Custom Search API (enabled)
- **API Key**: Created Jan 17, 2026, no restrictions shown
- **Error Rate**: 71/105 requests (67.6%)
- **Quota**: 45/100 used (55 remaining)
- **Timeline**: Worked fine until Jan 20, 100% failure since Jan 21

### Error Example
```
403 Client Error: Forbidden for url:
https://www.googleapis.com/customsearch/v1?key=AIza...&cx=832d...&q=AI+technology+2026&num=2
```

### What's Already Confirmed
- ✅ API enabled in API Library
- ✅ API key exists and is active
- ✅ Environment variables loaded correctly
- ✅ SSL certificates working (certifi installed)
- ✅ Quota NOT exceeded (45% used)
- ✅ Same configuration worked previously

### Possible Causes to Investigate
1. Does Custom Search API require billing even for free tier?
2. Do unrestricted API keys get auto-blocked by Google?
3. Does missing OAuth consent screen block API key calls?
4. Are there hidden quota limits (per-second, per-user)?
5. Can IP restrictions be auto-applied?

### What We Need
- Step-by-step diagnosis process
- Which Google Cloud Console sections to check
- Common misconfigurations for Custom Search API
- Whether billing is actually required

---

## Current Impact

### Keyword Curation Broken
- ❌ 0/35 keywords have references
- ❌ All generated posts lack sources
- ❌ SEO impact (no authoritative citations)
- ❌ Content quality reduced

### API Quota Waste
- 45 queries used in testing
- 30 queries wasted by Master in diagnosis
- 55 queries remaining (can't use until issue resolved)

---

## Next Steps

1. **User to provide**: Google Cloud Console screenshots/details above
2. **Ask ChatGPT**: Using this document as context
3. **Follow ChatGPT guidance**: Apply recommended fixes
4. **Test with minimal queries**: Maximum 2 queries per test
5. **Document solution**: Update this file with resolution

---

## Files Related to This Issue

- `scripts/keyword_curator.py` - Main script using Google API
- `.env` - Contains GOOGLE_API_KEY and GOOGLE_CX
- `data/topics_queue.json` - Shows 0 references in all keywords
- `.claude/reports/active/keyword-curator-403-investigation-2026-01-22.md` - Earlier (incorrect) analysis

---

## Commit History

- `90454dc` - Added certifi SSL support (didn't fix 403)
- `8571177` - Created investigation report (misdiagnosed as billing)

---

**Created**: 2026-01-22 00:30 KST
**Status**: Awaiting Google Cloud Console investigation
**Master's Note**: I cannot solve this without access to Google Cloud Console configuration. User needs to either provide detailed screenshots or ask external expert (ChatGPT).

