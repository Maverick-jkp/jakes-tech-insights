# Related Posts ("You Might Also Like") Investigation Report

**Date**: 2026-01-22
**Agent**: Master
**Status**: ✅ Investigation Complete

---

## Summary

Investigated two issues with the "You Might Also Like" section:
1. **Why it appears on some posts but not others**: Hugo's `.Related` function requires a minimum threshold score (80) and sufficient similar content. Posts without enough related content (based on categories, tags, date) won't show this section.
2. **Why thumbnails show placeholders instead of actual images**: The template is looking for Page Resources (`cover.*`) instead of the actual image paths specified in frontmatter.

---

## Issue 1: Related Posts Appearing Inconsistently

### Root Cause Analysis

**Location**: [layouts/_default/single.html:617-638](layouts/_default/single.html#L617-L638)

```hugo
{{ $related := .Site.RegularPages.Related . | first 4 }}
{{ with $related }}
<div class="related-posts">
    ...
</div>
{{ end }}
```

**Hugo Configuration**: [hugo.toml:241-256](hugo.toml#L241-L256)

```toml
[related]
  includeNewer = true
  threshold = 80        # Minimum score required
  toLower = false

  [[related.indices]]
    name = "categories"
    weight = 100

  [[related.indices]]
    name = "tags"
    weight = 80

  [[related.indices]]
    name = "date"
    weight = 10
```

### How Hugo's Related Content Works

Hugo calculates a similarity score between posts:
- **Categories match**: 100 points
- **Tags match**: 80 points per matching tag
- **Date proximity**: 10 points (if published close together)

**Threshold requirement**: Posts must score at least **80 points** to be considered "related".

### Testing Results

1. **Post with related content** (`/ko/tech/2026-01-22-붉은사막/`):
   - Has 1 related post shown
   - Reason: Only 2 total tech posts in Korean → limited pool
   - The older post (2026-01-21-붉은사막.md) is similar enough (same category + similar tag)

2. **Post without related section** (`/ko/business/2026-01-22-다보스-포럼/`):
   - No related posts section appears
   - Reason: Only 1 business post in Korean → no matches possible

3. **Content statistics**:
   - Total posts across all languages: 29
   - Korean tech posts: 2
   - Korean business posts: 1
   - **Problem**: Not enough content in each category for meaningful related posts

### Why Some Posts Show Nothing

The `{{ with $related }}` directive only renders the section if `$related` is not empty:
- If no posts score ≥80 points, `$related` is empty
- The entire "You Might Also Like" section is hidden
- **This is by design** - Hugo doesn't show related posts if there aren't any good matches

---

## Issue 2: Thumbnails Showing Placeholders

### Root Cause Analysis

**Location**: [layouts/_default/single.html:624-630](layouts/_default/single.html#L624-L630)

```hugo
<div class="related-thumbnail">
    {{ with .Resources.GetMatch "cover.*" }}
        {{ $thumb := .Fill "300x150 webp q85" }}
        <img src="{{ $thumb.RelPermalink }}" alt="{{ $.Title }}" loading="lazy">
    {{ else }}
        📄
    {{ end }}
</div>
```

### The Problem

**What the code does**:
- Looks for Page Resources (files in same directory as post markdown file)
- Searches for `cover.*` (cover.jpg, cover.png, etc.)
- If not found, shows placeholder emoji 📄

**What the posts actually have**:
- Images specified in frontmatter: `image: "/images/20260122-붉은사막.jpg"`
- Images stored in `/static/images/` directory
- **These are NOT Page Resources** - they're site-wide static assets

### Example Post Structure

```
content/ko/tech/2026-01-22-붉은사막.md:
---
image: "/images/20260122-붉은사막.jpg"
---

static/images/20260122-붉은사막.jpg
```

The template is looking for:
```
content/ko/tech/2026-01-22-붉은사막/cover.jpg  ← DOESN'T EXIST
```

### Why All Related Posts Show Placeholders

1. Template searches for `cover.*` in post directory
2. No posts have cover images as Page Resources
3. Falls back to placeholder emoji 📄
4. Actual images in `/static/images/` are ignored

---

## Recommendations

### Option 1: Fix Template to Use Frontmatter Images (Recommended)

**Pros**:
- Works with current content structure
- No need to reorganize files
- Leverages existing images in `/static/images/`

**Cons**:
- Can't use Hugo's image processing (resize, WebP conversion)
- Images loaded at original size (potential performance impact)

**Implementation**:
```hugo
<div class="related-thumbnail">
    {{ with .Params.image }}
        <img src="{{ . }}" alt="{{ $.Title }}" loading="lazy">
    {{ else }}
        📄
    {{ end }}
</div>
```

### Option 2: Migrate to Page Bundles

**Pros**:
- Can use Hugo's image processing (.Fill, .Resize, etc.)
- Better performance with optimized WebP images
- Industry best practice for Hugo sites

**Cons**:
- Requires reorganizing all content files
- Need to move images from `/static/images/` to post directories
- More complex file structure

**Required structure**:
```
content/ko/tech/2026-01-22-붉은사막/
├── index.md
└── cover.jpg
```

### Option 3: Hybrid Approach

Use frontmatter image but process it through Hugo:
```hugo
{{ with .Params.image }}
    {{ $img := resources.Get (strings.TrimPrefix "/" .) }}
    {{ with $img }}
        {{ $thumb := .Fill "300x150 webp q85" }}
        <img src="{{ $thumb.RelPermalink }}" alt="{{ $.Title }}" loading="lazy">
    {{ else }}
        <img src="{{ $.Params.image }}" alt="{{ $.Title }}" loading="lazy">
    {{ end }}
{{ else }}
    📄
{{ end }}
```

**Note**: This only works if images are in `assets/` directory, not `static/`.

---

## Proposed Solution

### For Issue 1: Related Posts Not Appearing

**Short-term**: Accept current behavior
- With only 29 posts total, related content will naturally be sparse
- As content grows, more related posts will appear automatically
- No code changes needed

**Long-term**: Consider lowering threshold
- Change `threshold = 80` to `threshold = 60` in [hugo.toml:243](hugo.toml#L243)
- Will show more "loosely related" posts
- Better for sites with < 50 posts per category

### For Issue 2: Thumbnail Placeholders

**Recommended**: Update template to use frontmatter images

**File to modify**: [layouts/_default/single.html:624-630](layouts/_default/single.html#L624-L630)

**Change from**:
```hugo
{{ with .Resources.GetMatch "cover.*" }}
    {{ $thumb := .Fill "300x150 webp q85" }}
    <img src="{{ $thumb.RelPermalink }}" alt="{{ $.Title }}" loading="lazy">
{{ else }}
    📄
{{ end }}
```

**Change to**:
```hugo
{{ with .Params.image }}
    <img src="{{ . }}" alt="{{ $.Title }}" loading="lazy"
         style="width: 100%; height: 100%; object-fit: cover;">
{{ else }}
    📄
{{ end }}
```

---

## Testing Plan

1. Update single.html template
2. Test on local dev server:
   - Verify thumbnails appear on related posts
   - Check responsive behavior
   - Confirm images load correctly
3. Test on multiple posts with different languages
4. Build and verify no broken images

---

## Next Steps

1. **User Decision Required**: Choose solution approach for thumbnails
2. **Implement template fix** (if Option 1 approved)
3. **Test thoroughly** on local server
4. **Commit changes** with proper co-authorship
5. **Consider future migration** to Page Bundles as content grows

---

**Report Created**: 2026-01-22 14:30 KST
**Next Action**: Awaiting user approval to implement thumbnail fix (Option 1 recommended)
