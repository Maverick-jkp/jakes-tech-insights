# Quality Standards

## Overview

Jake's Tech Insights maintains rigorous quality standards for AI-generated content to ensure authenticity, value, and engagement. This document outlines the content quality strategy, AI content risks, quality assurance methods, and writing style guidelines.

## Content Quality Strategy

### Core Principles

1. **Authenticity Over Perfection**: Content should feel human-written, not AI-polished
2. **Value Over Volume**: Each post must provide actionable insights
3. **Engagement Over Length**: Quality of ideas, not word count padding
4. **Accuracy Over Speed**: Fact-check critical claims, even if it slows generation

### Quality Metrics

**Quantitative Standards**:
- Word count: 800-1,600 words (EN/KO), 3,000-5,000 characters (JA)
- Reading time: 3-4 minutes ideal
- Headings: 3-5 H2 sections minimum
- External links: 2+ references to authoritative sources
- Keyword density: 5-7 mentions (natural, not forced)

**Qualitative Standards**:
- Authenticity: Natural human tone, no AI phrases
- Value: Practical, actionable insights (not generic advice)
- Engagement: Interesting structure, varied paragraph length
- Technical Accuracy: Correct facts, current information
- SEO Quality: Natural keyword integration, meta optimization

## AI Content Risks

### Common AI Content Problems

#### 1. Generic Advice
**Problem**: AI tends to provide surface-level, obvious advice.

**Example (Bad)**:
> "Communication is important in the workplace. Make sure to listen to your colleagues and share your ideas clearly."

**Example (Good)**:
> "When presenting to skeptical stakeholders, lead with the one metric they care about most. At Amazon, this meant starting every pitch with 'customer pain points' before discussing features."

**Mitigation**:
- Require specific examples with company names
- Request "counter-intuitive" or "non-obvious" insights
- Ask for "what most people get wrong about X"

#### 2. AI Phrase Overuse
**Problem**: AI uses predictable filler phrases.

**Blacklisted English Phrases**:
- "revolutionary"
- "game-changer"
- "cutting-edge"
- "it's important to note"
- "in today's digital age"
- "seamless integration"
- "robust solution"
- "leverage synergies"

**Blacklisted Korean Phrases**:
- "물론" (of course)
- "혁신적" (innovative)
- "게임체인저" (game-changer)
- "결론적으로" (in conclusion)
- "다양한" (various)

**Blacklisted Japanese Phrases**:
- "もちろん" (of course)
- "革新的" (innovative)
- "ゲームチェンジャー" (game-changer)
- "結論として" (in conclusion)

**Mitigation**:
- Quality gate detects these phrases (warnings)
- Editor Agent instructed to remove them
- Manual review if excessive warnings

#### 3. Lack of Specificity
**Problem**: AI defaults to "many companies..." or "experts say..."

**Example (Bad)**:
> "Many companies have found success with remote work policies."

**Example (Good)**:
> "GitLab's 1,300+ remote employees reported 18% higher productivity than their office-based competitors, according to their 2023 remote work report."

**Mitigation**:
- Require named companies/studies in prompts
- Ask for "specific numbers" and "recent data"
- Penalize vague statements in AI Review

#### 4. Overly Balanced Tone
**Problem**: AI tries to present all sides, resulting in bland conclusions.

**Example (Bad)**:
> "Both approaches have their merits. The best choice depends on your specific situation."

**Example (Good)**:
> "For teams under 10 people, async standup is a waste of time. Just talk to each other. Save the ritual for when you're actually too big to keep track."

**Mitigation**:
- Encourage opinionated takes in prompts
- Request "strong point of view"
- Ask "what do you disagree with conventional wisdom about?"

#### 5. No Failure Cases
**Problem**: AI focuses on success stories, ignoring when things don't work.

**Example (Missing)**:
> No discussion of when a strategy fails or who shouldn't use it.

**Example (Good)**:
> "## When Remote Work Doesn't Work
>
> If your team relies on rapid iteration (design, sales), forced async kills momentum. Figma didn't go remote-first for a reason."

**Mitigation**:
- Require "failure case" or "when X doesn't work" section
- Ask "who should NOT do this?"
- Include "common mistakes" in every article

## Quality Assurance Methods

### 1. Automated Quality Gate

**File**: `scripts/quality_gate.py`

**Checks**:
- ✅ Word count in range (800-1,600 words)
- ✅ Frontmatter completeness (title, date, category, description)
- ⚠️ AI phrase detection (warnings, not failures)
- ✅ Meta description length (120-160 chars)
- ✅ Title length (50-60 chars)

**Pass/Fail Criteria**:
- FAIL: Word count out of range, missing frontmatter
- WARN: AI phrases detected, SEO suggestions
- PASS: All critical checks passed

**Usage**:
```bash
# Standard mode (warnings don't fail)
python scripts/quality_gate.py

# Strict mode (warnings become failures)
python scripts/quality_gate.py --strict
```

### 2. AI Self-Review

**File**: `scripts/ai_reviewer.py`

**Scoring Criteria** (1-10 scale):

1. **Authenticity (1-10)**
   - Natural human tone
   - No AI phrases or generic language
   - Personal voice and conviction

2. **Value (1-10)**
   - Practical, actionable insights
   - Specific examples with names/numbers
   - Non-obvious advice

3. **Engagement (1-10)**
   - Interesting structure and flow
   - Varied paragraph length
   - Compelling opening and conclusion

4. **Technical Accuracy (1-10)**
   - Correct facts and current information
   - Proper terminology
   - No misleading claims

5. **SEO Quality (1-10)**
   - Natural keyword integration
   - Good meta description and title
   - Proper heading structure

**Recommendations**:
- **APPROVE**: Average score ≥ 8.0 → Publish
- **REVISE**: Average score 6.0-7.9 → Edit and regenerate
- **REJECT**: Average score < 6.0 → Discard and try new topic

**Usage**:
```bash
# Review all generated posts
python scripts/ai_reviewer.py

# Review specific post
python scripts/ai_reviewer.py --file content/en/tech/2026-01-17-my-post.md
```

### 3. Manual Spot Checks

**Frequency**: 10% of posts (random sampling)

**Focus Areas**:
- Fact-check specific claims (companies, statistics)
- Verify links are relevant and authoritative
- Check for plagiarism (Google unique phrases)
- Assess overall coherence and value

**Red Flags**:
- Contradictory statements within post
- Outdated information (pre-2020 examples)
- Broken or irrelevant links
- Copied content from other sources

## Writing Style Guidelines

### Tone by Language

**English**:
- **Style**: Medium/Substack (conversational, opinionated)
- **Reference**: Paul Graham essays, Stratechery
- **Voice**: First-person insights, confident takes
- **Length**: 900-1,100 words ideal

**Korean (한국어)**:
- **Style**: Toss bank blog (casual but professional)
- **Reference**: Toss, 29CM blogs
- **Voice**: Friendly, approachable, slightly informal
- **Length**: 900-1,100 words ideal

**Japanese (日本語)**:
- **Style**: Natural, authentic tone
- **Reference**: note.com articles
- **Voice**: Polite but not stiff, informative
- **Length**: 3,000-4,500 characters ideal

### Structural Guidelines

**Opening (First 2-3 Paragraphs)**:
- Start with a specific problem or surprising fact
- NO generic intros ("In today's world...")
- Hook reader with counter-intuitive angle

**Example (Bad)**:
> "Productivity is important for modern professionals. In this article, we'll explore various productivity techniques."

**Example (Good)**:
> "I deleted Slack from my phone and my team's output doubled. Not because I'm a bottleneck (I wish), but because async requests stopped derailing everyone's deep work."

**Body (3-5 H2 Sections)**:
- Each section: 200-300 words
- Start with a bolded key insight
- Include specific example or data point
- End with actionable takeaway

**Structure Template**:
```markdown
## [Section Title: Specific Problem/Topic]

**Key Insight**: [One sentence summary]

[2-3 paragraphs with specific examples]

**Actionable Takeaway**: [What reader should do]
```

**Failure Case Section (Required)**:
- Title: "When [Topic] Doesn't Work" or "Common Mistakes"
- 100-200 words
- Specific scenarios where advice fails
- Who should NOT follow this approach

**Conclusion (Final 2-3 Paragraphs)**:
- Restate core insight with new angle
- NO generic summary ("In conclusion...")
- End with thought-provoking question or call-to-action

### Paragraph Guidelines

**Variety in Length**:
- Mix short (1-2 sentences) and long (4-5 sentences) paragraphs
- Short paragraphs for emphasis
- Long paragraphs for explanation

**Example**:
```markdown
[Long paragraph with context and explanation...]

But here's the thing most people miss.

[Short paragraph with key insight.]

[Long paragraph with supporting details...]
```

**Sentence Structure**:
- Vary sentence length (5-25 words)
- Use active voice (90%+ of sentences)
- Start some sentences with conjunctions (But, And, So) for flow

### Link Guidelines

**Minimum Requirements**:
- 2+ external links per post
- Links to authoritative sources (company blogs, research papers, reputable news)
- Avoid: Wikipedia (too generic), random blogs (low authority)

**Good Link Targets**:
- Company official blogs (e.g., GitLab blog, Toss blog)
- Research papers (academic journals, industry reports)
- Major news outlets (NYT, WSJ, TechCrunch for tech topics)
- Primary sources (government data, company financials)

**Link Placement**:
- Inline with specific claims (not at end)
- Use descriptive anchor text (not "click here")

**Example**:
```markdown
[GitLab's 2023 remote work report](https://about.gitlab.com/...) found that 1,300+ remote employees...
```

## Human-Touch Strategies

### 1. Hooking Strategy

**Problem-Driven Openings** (not generic intros):

**Bad**:
> "Digital minimalism is becoming increasingly popular in today's connected world."

**Good**:
> "I spent $4,000 on productivity apps last year. Then I deleted all of them and got more done."

**Implementation**:
- Start with specific personal anecdote or statistic
- Frame as problem reader likely experiences
- Counter-intuitive angle preferred

### 2. Real Examples

**Require Named Companies/Studies**:

**Bad**:
> "Many companies have adopted remote work policies."

**Good**:
> "Shopify gave all 7,000 employees $1,000 to improve home offices. Result: 25% fewer Zoom meetings."

**Implementation**:
- Prompt must request "name 2-3 specific companies"
- Include recent data (2020+)
- Verify facts during manual spot checks

### 3. Failure Cases

**Dedicated "When X Doesn't Work" Section**:

**Required Elements**:
- Specific scenarios where advice fails
- Who should NOT use this approach
- Common mistakes to avoid

**Example**:
```markdown
## When Async Communication Fails

If you're launching a product in 2 weeks, async kills you. Figma's design team stayed in-office during launch sprints for a reason—rapid iteration needs real-time feedback.

Don't go async if:
- Team under 10 people (just talk)
- Crisis mode (ship fast > document perfectly)
- Creative brainstorming (riffing beats threading)
```

### 4. Authenticity Markers

**Show Vulnerability and Limitations**:

**Phrases to Include**:
- "In my experience..."
- "I've tried X and failed because..."
- "This only works if..."
- "What I got wrong about..."

**Example**:
> "I used to think morning routines were the secret to productivity. Then I had a kid. Turns out, systems that require perfect conditions are fragile systems."

**Implementation**:
- Draft Agent prompted to include personal perspective
- Editor Agent adds vulnerability markers
- Avoid: "one weird trick", "secret sauce", "guaranteed"

### 5. Decision-Stage Focus

**"What to Avoid" as Much as "What to Do"**:

**Balance Positive and Negative Advice**:

**Example Structure**:
```markdown
## What to Do
- [Actionable advice with example]

## What to Avoid
- [Common mistake with consequences]
```

**Implementation**:
- Every "do this" paired with "don't do that"
- Explain WHY something doesn't work
- Include consequences of common mistakes

## Content Requirements

### Frontmatter Standards

**Minimum Required Fields**:
```yaml
---
title: "SEO-friendly title (50-60 chars)"
date: 2026-01-17T12:00:00+09:00
draft: false
categories: ["tech"]
description: "Meta description (120-160 chars)"
---
```

**Title Guidelines**:
- 50-60 characters (optimal for search results)
- Include primary keyword
- Avoid clickbait (no "you won't believe...")
- Be specific, not generic

**Good Titles**:
- "Why GitLab's Remote Work Failed for Design Teams" (56 chars)
- "Toss Bank's Growth Hack: Remove Features, Not Add Them" (58 chars)

**Bad Titles**:
- "10 Amazing Productivity Tips You Need to Know" (too generic)
- "This One Weird Trick Will Change Your Life" (clickbait)

**Description Guidelines**:
- 120-160 characters (optimal for search snippets)
- Include primary keyword
- Compelling but accurate
- Complete sentence(s)

**Good Descriptions**:
> "GitLab's 1,300 remote employees reported 18% higher productivity, but their design team stayed in-office. Here's why async doesn't work for everyone." (155 chars)

**Bad Descriptions**:
> "Learn about remote work and productivity tips for your team." (too vague, no specifics)

### SEO Standards

**Keyword Integration**:
- Primary keyword: 5-7 mentions (natural placement)
- Title: Include primary keyword
- First paragraph: Include primary keyword
- H2 headings: Include keyword variations
- Meta description: Include primary keyword

**Heading Structure**:
- H1: Post title (auto-generated by Hugo)
- H2: 3-5 main sections
- H3: Subsections within H2 (optional)
- No H4-H6 (unnecessary complexity)

**Internal Linking** (Future):
- Link to related posts within site
- Use descriptive anchor text
- 2-3 internal links per post ideal

## Quality Improvement Workflow

### When Post Fails Quality Gate

**Step 1: Identify Failure Reason**
- Word count too low/high?
- Missing frontmatter?
- Excessive AI phrases?

**Step 2: Manual Fix or Regenerate**
- Minor issues (frontmatter): Manual fix
- Major issues (content quality): Regenerate

**Step 3: Rerun Quality Gate**
```bash
python scripts/quality_gate.py
```

### When AI Review Recommends REVISE

**Step 1: Read AI Review Report**
```bash
cat ai_review_report.json
```

**Step 2: Address Specific Issues**
- Low Authenticity: Remove AI phrases, add personal voice
- Low Value: Add specific examples, remove generic advice
- Low Engagement: Restructure, vary paragraph length
- Low Technical Accuracy: Fact-check, update outdated info
- Low SEO: Improve keyword usage, fix meta description

**Step 3: Regenerate with Updated Prompts**
- Adjust Draft Agent prompt based on feedback
- Emphasize areas where score was low

### When AI Review Recommends REJECT

**Step 1: Analyze Root Cause**
- Was topic too generic?
- Were prompts unclear?
- Did generation truncate?

**Step 2: Try Different Topic**
- Don't force bad topics
- Move to next item in queue

**Step 3: Improve Prompts (If Pattern)**
- If multiple rejects on same category, update prompts
- Add more specific instructions
- Include better examples

## Continuous Improvement

### Weekly Review Process

**Every Sunday**:
1. Review past week's posts (7 × 3 = 21 posts)
2. Identify patterns in quality issues
3. Update prompts if needed
4. Adjust quality gate thresholds if too strict/lenient

### Monthly Analysis

**Every Month**:
1. Analyze top 10 performing posts (traffic, engagement)
2. Identify common elements (topics, structure, tone)
3. Incorporate learnings into prompts
4. Update blacklist phrases if new patterns emerge

### Metrics to Track

**Content Metrics**:
- Average word count
- AI phrase detection rate
- Quality gate pass rate
- AI Review average score

**Engagement Metrics** (requires Google Analytics):
- Bounce rate
- Average time on page
- Pages per session
- Scroll depth

**SEO Metrics** (requires Google Search Console):
- Impressions
- Click-through rate
- Average position
- Top keywords

## References

- ChatGPT Human-Touch Strategies: Internal conversation (2026-01-17)
- Paul Graham Essays: http://www.paulgraham.com/articles.html
- Toss Blog (Korean): https://blog.toss.im/
- Stratechery (Ben Thompson): https://stratechery.com/

---

**Last Updated**: 2026-01-17
**Next Review**: 2026-02-17 (monthly)
