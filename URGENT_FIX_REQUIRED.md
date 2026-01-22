# 🚨 URGENT: Fix Required Before Next Content Generation

## Problem Confirmed

Your content is being generated **WITHOUT references** and **WITH placeholder images** because:

### ❌ Missing API Credentials

```
GOOGLE_API_KEY: NOT SET
GOOGLE_CX: NOT SET
UNSPLASH_ACCESS_KEY: NOT SET
```

---

## ⚡ Quick Fix (30 minutes)

### 1. Get Google Custom Search API Credentials

1. Go to: https://console.cloud.google.com/
2. Create/select project → Enable "Custom Search API"
3. Create API Key → Copy it (this is `GOOGLE_API_KEY`)

4. Go to: https://programmablesearchengine.google.com/
5. Create search engine → "Search entire web"
6. Copy Search Engine ID (this is `GOOGLE_CX`)

### 2. Get Unsplash API Key

1. Go to: https://unsplash.com/developers
2. Register → Create application
3. Copy Access Key (this is `UNSPLASH_ACCESS_KEY`)

### 3. Add to GitHub Secrets

1. Go to: https://github.com/YOUR_REPO/settings/secrets/actions
2. Add these 3 repository secrets:
   - `GOOGLE_API_KEY`: [your Google API key]
   - `GOOGLE_CX`: [your search engine ID]
   - `UNSPLASH_ACCESS_KEY`: [your Unsplash key]

### 4. Test

```bash
# Trigger workflow manually from GitHub Actions tab:
# Run "Daily Keyword Curation" first
# Then run "Daily Content Generation"

# Check logs - should see:
# ✓ GOOGLE_API_KEY: Configured
# ✓ UNSPLASH_ACCESS_KEY: Configured
# ✅ Quality Check PASSED: All posts have references and real images!
```

---

## 📖 Detailed Guide

See: `/Users/jakepark/projects/jakes-tech-insights/docs/API_SETUP_GUIDE.md`

---

## ✅ What Was Fixed

1. **Added validation** - Workflows will now FAIL if API keys missing
2. **Added warnings** - Clear messages show which APIs need configuration
3. **Added quality gate** - New script prevents publishing bad content
4. **Added documentation** - Step-by-step guides for API setup

---

## 🎯 Success Criteria

After configuration, you should see:

- ✅ Keywords have references in `data/topics_queue.json`
- ✅ Posts include "## References" section
- ✅ Posts use real Unsplash images (not placeholders)
- ✅ Workflow logs show quality gate PASSED
- ✅ No manual fixes needed

---

## 🆘 Need Help?

Read the full analysis: `/Users/jakepark/projects/jakes-tech-insights/docs/ROOT_CAUSE_ANALYSIS_2026-01-21.md`
