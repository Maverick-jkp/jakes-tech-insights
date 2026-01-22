# Design System

## Overview

Jake's Tech Insights uses a custom design system built on top of the Hugo PaperMod theme. The design emphasizes clean layouts, consistent visual hierarchy, and language-specific optimizations for English, Korean, and Japanese content.

## Color System

### Primary Colors
- **Green Accent**: Category badges, buttons, and interactive elements
- **Background**: Clean white/light theme for optimal readability
- **Text**: High-contrast dark text on light backgrounds

### Category Colors
All categories use the consistent green accent color for badges and highlights across:
- Tech
- Business
- Society
- Entertainment
- Lifestyle

## Layout Structure

### Homepage Bento Grid

The homepage uses a responsive Bento grid layout with three main components:

1. **Featured Card** (Large)
   - Vertical layout with thumbnail on top
   - Full-width thumbnail (180px height)
   - Green category badge
   - Language-specific height: 420px (EN), 480px (KO/JA)

2. **Latest Widget** (Medium)
   - Shows exactly 3 recent posts
   - Skips the featured post to avoid duplication
   - Compact thumbnails (60px height)
   - Compact spacing (0.3rem gaps, 0.4rem padding)
   - No scrollbar, all content visible

3. **Small Cards** (Grid)
   - Multiple post cards in grid layout
   - Green category badges
   - Consistent height with Featured/Latest sections
   - AdSense widget placeholder matches design

### Language-Specific Sizing

Due to character height differences, Korean and Japanese text requires additional vertical space:

```css
/* English: Default height */
.featured-card { height: 420px; }

/* Korean: Additional 60px */
body[lang="ko"] .featured-card { height: 480px; }

/* Japanese: Additional 60px */
body[lang="ja"] .featured-card { height: 480px; }
```

This applies to:
- Featured cards
- Latest widget items
- Small cards in grid
- Category page cards

## Typography

### Font Hierarchy

- **Headlines**: Bold, high-contrast
- **Body Text**: Optimized for readability
- **Meta Information**: Smaller, secondary color
- **Links**: Clear hover states

### Language Considerations

- **English**: Latin characters with standard line height
- **Korean (한국어)**: CJK characters requiring increased line height
- **Japanese (日本語)**: CJK characters with vertical spacing optimization

## Homepage Layout

### Bento Grid Components

**Featured Card Design:**
- Thumbnail: Full width, 180px height, positioned on top
- Category badge: Green, top-left corner
- Title: Large, bold font
- Description: Truncated to 150 characters
- Vertical layout provides better visual hierarchy than horizontal

**Latest Widget Optimization:**
```html
{{ range after 1 (first 4 $currentLangPages) }}
  <!-- Shows posts 2-4, skipping the featured post -->
{{ end }}
```

**Spacing Rules:**
- Gap between cards: 0.3rem
- Internal padding: 0.4rem
- Thumbnail margins: Minimal for compact display
- No scrollbars: All content visible in viewport

### Featured Card Evolution

**Before:**
- Horizontal layout (thumbnail left, content right)
- Small thumbnail (limited visual impact)
- Inconsistent with other card designs

**After:**
- Vertical layout (thumbnail top, content below)
- Full-width thumbnail (maximum visual impact)
- Green category badge matching other cards
- Better screen space utilization

## Category Pages

### Page Structure

1. **Header Section**
   - Category title (e.g., "Tech", "Business")
   - Multilingual description
   - Floating menu button

2. **Description Text Examples**

**Tech:**
- EN: "Exploring the essence of technology and designing the future"
- KO: "기술의 본질을 탐구하고 미래를 설계합니다"
- JA: "テクノロジーの本質を探求し、未来をデザインする"

**Business:**
- EN: "Discovering hidden principles of business and creating growth"
- KO: "비즈니스의 숨은 원리를 발견하고 성장을 만듭니다"
- JA: "ビジネスの隠れた原理を発見し、成長を創造する"

**Society:**
- EN: "Reading societal changes and imagining a better tomorrow"
- KO: "사회의 변화를 읽고 더 나은 내일을 상상합니다"
- JA: "社会の変化を読み取り、より良い明日を想像する"

**Entertainment:**
- EN: "Following cultural trends and discovering joy"
- KO: "문화 트렌드를 따라가며 즐거움을 발견합니다"
- JA: "文化トレンドを追い、喜びを発見する"

**Lifestyle:**
- EN: "Rediscovering everyday values and creating a better life"
- KO: "일상의 가치를 재발견하고 더 나은 삶을 만듭니다"
- JA: "日常の価値を再発見し、より良い暮らしを創る"

3. **Post Cards**
   - Grid layout
   - Text-only excerpts (no images in previews)
   - Truncated to 120 characters using `{{ .Summary | plainify | truncate 120 }}`
   - Green category badges

### CSS Class Structure

**Critical Naming Convention:**
- `.card-content`: Used for card preview content
- `.post-content`: Used for full post content on single pages
- Separation prevents CSS conflicts between layouts

### Floating Menu

Present on all pages (category, single post, all-posts):
- Hamburger icon button
- Links to: Home, All Posts, all categories
- Language-aware URLs (e.g., `/ko/categories/tech`)
- Fixed position for easy access

## All-Posts Page

### Card Display

- Text-only excerpts using `{{ .Summary | plainify | truncate 150 }}`
- Removes all HTML and images from previews
- Consistent card heights
- No reading time display (removed for accuracy)

### Logo Standardization

All pages use consistent branding:
```
JAKE'S INSIGHTS
```

Previous inconsistencies ("Jake's Tech Insights") have been unified.

## Single Post Pages

### Content Area

**Image Sizing:**
```css
.post-content img {
  max-width: 500px;
  margin: 1rem auto;
  display: block;
}

@media (max-width: 768px) {
  .post-content img {
    max-width: 100%;
  }
}
```

**Rationale:**
- Prevents images from dominating viewport
- Keeps content above the fold
- Responsive on mobile devices

### Navigation

- Floating menu present on all single post pages
- Same design as category pages
- Consistent user experience across site

## Design Decisions

### Why Vertical Featured Layout?

1. **Visual Impact**: Full-width thumbnail is more engaging than side thumbnail
2. **Consistency**: Matches the vertical flow of other cards
3. **Screen Real Estate**: Better utilizes available width
4. **Hierarchy**: Clear top-to-bottom reading pattern

### Why Text-Only Excerpts?

1. **Performance**: Faster rendering without image processing
2. **Layout Stability**: No unpredictable heights from embedded content
3. **Clarity**: Plain text is easier to scan in card previews
4. **Mobile Optimization**: Reduces data usage and scroll length

### Why Language-Specific Heights?

1. **Character Density**: CJK characters are visually denser than Latin
2. **Line Height**: Korean/Japanese require more vertical spacing
3. **Readability**: Prevents cramped appearance in cards
4. **Consistency**: Maintains visual balance across languages

### Why Green Category Badges?

1. **Brand Identity**: Consistent accent color across all elements
2. **Visibility**: High contrast against white backgrounds
3. **Hierarchy**: Clearly identifies content category
4. **Recognition**: Users quickly associate color with categories

## Files Modified

Design system implementation spans multiple files:

- `layouts/index.html` - Homepage Bento grid layout
- `layouts/categories/list.html` - Category landing pages
- `layouts/_default/all-posts.html` - All posts listing page
- `layouts/_default/single.html` - Individual post pages
- `assets/css/extended/custom.css` - Image width overrides and custom styles

## Testing Checklist

When modifying the design system, verify:

- [ ] All 3 languages (EN/KO/JA) display correctly
- [ ] Featured card thumbnail is full-width
- [ ] Latest widget shows exactly 3 items
- [ ] No scrollbars in Latest widget
- [ ] Category descriptions appear in correct language
- [ ] Floating menu works on all page types
- [ ] Card excerpts are text-only (no images)
- [ ] Mobile responsive behavior (< 768px)
- [ ] Green badges visible on all card types
- [ ] Logo consistency across all pages

## Future Enhancements

Potential design system improvements:

- Dark mode support
- Additional accent colors for variety
- Animation transitions between pages
- Progressive image loading
- Advanced typography with variable fonts
- Accessibility improvements (WCAG 2.1 AA)
