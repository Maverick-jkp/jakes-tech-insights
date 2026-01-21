# API Setup Guide

## Critical: Missing API Credentials

Your content generation is failing because **Google Custom Search API credentials are not configured**. This causes:

1. ❌ Keywords generated WITHOUT references
2. ❌ Posts published WITHOUT credible sources
3. ❌ Reduced SEO value and user trust

---

## 🔴 IMMEDIATE ACTION REQUIRED

### Step 1: Set Up Google Custom Search API

#### 1.1 Create Google Cloud Project
1. Go to https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Enable "Custom Search API"
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. **Copy the API Key** → This is your `GOOGLE_API_KEY`

#### 1.2 Create Custom Search Engine
1. Go to https://programmablesearchengine.google.com/
2. Click "Add" to create new search engine
3. Configure:
   - **Search the entire web**: Enable
   - **Search engine name**: "Tech Insights Reference Search"
4. Click "Create"
5. Go to "Setup" → Copy the **Search engine ID** → This is your `GOOGLE_CX`

#### 1.3 Configure GitHub Secrets
1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add the following repository secrets:
   - `GOOGLE_API_KEY`: Your Google Cloud API key
   - `GOOGLE_CX`: Your Custom Search Engine ID
   - `UNSPLASH_ACCESS_KEY`: Your Unsplash Access Key (see Step 2)

---

### Step 2: Set Up Unsplash API (Image Downloads)

#### 2.1 Create Unsplash Developer Account
1. Go to https://unsplash.com/developers
2. Register/Login
3. Create a new application
4. Copy your **Access Key** → This is your `UNSPLASH_ACCESS_KEY`

#### 2.2 Add to GitHub Secrets
1. Settings → Secrets and variables → Actions
2. Add new secret:
   - Name: `UNSPLASH_ACCESS_KEY`
   - Value: Your Unsplash Access Key

---

## 🧪 Testing Locally

### Test Keyword Curation
```bash
export ANTHROPIC_API_KEY="your-key"
export GOOGLE_API_KEY="your-google-key"
export GOOGLE_CX="your-search-engine-id"

python scripts/keyword_curator.py --count 5
```

**Expected Output:**
- ✓ Should fetch trending topics from Google Trends
- ✓ Should search for references using Google Custom Search
- ✓ Should extract 2 references per keyword
- ✓ Should show "All 5 keywords have references!" message

**If you see warnings:**
- ⚠️ "Google Custom Search not configured" → API keys not set
- ⚠️ "X keywords have NO references" → Google API quota exceeded or invalid credentials

### Test Content Generation
```bash
export ANTHROPIC_API_KEY="your-key"
export UNSPLASH_ACCESS_KEY="your-unsplash-key"

python scripts/generate_posts.py --count 1
```

**Expected Output:**
- ✓ Pre-flight check should show both API keys configured
- ✓ Should download real Unsplash images (not placeholders)
- ✓ Should include references section in generated posts
- ✓ Quality check should PASS with no warnings

---

## 🚨 Common Issues

### Issue 1: "No references generated"
**Cause:** Google Custom Search API credentials missing or invalid

**Fix:**
1. Verify `GOOGLE_API_KEY` and `GOOGLE_CX` are set correctly
2. Check Google Cloud Console: Is Custom Search API enabled?
3. Check billing: Google requires a billing account (free tier available)

### Issue 2: "Placeholder images used"
**Cause:** `UNSPLASH_ACCESS_KEY` not configured

**Fix:**
1. Get Unsplash Access Key from https://unsplash.com/developers
2. Add to GitHub Secrets: `UNSPLASH_ACCESS_KEY`
3. Verify the key is valid by testing locally

### Issue 3: "API quota exceeded"
**Cause:** Google Custom Search has limits (100 queries/day on free tier)

**Temporary Fix:**
- Reduce keyword count: `--count 5` instead of `--count 15`

**Permanent Fix:**
- Upgrade to paid tier (100 queries/day → unlimited)
- Or implement caching/batching strategy

---

## 📊 Monitoring

### Check Workflow Logs
1. Go to Actions tab in GitHub
2. Click on "Daily Keyword Curation" workflow
3. Look for warnings:
   - "Google Custom Search not configured"
   - "X keywords have NO references"

### Validate Generated Content
1. Check `data/topics_queue.json`
2. Look for `"references": []` (empty array = BAD)
3. Should see `"references": [{"title": "...", "url": "...", "source": "..."}]`

### Test Posts
1. Check generated posts in `content/*/tech/*.md`
2. Search for "## References" section
3. Verify images are NOT placeholder paths (`/images/placeholder-*.jpg`)

---

## ✅ Success Criteria

When properly configured, you should see:

1. ✅ Keywords have 1-2 references each in `topics_queue.json`
2. ✅ Posts include "## References" section with real URLs
3. ✅ Posts use downloaded Unsplash images (not placeholders)
4. ✅ No warnings in workflow logs about missing credentials
5. ✅ Quality gate passes with "All posts have references and real images!"

---

## 🔧 Emergency Fallback

If you can't configure Google API immediately:

1. **Option A**: Use existing keywords from queue (already curated)
2. **Option B**: Manually add references to posts after generation
3. **Option C**: Generate keywords without references (not recommended - SEO impact)

**Long-term:** You MUST configure Google Custom Search API for sustainable content generation.
