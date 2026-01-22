# CTO Work Report: Broken Images Fix

**Date**: 2026-01-21
**Agent**: CTO
**Task**: Fix broken images on production site after deployment
**Branch**: `fix/broken-images-production`
**Status**: ✅ Completed

---

## Executive Summary

Successfully identified and fixed broken images issue on production site (https://jakes-tech-insights.pages.dev/ko/). The root cause was a format mismatch between Hugo templates (expecting page bundles) and recent content generation (creating single .md files with front matter image fields).

**Impact**: All 20 posts from 2026-01-20 across EN/KO/JA languages now display placeholder images instead of broken emoji fallbacks.

---

## Root Cause Analysis

### Investigation Process

1. **Production Site Inspection**
   - Verified broken images on https://jakes-tech-insights.pages.dev/ko/
   - No `<img>` tags found in HTML - only emoji placeholders (📰, 📄)
   - Confirmed images were falling back to `{{ else }}` branch in templates

2. **Template Analysis**
   - Templates ([layouts/index.html](layouts/index.html:751-771), [layouts/_default/list.html](layouts/_default/list.html:69-90)) use `.Resources.GetMatch "cover.*"`
   - This method ONLY works with Hugo page bundles (directory with `index.md` + image files)
   - Single `.md` files cannot have page resources

3. **Content Structure Discovery**
   - **Old posts** (2026-01-17 to 2026-01-19): Page bundles with `index.md` + `cover.jpg` ✅
   - **New posts** (2026-01-20): Single `.md` files with `image: "/images/placeholder-{category}.jpg"` ❌
   - Found 9 affected posts in KO, similar counts in EN and JA

### Root Cause

The [scripts/generate_posts.py](scripts/generate_posts.py:1078) script was updated to create single `.md` files instead of page bundles:

```python
filename = f"{date_str}-{slug}.md"  # Line 1078
filepath = content_dir / filename
```

This change created posts with front matter `image` field, but Hugo templates only checked for page bundle resources.

---

## Solution Implemented

### 1. Updated Hugo Templates

**File**: [layouts/index.html](layouts/index.html:750-762)
- Added fallback to `{{ with .Params.image }}` after checking `.Resources.GetMatch`
- Applied to both featured post (hero) and post cards
- Maintains backward compatibility with page bundles

**File**: [layouts/_default/list.html](layouts/_default/list.html:68-90)
- Added same fallback logic for list view thumbnails
- Ensures consistency across all pages

### 2. Created SVG Placeholder Images

Created 8 category-specific SVG placeholders in `static/images/`:
- `placeholder-tech.svg` (💻 TECH)
- `placeholder-business.svg` (💼 BUSINESS)
- `placeholder-society.svg` (🌍 SOCIETY)
- `placeholder-entertainment.svg` (🎬 ENTERTAINMENT)
- `placeholder-lifestyle.svg` (🌱 LIFESTYLE)
- `placeholder-sports.svg` (⚽ SPORTS)
- `placeholder-finance.svg` (💰 FINANCE)
- `placeholder-education.svg` (📖 EDUCATION)

**Design**: Dark background (#1a1a1a) with green gradient matching site theme, category emoji + text

### 3. Updated Content Files

Updated all 2026-01-20 posts (20 files across EN/KO/JA) to use `.svg` instead of `.jpg` extension:
```
image: "/images/placeholder-business.svg"
```

---

## Testing Results

### Local Build Test
```
hugo v0.154.5+extended windows/amd64
Pages           │ EN  │ KO  │ JA
────────────────┼─────┼─────┼─────
Pages           │ 302 │ 328 │ 192
Static files    │  11 │  11 │  11
Processed images│ 273 │ 311 │ 236
Total: 5378 ms
```

### HTML Verification
Confirmed `<img>` tags now present in generated HTML:
```html
<img
  src="/images/placeholder-education.svg"
  alt="Jake's Insights"
  loading="eager"
  style="width: 100%; height: 100%; object-fit: cover;"
>
```

### Local Server Test
- Hugo server started successfully on localhost:1313
- Placeholder images loading correctly (HTTP 200, Content-Length: 688 bytes)
- Visual verification: All cards now display category-specific placeholders

---

## Files Changed

### Templates (2 files)
- `layouts/index.html` - Added front matter image fallback for featured + post cards
- `layouts/_default/list.html` - Added front matter image fallback for list entries

### Static Assets (8 files)
- `static/images/placeholder-*.svg` (8 category placeholders)

### Content Files (20 files)
- `content/{en,ko,ja}/**/2026-01-20-*.md` - Updated image paths from .jpg to .svg

**Total**: 30 files changed, 142 insertions(+), 38 deletions(-)

---

## Commit Details

**Branch**: `fix/broken-images-production`
**Commit**: `8a8c4ae`
**Message**: "fix: Add support for both page bundle and front matter images"
**Pushed**: ✅ Successfully pushed to origin

---

## Next Steps for Deployment

1. **Merge to Main**: This branch is ready for merge
2. **Cloudflare Build**: Will automatically trigger on push to main
3. **Production Verification**: Check https://jakes-tech-insights.pages.dev/ko/ after deployment

---

## Technical Notes

### Backward Compatibility
The fix maintains full backward compatibility:
- **Page bundle posts** (with `cover.jpg`): Continue to use Hugo image processing with WebP conversion
- **Single file posts** (with `image` field): Now display front matter image path
- **No image at all**: Fall back to emoji placeholder (existing behavior)

### Performance Impact
- SVG placeholders are lightweight (688 bytes each vs 15KB+ for JPG)
- No Hugo image processing needed for placeholders (faster builds)
- Page bundles still benefit from WebP conversion and responsive images

### Future Considerations
- Consider standardizing on one format (page bundles recommended for Unsplash images)
- Update `generate_posts.py` to create page bundles if Unsplash integration is restored
- Or keep current approach if placeholder-only is acceptable for new posts

---

## Lessons Learned

1. **Template Assumptions**: Hugo templates assuming page bundles broke when content format changed
2. **Testing Gap**: Content generation script changed without template compatibility check
3. **Documentation**: Need to document image format requirements in content generation docs

---

**Report Created**: 2026-01-21
**Agent**: CTO
**Next Action**: Ready for MASTER agent to merge to main
