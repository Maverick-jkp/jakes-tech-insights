# Windows Environment Setup & Known Issues

## 🚨 Critical Issue: Unsplash Image Downloads Fail on Windows

### Problem
All Unsplash image downloads fail with "HTTP error: unknown" on Windows environment.

**Symptoms:**
```
🔍 Searching Unsplash for: nasdaq finance money
✓ Found image by [photographer]
📥 Downloading optimized image (1200px, q85)...
⚠️ Image download HTTP error: unknown  # ❌ FAILS EVERY TIME
```

### Root Cause
Windows Python installation missing proper SSL certificate chain for HTTPS requests to Unsplash CDN.
- ✅ Mac: System root certificates work fine
- ❌ Windows: Python requests library can't verify Unsplash SSL certificates

### Solution Required (Not Yet Applied)

#### Step 1: Install certifi package
```bash
cd C:\Users\[your-username]\projects\jakes-tech-insights
pip install certifi
```

#### Step 2: Update generate_posts.py

**File:** `scripts/generate_posts.py`
**Line:** ~918 (Unsplash API request)

**Current code:**
```python
response = requests.get(url, headers=headers, params=params, timeout=10)
```

**Change to:**
```python
import certifi
response = requests.get(url, headers=headers, params=params, timeout=10, verify=certifi.where())
```

**Also update line ~1040 (image download):**
```python
# Current
response = requests.get(url, timeout=30)

# Change to
response = requests.get(url, timeout=30, verify=certifi.where())
```

#### Step 3: Test
```bash
python scripts/generate_posts.py --topic-id [test-topic-id]
```

Verify that images download successfully to `static/images/`.

---

## ✅ Completed Mac Session Fixes (2026-01-21)

### Fix #1: Git Push Race Condition
- **Commit:** 9bc64ee
- **Status:** ✅ Fixed
- **Details:** Added pull-rebase + retry logic to prevent concurrent push failures

### Fix #2: Unsplash Keyword Translations
- **Commit:** cee879a
- **Status:** ✅ Fixed
- **Details:** Added 27 AI/Jobs keyword translations (Korean/Japanese)

### Fix #3: Workflow Stale Data
- **Commit:** f4d926f
- **Status:** ✅ Fixed
- **Details:** Added git pull to fetch latest topics_queue.json before generation

---

## 📋 Windows Environment Checklist

When switching back to Windows, ensure:

- [ ] Python 3.11+ installed
- [ ] Git configured with user.name and user.email
- [ ] `pip install certifi` (CRITICAL for Unsplash)
- [ ] Apply certifi fix to generate_posts.py
- [ ] Test Unsplash image download locally
- [ ] Verify GitHub Actions still works (it runs on Linux, unaffected)

---

## 🎯 Next Tasks for Windows Session

### Priority 1: Fix SSL Certificate Issue (5 min)
1. Install certifi
2. Update generate_posts.py with verify=certifi.where()
3. Test image downloads
4. Commit fix

### Priority 2: Remove Hardcoded Mac Paths (10 min)
Fix `scripts/fetch_images_for_posts.py` lines 201 & 232:

**Current:**
```python
image_output_path = Path(f"/Users/jakepark/projects/jakes-tech-insights/static/images/{image_filename}")
content_dir = Path("/Users/jakepark/projects/jakes-tech-insights/content")
```

**Change to:**
```python
project_root = Path(__file__).parent.parent
image_output_path = project_root / "static" / "images" / image_filename
content_dir = project_root / "content"
```

### Priority 3: Add Optimistic Locking (30 min)
Add version field to topics_queue.json to prevent race conditions:

**File:** `scripts/topic_queue.py`

Add to _save_queue():
```python
def _save_queue(self, data: Dict):
    # Increment version
    data['version'] = data.get('version', 0) + 1

    # Atomic write
    import tempfile
    temp_fd, temp_path = tempfile.mkstemp(dir=self.queue_file.parent)
    with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(temp_path, self.queue_file)
```

Add to reserve_topics():
```python
def reserve_topics(self, count: int) -> List[Dict]:
    data = self._load_queue()
    expected_version = data.get('version', 0)

    # ... reservation logic ...

    # Check version before saving
    current_data = self._load_queue()
    if current_data.get('version', 0) != expected_version:
        raise ConcurrencyError("Queue was modified by another process - retry")

    self._save_queue(data)
```

---

## 🐛 Known Issues (Deferred from Windows Session)

### Issue: Placeholder Images Policy Violation
- **Date:** 2026-01-21 00:00-01:15 KST
- **Incident:** CTO Agent attempted to commit posts with placeholder images
- **User Policy:** Placeholder images are ABSOLUTELY FORBIDDEN
- **Action Taken:** Emergency rollback, deferred to Mac
- **Resolution:** Fixed on Mac with keyword translations (cee879a)

---

## 📊 System Health Status

| Component | Mac | Windows | GitHub Actions |
|-----------|-----|---------|----------------|
| Content Generation | ✅ Working | ⚠️ Untested | ✅ Working |
| Keyword Curation | ✅ Working | ⚠️ Untested | ✅ Working |
| Unsplash Images | ✅ Working | ❌ SSL Error | ✅ Working (Linux) |
| Git Push | ✅ Working | ⚠️ Untested | ✅ Fixed (retry logic) |
| Quality Gate | ✅ Working | ⚠️ Untested | ✅ Working |

---

## 🔧 Environment-Specific Notes

### Mac (Current)
- All systems operational
- Use this environment for critical operations
- Image generation works perfectly

### Windows (Next Session)
- **MUST fix SSL issue before using**
- Good for development/testing
- Not recommended for production image generation until fixed

### GitHub Actions (Production)
- Runs on Linux (ubuntu-latest)
- Unaffected by local environment issues
- Automated workflows functioning after recent fixes

---

## 📝 Session Handoff Notes

**From:** Mac session (2026-01-21 evening)
**To:** Windows session (next 3-4 days)

**Completed:**
- ✅ All critical automation bugs fixed
- ✅ Git push race conditions resolved
- ✅ Keyword translations expanded
- ✅ Workflow coordination improved

**Your Tasks:**
1. Fix Windows SSL certificate issue (certifi)
2. Remove hardcoded Mac paths
3. Test full content generation pipeline
4. Optional: Add optimistic locking for extra reliability

**Blockers:**
- None - all systems operational on Mac
- Windows needs SSL fix before image generation

---

**Last Updated:** 2026-01-21 22:30 KST (Mac)
**Next Update:** When switching to Windows
