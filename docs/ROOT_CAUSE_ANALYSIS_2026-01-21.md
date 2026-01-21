# Root Cause Analysis: Missing References & Placeholder Images

**Date:** 2026-01-21
**Severity:** CRITICAL
**Impact:** Every generated post lacks references and uses placeholder images

---

## 🔴 Problem Summary

User reported that **EVERY DAY** the same problems occur:
1. Posts generated WITHOUT references (0 references per post)
2. Posts generated WITHOUT Unsplash images (using placeholder images)
3. Issue persists despite previous workflow fixes

**User's explicit requirement:**
> "제발 root cause면밀하게 확실하게 잡아서 다시는 이태스크 안하게끔하자"
> (Translation: "Please identify root cause thoroughly and fix it so we NEVER have to do this task again")

---

## 🔍 Investigation Process

### Step 1: Verified the Problem

Checked today's generated posts:
- `/content/ko/tech/2026-01-21-ai-대체-일자리.md` ❌ No references, placeholder image
- `/content/en/tech/2026-01-21-job-displacement-ai-2025.md` ❌ No references, placeholder image
- `/content/ja/tech/2026-01-21-ai失業リスク2025.md` ❌ No references, placeholder image

### Step 2: Checked Topic Queue

Examined `data/topics_queue.json` for today's topics:
```json
{
  "id": "081-ko-tech-AI-대체-일자리",
  "keyword": "AI 대체 일자리",
  "references": [],  // ❌ EMPTY!
  ...
}
```

**Finding:** ALL keywords in queue have `"references": []` (empty array)

### Step 3: Traced Reference Generation Logic

Analyzed `scripts/keyword_curator.py`:

1. **Line 261-303:** `fetch_trending_topics()` method
   - Fetches trending topics from Google Trends RSS
   - **If Google Custom Search API credentials missing:** Sets `self.search_results = []` (empty)
   - Returns trending topics but NO search result data

2. **Line 398-436:** `extract_references()` method
   - Attempts to match keywords with search results
   - **If `self.search_results` is empty:** Returns `[]` (no references)

3. **Line 501-512:** References extraction in `generate_candidates()`
   - Loops through candidates and calls `extract_references()`
   - **If no search results available:** ALL references are empty

### Step 4: Checked Environment Variables

```bash
GOOGLE_API_KEY: NOT SET
GOOGLE_CX: NOT SET
UNSPLASH_ACCESS_KEY: NOT SET
```

---

## 🎯 ROOT CAUSES IDENTIFIED

### Root Cause #1: Missing Google Custom Search API Credentials

**What's broken:**
- `GOOGLE_API_KEY` and `GOOGLE_CX` are NOT configured in GitHub Secrets
- Without these, `keyword_curator.py` cannot fetch search results for references
- Code falls back to RSS-only mode, which provides trending topics but NO references

**Evidence:**
```python
# keyword_curator.py line 299-302
if not self.google_api_key or not self.google_cx:
    safe_print("  ⚠️  Google Custom Search not configured")
    self.search_results = []  # ❌ NO SEARCH RESULTS
    return "\n\n".join([f"Trending: {q}" for q in search_queries[:30]])
```

**Impact:**
- Every keyword gets `"references": []` in the queue
- Generated posts have no "## References" section
- Reduced SEO value, credibility, and user trust

---

### Root Cause #2: Missing Unsplash API Key

**What's broken:**
- `UNSPLASH_ACCESS_KEY` is NOT configured in GitHub Secrets
- Without this, `generate_posts.py` cannot download real images
- Code falls back to placeholder images

**Evidence:**
```python
# generate_posts.py line 1122-1125
if not image_path:
    # Use category-based placeholder
    image_path = f"/images/placeholder-{category}.jpg"  # ❌ PLACEHOLDER
```

**Impact:**
- Every post uses placeholder images like `/images/placeholder-tech.jpg`
- Poor user experience, reduced engagement
- User explicitly said "NO PLACEHOLDERS"

---

### Root Cause #3: No Validation / Silent Failures

**What's broken:**
- Workflows don't FAIL when references are missing
- Workflows don't FAIL when placeholder images are used
- Content gets published despite quality issues

**Why this matters:**
- User keeps discovering the problem AFTER posts are published
- No early warning system to prevent bad content
- Waste of time fixing manually every day

---

## ✅ SOLUTIONS IMPLEMENTED

### Solution 1: Enhanced Warnings in keyword_curator.py

**Changes:**
- Added CRITICAL WARNING when Google API not configured
- Shows clear message about missing references
- Validates after extraction and reports statistics

**Code added:**
```python
if not self.google_api_key or not self.google_cx:
    safe_print("  🚨 CRITICAL WARNING: Google Custom Search not configured")
    safe_print("  📌 References will NOT be generated for keywords!")
```

### Solution 2: Pre-flight Checks in generate_posts.py

**Changes:**
- Validates environment variables BEFORE generation starts
- Shows status of ANTHROPIC_API_KEY and UNSPLASH_ACCESS_KEY
- Warns if Unsplash key missing (placeholders will be used)

**Code added:**
```python
safe_print(f"  🔍 Pre-flight Environment Checks")
if unsplash_key:
    safe_print("  ✓ UNSPLASH_ACCESS_KEY: Configured")
else:
    safe_print("  ⚠️  UNSPLASH_ACCESS_KEY: NOT FOUND")
    safe_print("     Posts will use placeholder images!")
```

### Solution 3: Post-Generation Validation in generate_posts.py

**Changes:**
- Scans all generated posts for quality issues
- Counts posts without references
- Counts posts with placeholder images
- Shows warnings with root cause and fix instructions

**Code added:**
```python
if posts_without_references > 0:
    safe_print(f"🚨 WARNING: {posts_without_references} posts have NO references!")
    safe_print(f"   FIX: Ensure Google Custom Search API is configured")
```

### Solution 4: Quality Gate Validation Script

**New file:** `scripts/validate_content_quality.py`

**Purpose:**
- Runs BEFORE committing generated content
- Validates references exist in posts
- Validates real images (not placeholders)
- **FAILS the workflow** if quality standards not met

**Integration:**
- Added to `.github/workflows/daily-content.yml`
- Runs after quality_gate.py
- Prevents publishing bad content

### Solution 5: Comprehensive Setup Documentation

**New file:** `docs/API_SETUP_GUIDE.md`

**Contents:**
- Step-by-step guide to configure Google Custom Search API
- Step-by-step guide to configure Unsplash API
- Testing instructions for local development
- Troubleshooting common issues
- Success criteria checklist

---

## 🧪 TESTING REQUIRED

### Test 1: Configure Google Custom Search API

**Action:**
1. Follow `docs/API_SETUP_GUIDE.md` to get API credentials
2. Add `GOOGLE_API_KEY` and `GOOGLE_CX` to GitHub Secrets

**Expected Result:**
- Keyword curation should fetch search results
- Keywords should have 1-2 references each
- No warnings about missing references

**Validation:**
```bash
# Check topics_queue.json
grep -A 5 "references" data/topics_queue.json
# Should show: "references": [{"title": "...", "url": "...", "source": "..."}]
# NOT: "references": []
```

### Test 2: Configure Unsplash API

**Action:**
1. Follow `docs/API_SETUP_GUIDE.md` to get Unsplash Access Key
2. Add `UNSPLASH_ACCESS_KEY` to GitHub Secrets

**Expected Result:**
- Content generation should download real images
- Posts should NOT use placeholder images
- Images saved to `static/images/` directory

**Validation:**
```bash
# Check generated posts
grep "image:" content/*/tech/2026-01-21-*.md
# Should show: image: "/images/20260121-*.jpg"
# NOT: image: "/images/placeholder-tech.jpg"
```

### Test 3: Workflow Validation

**Action:**
1. Run daily-content workflow manually
2. Check workflow logs for warnings

**Expected Result:**
- Pre-flight check shows all API keys configured ✓
- No warnings about missing references
- No warnings about placeholder images
- Quality gate PASSES

**Validation:**
```bash
# In workflow logs, look for:
"✓ UNSPLASH_ACCESS_KEY: Configured"
"✅ Quality Check PASSED: All posts have references and real images!"
```

---

## 🔐 IMMEDIATE ACTION ITEMS

1. **[CRITICAL] Set up Google Custom Search API**
   - Get API key from Google Cloud Console
   - Create Custom Search Engine
   - Add `GOOGLE_API_KEY` and `GOOGLE_CX` to GitHub Secrets

2. **[CRITICAL] Set up Unsplash API**
   - Get Access Key from Unsplash Developers
   - Add `UNSPLASH_ACCESS_KEY` to GitHub Secrets

3. **[REQUIRED] Run test keyword curation**
   - Trigger daily-keywords workflow manually
   - Verify references are generated
   - Check `data/topics_queue.json` for non-empty references

4. **[REQUIRED] Regenerate today's posts**
   - Delete today's 3 posts with placeholder images
   - Run daily-content workflow manually
   - Verify new posts have references and real images

5. **[OPTIONAL] Monitor for 24-48 hours**
   - Check automated runs
   - Verify no warnings in logs
   - Confirm quality gate passes consistently

---

## 📊 SUCCESS CRITERIA

When fully fixed, you should see:

✅ Keywords in `topics_queue.json` have 1-2 references each
✅ Posts include "## References" section with real URLs
✅ Posts use downloaded Unsplash images (paths like `/images/20260121-*.jpg`)
✅ Workflow logs show "Quality gate PASSED"
✅ No warnings about missing API credentials
✅ No manual intervention needed daily

---

## 🎓 LESSONS LEARNED

1. **Silent failures are dangerous** - Code should FAIL LOUDLY when critical dependencies missing
2. **Validation must happen early** - Check environment before starting work, not after
3. **Quality gates must enforce standards** - Don't allow bad content to be published
4. **Documentation is critical** - Clear setup guides prevent recurring issues
5. **Test thoroughly** - Manual testing catches issues automation misses

---

## 📝 NEXT STEPS

1. User must configure Google Custom Search API and Unsplash API (cannot proceed without these)
2. Test the fixes by running workflows manually
3. Verify quality improves over next 2-3 automated runs
4. Monitor for any new issues or edge cases

**Estimated time to fix:** 30-60 minutes (API setup) + 10 minutes (testing)
**Confidence level:** HIGH - Root cause identified and comprehensive fixes implemented
