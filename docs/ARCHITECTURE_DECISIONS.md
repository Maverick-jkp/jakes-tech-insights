# Architecture Decision Records (ADR)

## Overview

This document records key architectural decisions made during the development of Jake's Tech Insights, including the rationale, alternatives considered, and consequences of each decision.

---

## ADR-001: Category-Based Taxonomy (Primary Organization)

### Status
Accepted - Implemented on Day 1

### Context
The site needed a clear content organization system for automated content generation and user navigation. We needed to decide between tag-based, category-based, or hybrid taxonomy.

### Decision
Use **category-based taxonomy** as the primary (and only) content organization method with exactly 5 categories:
- Tech
- Business
- Society
- Entertainment
- Lifestyle

### Rationale

**1. Clear Content Segmentation**
- 5 categories provide intuitive, non-overlapping buckets
- Easy for users to browse by general topic area
- Predictable navigation structure

**2. SEO Benefits**
- Category pages rank for broader keywords (e.g., "tech articles")
- Focused content clusters build topical authority
- Clean URL structure: `/categories/tech/`

**3. Navigation Simplicity**
- 5 clear sections vs. dozens of unpredictable tags
- Reduces cognitive load for users
- Simpler menu structure

**4. Automated Classification**
- AI can reliably assign 1 of 5 categories
- Reduces classification errors
- Consistent categorization across languages

**5. URL Structure**
- Clean, predictable URLs: `/tech/my-article/`
- Category visible in URL path
- Better for SEO and user understanding

### Alternatives Considered

**Option 1: Tag-Based Taxonomy**
- Pros: Flexible, granular classification
- Cons:
  - AI-generated tags are inconsistent
  - Creates too many thin tag pages (bad for SEO)
  - Overlapping tags confuse users
  - Requires ongoing tag curation

**Option 2: Hybrid (Categories + Tags)**
- Pros: Both broad and granular classification
- Cons:
  - Redundancy between categories and tags
  - Complexity in navigation (multiple paths to same content)
  - Maintenance burden (tag cleanup)
  - SEO dilution across too many pages

**Option 3: Single Stream (No Taxonomy)**
- Pros: Simplest implementation
- Cons:
  - Poor user experience (can't filter content)
  - No topical authority building
  - Weak SEO (no category pages)

### Consequences

**Positive:**
- Clear, simple navigation
- Strong category page SEO
- Reliable automated categorization
- Easy to maintain

**Negative:**
- Less granular than tags
- Can't cross-reference topics easily
- May need to recategorize if categories change

**Neutral:**
- 5 categories may need adjustment over time
- Some posts could fit multiple categories (resolved by choosing primary)

---

## ADR-002: Tags Removed (No Secondary Taxonomy)

### Status
Accepted - Implemented on Day 3

### Context
Initial implementation included tags in frontmatter alongside categories. We needed to decide whether to keep tags for additional content classification.

### Decision
**Remove tags entirely** from the site taxonomy. Posts have only one category, no tags.

### Rationale

**1. Redundancy with Categories**
- Tags overlapped significantly with category names
- Example: "tech" tag in "tech" category adds no value
- Users confused by multiple classification systems

**2. AI Limitations**
- AI-generated tags were inconsistent across posts
- Same concepts tagged differently (e.g., "AI", "artificial intelligence", "machine learning")
- Requires manual curation to maintain quality

**3. SEO Dilution**
- 50+ tag pages with only 1-3 posts each (thin content)
- Spread SEO authority across too many pages
- Better to concentrate authority in 5 strong category pages

**4. User Confusion**
- Multiple paths to same content (category + tag archives)
- Unclear which taxonomy to use for navigation
- Inconsistent experience across site

**5. Maintenance Burden**
- Ongoing tag cleanup required
- Merging similar tags
- Deleting unused tags
- Time-consuming manual work

### Alternatives Considered

**Option 1: Keep Tags, Improve AI**
- Pros: More granular classification
- Cons:
  - AI still inconsistent even with better prompts
  - Ongoing maintenance required
  - SEO dilution persists

**Option 2: Manual Tagging Only**
- Pros: High-quality, consistent tags
- Cons:
  - Defeats automation purpose
  - Doesn't scale with 3 posts/day
  - Human bottleneck

**Option 3: Hybrid (Categories Required, Tags Optional)**
- Pros: Flexibility
- Cons:
  - Inconsistent application
  - Same SEO/UX issues
  - Complexity remains

### Consequences

**Positive:**
- Cleaner taxonomy (5 categories only)
- Stronger SEO (concentrated authority)
- Simpler user experience
- No tag maintenance overhead
- AI classification more reliable

**Negative:**
- Less granular content discovery
- Can't cross-reference related topics easily
- Users accustomed to tags may be disappointed

**Neutral:**
- Can add tags later if needed (not irreversible)
- Search functionality can compensate for lack of tags

---

## ADR-003: Separate contentDir for Each Language

### Status
Accepted - Implemented on Day 1

### Context
Hugo supports two approaches to multilingual content:
1. Separate content directories per language
2. Single content directory with language suffixes (e.g., `post.en.md`, `post.ko.md`)

We needed to choose the structure that best supports automated content generation.

### Decision
Use **separate contentDir for each language**:
```
content/
├── en/
├── ko/
└── ja/
```

Configuration:
```toml
[languages.en]
contentDir = "content/en"

[languages.ko]
contentDir = "content/ko"

[languages.ja]
contentDir = "content/ja"
```

### Rationale

**1. Language Isolation**
- Each language maintains independent file structure
- No risk of cross-language file conflicts
- Clear visual separation in file browser

**2. Automated Generation Simplicity**
- Scripts target specific language directories
- Example: `content/en/tech/` for English tech posts
- No need to handle `.LANG.md` naming conventions

**3. Deployment Simplicity**
- No complex multilingual file matching required
- Each language builds independently
- Clearer build logs and debugging

**4. Git Conflict Prevention**
- Multiple team members can work on different languages
- Reduces merge conflicts
- Example: One person generates EN posts, another KO posts

**5. Backup/Migration Ease**
- Easy to extract one language's content
- Example: `cp -r content/ko/ backup/`
- Language-specific backups straightforward

**6. Directory Organization**
- Matches category structure within each language
- Example: `content/en/tech/`, `content/ko/tech/`
- Intuitive file paths

### Alternatives Considered

**Option 1: Single Directory with Language Suffixes**
```
content/
└── posts/
    ├── my-article.en.md
    ├── my-article.ko.md
    └── my-article.ja.md
```

- Pros: Related translations grouped together
- Cons:
  - Requires complex file matching logic
  - AI generation scripts need to handle `.LANG.md` naming
  - Git conflicts when generating same topic in multiple languages
  - Harder to isolate language-specific issues
  - Confusing when browsing files

**Option 2: Hybrid (Separate Dirs for Some Languages)**
- Pros: Flexibility
- Cons:
  - Inconsistent structure
  - More complex to maintain
  - Confusing for developers

### Consequences

**Positive:**
- Clear separation of concerns
- Simple automated generation scripts
- Easy language-specific operations
- Reduced git conflict risk
- Intuitive file organization

**Negative:**
- Related translations not grouped in filesystem
- Harder to find all translations of a specific post
- Duplicate directory structures across languages

**Neutral:**
- Can use scripts to find related translations if needed
- Hugo handles language linking automatically in URLs

**Mitigation:**
- Use naming conventions to link related posts
- Example: `2026-01-17-digital-minimalism.md` in all language dirs
- Scripts can find translations by date/slug matching

---

## ADR-004: Hugo Static Site Generator (vs. Alternatives)

### Status
Accepted - Implemented on Day 0

### Context
Needed to choose a site generator for automated, multilingual content publishing with fast builds and easy deployment.

### Decision
Use **Hugo** static site generator with the **PaperMod** theme.

### Rationale

**1. Build Speed**
- Hugo builds 1000+ pages in under 1 second
- Critical for automated daily deployments
- Faster iteration during development

**2. Multilingual Support**
- Built-in multilingual capabilities
- Language-specific content directories
- Automatic language switcher

**3. Markdown-Based**
- Simple content format for AI generation
- Human-readable frontmatter (YAML)
- Easy to version control

**4. Static Output**
- No server-side processing required
- Deploy to any static host (Cloudflare Pages, Netlify, etc.)
- Fast page loads (no database queries)
- High security (no dynamic code execution)

**5. Theme Ecosystem**
- PaperMod theme: Clean, minimal, SEO-optimized
- Easy customization via layouts and CSS
- Active community support

**6. Cloudflare Pages Integration**
- Automatic builds on git push
- Free hosting for static sites
- Global CDN distribution
- 2-3 minute deployment time

### Alternatives Considered

**Option 1: Jekyll (Ruby-based)**
- Pros: GitHub Pages native support, mature ecosystem
- Cons:
  - Slower builds (Ruby vs. Go)
  - More complex Ruby dependency management
  - Less active development than Hugo

**Option 2: Next.js (React-based)**
- Pros: Modern framework, rich features, ISR support
- Cons:
  - Overkill for static content site
  - Slower builds than Hugo
  - More complex deployment
  - Higher hosting costs (serverless functions)

**Option 3: Gatsby (React-based)**
- Pros: Rich plugin ecosystem, GraphQL data layer
- Cons:
  - Slower builds (especially with many posts)
  - More complex configuration
  - Higher learning curve

**Option 4: 11ty (JavaScript-based)**
- Pros: Flexible templating, modern JavaScript
- Cons:
  - Smaller community than Hugo
  - Less mature multilingual support
  - Fewer themes available

### Consequences

**Positive:**
- Extremely fast builds (< 1 sec for 100+ posts)
- Simple deployment pipeline
- No server maintenance
- Excellent performance (static files)
- Strong multilingual support
- Easy for developers to modify

**Negative:**
- No dynamic features (comments, search require 3rd party)
- Limited server-side logic (all build-time)
- Go templating syntax learning curve

**Neutral:**
- Committed to Hugo ecosystem
- Theme customization requires learning Hugo templating
- Can migrate to other SSGs if needed (Markdown is portable)

---

## ADR-005: Two-Stage Content Generation (Draft + Editor)

### Status
Accepted - Implemented on Day 3

### Context
AI-generated content often needs refinement for quality, tone, and SEO. We needed to decide on a content generation pipeline.

### Decision
Use **two-stage generation** with separate Claude API calls:
1. **Draft Agent**: Generates initial content
2. **Editor Agent**: Reviews and refines the draft

### Rationale

**1. Separation of Concerns**
- Draft Agent focuses on content creation
- Editor Agent focuses on quality and polish
- Clear responsibilities reduce prompt complexity

**2. Quality Improvement**
- Editor catches issues Draft Agent misses
- Examples: AI phrases, tone inconsistencies, SEO optimization
- Second pass consistently improves output

**3. Language-Specific Optimization**
- Each language has tailored prompts
- Korean: Toss bank style (casual but professional)
- English: Medium/Substack style (conversational)
- Japanese: Natural, authentic tone

**4. Debuggability**
- Can examine draft before editing
- Identify which stage causes issues
- Easier to improve prompts iteratively

**5. Flexibility**
- Can skip editing stage if needed
- Can chain multiple editing passes
- Can use different models for each stage

### Alternatives Considered

**Option 1: Single-Stage Generation**
- Pros: Simpler, faster, cheaper (one API call)
- Cons:
  - Lower quality output
  - AI phrases more common
  - Harder to prompt for all requirements at once

**Option 2: Multi-Agent Pipeline (3+ Stages)**
- Example: Draft → Fact Check → SEO → Polish
- Pros: Highly specialized agents
- Cons:
  - Much higher cost (4+ API calls)
  - Slower generation time
  - Diminishing returns after 2 stages
  - Over-engineering for current needs

**Option 3: Human-in-the-Loop**
- Pros: Highest quality, human oversight
- Cons:
  - Defeats automation purpose
  - Doesn't scale to 3 posts/day
  - Human bottleneck

### Consequences

**Positive:**
- Higher quality content than single-stage
- Consistent tone and style
- Better SEO optimization
- Easier to debug and improve

**Negative:**
- 2x API calls = 2x cost (mitigated by better quality)
- Slower generation (6-8 sec vs. 3-4 sec)
- More complex prompt management

**Neutral:**
- Could add 3rd stage if needed
- Could skip editing for certain content types

**Cost Impact:**
- Draft: ~$0.06-0.09/post
- Editor: ~$0.06-0.09/post
- Total: ~$0.12-0.18/post (acceptable for quality gain)

---

## Summary of Decisions

| ADR | Decision | Status | Impact |
|-----|----------|--------|--------|
| 001 | Category-based taxonomy | Accepted | High - Affects navigation, SEO, UX |
| 002 | Tags removed | Accepted | Medium - Simplifies taxonomy |
| 003 | Separate contentDir | Accepted | High - Affects file structure, automation |
| 004 | Hugo static site generator | Accepted | Critical - Foundation of entire system |
| 005 | Two-stage generation | Accepted | High - Affects quality, cost, complexity |

---

## Reversibility

**Easy to Reverse:**
- ADR-002 (Tags): Can add tags back to frontmatter anytime
- ADR-005 (Two-stage): Can switch to single-stage by removing editor call

**Moderate Effort to Reverse:**
- ADR-001 (Categories): Would need to restructure content, update layouts
- ADR-003 (ContentDir): Could consolidate to single dir with filename refactoring

**Difficult to Reverse:**
- ADR-004 (Hugo): Migration to different SSG requires layout/template rewrite

---

## Lessons Learned

### What Worked Well
- Category-based taxonomy proven simple and effective
- Separate contentDir reduces complexity significantly
- Two-stage generation produces consistently better quality
- Hugo's speed enables rapid iteration

### What Could Improve
- Consider adding search functionality to compensate for no tags
- May need category adjustments as content evolves
- Could optimize two-stage generation with prompt caching

### Future Considerations
- Monitor whether 5 categories remain sufficient
- Evaluate if tags become necessary at scale (500+ posts)
- Consider 3rd generation stage for fact-checking if quality issues arise
- Explore other SSGs if Hugo limitations become problematic

---

**Last Updated**: 2026-01-17
**Next Review**: After 3 months of operation (2026-04-17)
