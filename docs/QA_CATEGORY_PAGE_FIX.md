# QA Test Report: Category Page Thumbnail Fix

**Date**: 2026-01-20
**Tester**: Claude Code
**Issue**: Category page thumbnails showing as placeholders after 22e5f03 deployment
**Root Cause**: Incorrect context variable in list.html template

---

## Problem Analysis

### Original Issue
After deploying commit 22e5f03, all category pages (e.g., `/ko/categories/tech/`) showed placeholder icons (📄) instead of post thumbnails.

### Root Cause
In `layouts/_default/list.html` line 69, the code used:
```go
{{- with .Resources.GetMatch "cover.*" }}
```

**Problem**: Inside the `{{ range $index, $page := $paginator.Pages }}` loop, `.Resources` refers to the **list page's resources**, not the **individual post's resources**.

### Solution
Changed to use the correct page context:
```go
{{- with $page.Resources.GetMatch "cover.*" }}
```

Also updated the alt text from `{{ $.Title }}` to `{{ $page.Title }}` for consistency.

---

## Files Changed

### layouts/_default/list.html
```diff
- {{- with .Resources.GetMatch "cover.*" }}
+ {{- with $page.Resources.GetMatch "cover.*" }}
  <figure class="entry-cover">
    {{ $thumb := .Fill "400x200 webp q85" }}
    {{ $thumb2x := .Fill "800x400 webp q85" }}
    {{ $fallback := .Fill "400x200 jpg q85" }}
    <picture>
      <source
        srcset="{{ $thumb.RelPermalink }} 1x,
                {{ $thumb2x.RelPermalink }} 2x"
        type="image/webp"
      >
      <img
        src="{{ $fallback.RelPermalink }}"
-       alt="{{ $.Title }}"
+       alt="{{ $page.Title }}"
        loading="lazy"
        width="400"
        height="200"
        style="width: 100%; height: auto; object-fit: cover;"
      >
    </picture>
  </figure>
  {{- end }}
```

---

## QA Test Checklist

Please verify the following pages after deployment:

### Homepage Tests
- [ ] Featured post thumbnail displays correctly (not placeholder)
- [ ] Regular post card thumbnails display (8 cards in 4x2 grid)
- [ ] Floating widget shows 2x4 category grid
- [ ] All 8 categories visible in floating widget

### Category Page Tests (/ko/categories/tech/)
- [ ] All post thumbnails display correctly (not 📄 placeholder)
- [ ] Images use WebP format with JPG fallback
- [ ] Floating widget appears in bottom-right
- [ ] Floating widget shows 2x4 category grid (8 categories)
- [ ] Category grid links work correctly

### Category Page Tests (/ko/categories/business/)
- [ ] All post thumbnails display correctly
- [ ] Floating widget works
- [ ] All 8 categories visible

### Category Page Tests (/ko/categories/society/)
- [ ] All post thumbnails display correctly
- [ ] Floating widget works
- [ ] All 8 categories visible

### Category Page Tests (All Other Categories)
Test for: entertainment, lifestyle, sports, finance, education
- [ ] Tech category
- [ ] Business category
- [ ] Society category
- [ ] Entertainment category
- [ ] Lifestyle category
- [ ] Sports category
- [ ] Finance category
- [ ] Education category

### Multi-language Tests
- [ ] Korean (/ko/categories/*)
- [ ] Japanese (/ja/categories/*)
- [ ] English (/categories/*)

### Mobile Responsiveness
- [ ] Thumbnails display correctly on mobile
- [ ] Floating widget accessible on mobile
- [ ] Category grid readable on mobile

### Performance Tests
- [ ] Images load with lazy loading
- [ ] WebP format served to modern browsers
- [ ] JPG fallback served to older browsers
- [ ] Page load time acceptable (<3s)

---

## Expected Results

### Before Fix (22e5f03)
- ❌ Category pages show 📄 placeholder icon
- ❌ No actual post images visible
- ✅ Floating widget works
- ✅ Homepage works correctly

### After Fix (Current)
- ✅ Category pages show actual post thumbnails
- ✅ Images processed as WebP + JPG fallback
- ✅ Floating widget works with 2x4 grid
- ✅ Homepage continues to work correctly
- ✅ All 8 categories visible

---

## Technical Details

### Image Processing
- Format: WebP with JPG fallback
- Sizes: 400x200 (1x), 800x400 (2x retina)
- Quality: 85%
- Loading: Lazy (except featured post)
- Object-fit: cover

### Page Bundle Structure
```
content/ko/tech/2026-01-20-example-post/
├── index.md
└── cover.jpg
```

Hugo processes these into:
- `cover_hu123abc_400x200_fill_q85.webp`
- `cover_hu123abc_800x400_fill_q85.webp`
- `cover_hu123abc_400x200_fill_q85.jpg`

---

## Deployment Steps

1. Commit the fix:
   ```bash
   git add layouts/_default/list.html
   git commit -m "🐛 Fix: Correct page context for category page thumbnails"
   ```

2. Push to GitHub:
   ```bash
   git push origin main
   ```

3. Wait for Cloudflare Pages deployment (~2-3 minutes)

4. Run QA tests using this checklist

5. If any test fails, document in "Issues Found" section below

---

## Issues Found

### Issue 1: [Add any issues found during QA]
- **Description**:
- **Steps to Reproduce**:
- **Expected**:
- **Actual**:
- **Fix**:

---

## Sign-off

- [ ] All homepage tests passed
- [ ] All category page tests passed
- [ ] Multi-language tests passed
- [ ] Mobile tests passed
- [ ] Performance tests passed
- [ ] No regressions found

**QA Tester**: ___________________
**Date**: ___________________
**Status**: ⬜ PASS / ⬜ FAIL

---

## Additional Notes

- The fix changes `.Resources` to `$page.Resources` in the range loop
- This ensures each post's page bundle resources are accessed correctly
- No changes to image processing logic or floating widget
- Previous commit 22e5f03 successfully added floating widget but had wrong context variable
