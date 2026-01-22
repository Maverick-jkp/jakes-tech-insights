# Week 1: CLAUDE.md Progressive Disclosure Refactor

**Date**: 2026-01-23
**Goal**: 957줄 → 200줄 entry point + 7 focused documents
**Pattern**: 350k LOC case 기반 (검증된 production pattern)

---

## 📊 Current State Analysis

```
CLAUDE.md:          957줄 (everything mixed)
WORKFLOW.md:        582줄 (multi-agent rules)
mistakes-log.md:    215줄 (error log)
session-state.json: 536줄 (growing indefinitely)
────────────────────────────
Total: 2,290줄 loaded every session
```

**문제점**:
- Claude가 안 읽음 (500줄 권장, 957줄은 과다)
- Progressive disclosure 없음
- 모든 컨텍스트가 항상 로딩됨

---

## 🎯 Target Structure (350k Case Pattern)

```
CLAUDE.md (200줄)                    ← Entry point only
  │
  ├─ Quick links to other docs
  ├─ Essential commands only
  └─ "Read X.md for details"

.claude/docs/                        ← On-demand loading
  ├─ architecture.md                 (Content pipeline 상세)
  ├─ commands.md                     (All command reference)
  ├─ development.md                  (Common tasks)
  ├─ troubleshooting.md              (문제 해결)
  ├─ quality-standards.md            (Content quality)
  ├─ design-system.md                (UI/UX)
  └─ security.md                     (API keys, incidents)

.claude/skills/                      ← Week 2 (Task-based loading)
  ├─ content-generation/SKILL.md
  ├─ quality-validation/SKILL.md
  ├─ hugo-operations/SKILL.md
  └─ keyword-curation/SKILL.md
```

---

## 📝 New CLAUDE.md Structure (200줄)

### Section 1: Mandatory Reading (30줄)
```markdown
# CLAUDE.md

## ⚠️ MANDATORY FIRST ACTION

**Before ANY work, read these in order:**
1. CLAUDE.md (this file) - Overview
2. .claude/docs/[relevant].md - Details on-demand
3. .claude/session-state.json - Current state
4. .claude/mistakes-log.md - Past errors

## 🔴 PRE-ACTION VERIFICATION

Before fixing ANY issue:
1. git status && git diff
2. git fetch origin && git show origin/main:path/to/file
3. ls -la .env
4. Verify problem actually exists
```

### Section 2: Project Overview (40줄)
```markdown
## Project Overview

**Jake's Tech Insights** - AI-powered multilingual blog
- Tech: Hugo, Python 3.x, Claude API (Sonnet 4.5)
- Languages: EN, KO, JA
- Deployment: Cloudflare Pages
- Automation: 3x daily (6 AM, 12 PM, 6 PM KST)

**Architecture**: See `.claude/docs/architecture.md`
**Commands**: See `.claude/docs/commands.md`
```

### Section 3: Quick Commands (60줄)
```markdown
## Quick Commands

### Hugo (CRITICAL: Use full path)
```bash
/opt/homebrew/bin/hugo server -D
/opt/homebrew/bin/hugo --minify
```

### Python
```bash
pip install -r requirements.txt
python scripts/generate_posts.py --count 3
pytest
```

### Git
```bash
git status
git commit -m "..."
```

**Full reference**: `.claude/docs/commands.md`
```

### Section 4: File Structure (30줄)
```markdown
## Key Files

```
content/{en,ko,ja}/          # Blog posts
scripts/                     # Python automation
layouts/                     # Hugo templates
.claude/
  ├─ docs/                   # Detailed docs (on-demand)
  ├─ skills/                 # Task-specific (Week 2)
  └─ sessions/               # Per-session state (Week 4)
```

**Details**: `.claude/docs/architecture.md`
```

### Section 5: Documentation Index (30줄)
```markdown
## Documentation

**Read on-demand based on your task:**

| Task | Read |
|------|------|
| Content generation | `.claude/docs/architecture.md` |
| Hugo troubleshooting | `.claude/docs/troubleshooting.md` |
| Quality issues | `.claude/docs/quality-standards.md` |
| Design changes | `.claude/docs/design-system.md` |
| Common tasks | `.claude/docs/development.md` |
| All commands | `.claude/docs/commands.md` |
| Security | `.claude/docs/security.md` |
```

### Section 6: Important Links (10줄)
```markdown
## Links

- Live: https://jakes-tech-insights.pages.dev
- Repo: https://github.com/Maverick-jkp/jakes-tech-insights
- Hugo: https://gohugo.io/documentation/
- Claude API: https://docs.anthropic.com/en/api/
```

**Total: ~200줄**

---

## 📄 Extracted Documents (7 files)

### 1. `.claude/docs/architecture.md` (~150줄)

**Content from current CLAUDE.md**:
- System Architecture (lines 190-280)
- Content Generation Flow
- Topic Queue State Machine
- Draft/Editor Agent details

**Why separate**:
- Only needed when working on content pipeline
- Technical details not needed for simple tasks

### 2. `.claude/docs/commands.md` (~120줄)

**Content**:
- Hugo Commands (current lines 50-80)
- Python Environment (lines 81-95)
- Testing (lines 96-110)
- Content Generation Pipeline (lines 111-140)
- All command reference consolidated

**Why separate**:
- Reference material
- Look up as needed
- Not needed in every session

### 3. `.claude/docs/development.md` (~200줄)

**Content**:
- Common Development Tasks (current lines 350-550)
  - Generate content for keyword
  - Fix stuck topics
  - Test locally
  - Update system prompts
  - Add new category
  - Run full pipeline

**Why separate**:
- Task-specific guides
- Read only when doing that task

### 4. `.claude/docs/troubleshooting.md` (~150줄)

**Content**:
- Troubleshooting section (current lines 550-700)
  - Hugo not found
  - API key issues
  - Queue stuck
  - Quality gate failures
  - GitHub Actions delays
  - Hugo build errors

**Why separate**:
- Only needed when things break
- Reference material

### 5. `.claude/docs/quality-standards.md` (~100줄)

**Content**:
- Content Quality Standards (current lines 280-350)
  - Word count requirements
  - AI phrase blacklist
  - SEO requirements
  - Image requirements

**Why separate**:
- Only needed for content generation
- Reference for quality checks

### 6. `.claude/docs/design-system.md` (~80줄)

**Content**:
- Design System (current lines 700-780)
  - Colors
  - Typography
  - Breakpoints
  - Grid system

**Why separate**:
- Only needed for UI/design work
- Not needed for backend/automation

### 7. `.claude/docs/security.md` (~60줄)

**Content**:
- Security section (current lines 850-910)
  - API Keys storage
  - Pre-commit validation
  - Past incidents

**Why separate**:
- Sensitive information
- Reference only when needed

---

## 🔄 Migration Strategy

### Step 1: Create directory structure
```bash
mkdir -p .claude/docs
```

### Step 2: Extract documents (순서대로)

1. **architecture.md** - Copy lines 190-280 from CLAUDE.md
2. **commands.md** - Copy lines 50-140 from CLAUDE.md
3. **development.md** - Copy lines 350-550 from CLAUDE.md
4. **troubleshooting.md** - Copy lines 550-700 from CLAUDE.md
5. **quality-standards.md** - Copy lines 280-350 from CLAUDE.md
6. **design-system.md** - Copy lines 700-780 from CLAUDE.md
7. **security.md** - Copy lines 850-910 from CLAUDE.md

### Step 3: Create new CLAUDE.md

- Use template above (200줄)
- Link to extracted docs
- Keep only essentials

### Step 4: Backup old files

```bash
mkdir -p .claude/archive/v5.0-before-refactor/
cp CLAUDE.md .claude/archive/v5.0-before-refactor/
cp .claude/WORKFLOW.md .claude/archive/v5.0-before-refactor/
```

### Step 5: Update session-state.json

```json
{
  "documentation_structure": {
    "version": "6.0",
    "date": "2026-01-23",
    "pattern": "Progressive disclosure (350k LOC case)",
    "entry_point": "CLAUDE.md (200 lines)",
    "on_demand_docs": ".claude/docs/ (7 files)"
  }
}
```

---

## ✅ Success Criteria

**Before (Current)**:
- CLAUDE.md: 957줄
- Claude가 안 읽음
- 모든 컨텍스트 항상 로딩
- git CLI 없다는 헛소리

**After (Week 1)**:
- CLAUDE.md: 200줄 ✅
- .claude/docs/: 7 files (860줄 total)
- Claude가 실제로 읽음 ✅
- On-demand loading ✅
- 필요한 문서만 읽으라고 링크 제공 ✅

**측정**:
- Line count: `wc -l CLAUDE.md` = 200 이하
- Claude가 "Read .claude/docs/X.md" 지시를 따름
- 간단한 작업에서 불필요한 컨텍스트 로딩 없음

---

## 🚀 Implementation Order

### Task 1: Create docs directory & backup (5분)
```bash
mkdir -p .claude/docs
mkdir -p .claude/archive/v5.0-before-refactor/
cp CLAUDE.md .claude/archive/v5.0-before-refactor/
```

### Task 2: Extract architecture.md (30분)
- Copy content pipeline details
- Add frontmatter
- Test readability

### Task 3: Extract commands.md (20분)
- Consolidate all commands
- Organize by category

### Task 4: Extract development.md (40분)
- All common tasks
- Step-by-step guides

### Task 5: Extract troubleshooting.md (30분)
- All error solutions
- Organized by problem type

### Task 6: Extract quality-standards.md (20분)
- Content quality criteria
- Validation rules

### Task 7: Extract design-system.md (20분)
- UI/UX guidelines
- Color/typography specs

### Task 8: Extract security.md (15분)
- API key management
- Security incidents

### Task 9: Create new CLAUDE.md (60분)
- Use 200-line template
- Link to all docs
- Essential commands only

### Task 10: Test & validate (30분)
- Check line counts
- Verify links work
- Test Claude reading comprehension

**Total: ~4-5 hours**

---

## 📊 Expected Results

### Context Loading Comparison

**Before**:
```
Simple task (git status):
- Loads: CLAUDE.md (957줄)
- Total: 957줄

Medium task (generate content):
- Loads: CLAUDE.md (957줄) + WORKFLOW.md (582줄)
- Total: 1,539줄

Complex task (multi-agent):
- Loads: All files (2,290줄)
- Total: 2,290줄
```

**After Week 1**:
```
Simple task (git status):
- Loads: CLAUDE.md (200줄)
- Total: 200줄 (79% reduction ✅)

Medium task (generate content):
- Loads: CLAUDE.md (200줄) + architecture.md (150줄) + commands.md (120줄)
- Total: 470줄 (69% reduction ✅)

Complex task (multi-agent):
- Loads: CLAUDE.md (200줄) + relevant docs (~400줄)
- Total: 600줄 (74% reduction ✅)
```

---

## 🔧 Testing Plan

### Test 1: Simple task
```
User: "Run git status"
Expected: Claude reads CLAUDE.md (200줄) only
Actual: [measure]
```

### Test 2: Content generation
```
User: "Generate 1 post"
Expected: Claude reads CLAUDE.md + architecture.md
Actual: [measure]
```

### Test 3: Troubleshooting
```
User: "Hugo build failing"
Expected: Claude reads CLAUDE.md, then asks to read troubleshooting.md
Actual: [measure]
```

### Test 4: No more hallucinations
```
User: "Check API key"
Expected: Claude reads security.md, follows documented procedure
Actual: Should NOT claim "git CLI missing" or "API key missing"
```

---

## 📈 Week 1 Deliverables

1. ✅ `.claude/docs/` directory with 7 files
2. ✅ New CLAUDE.md (200줄)
3. ✅ Backup of old files in `.claude/archive/v5.0-before-refactor/`
4. ✅ Updated session-state.json (documentation v6.0)
5. ✅ Test results documented
6. ✅ Week 1 completion report

---

## 🔜 Preview: Week 2-4

**Week 2**: Extract Skills (Anthropic standard)
- `.claude/skills/content-generation/SKILL.md`
- `.claude/skills/quality-validation/SKILL.md`
- `.claude/skills/hugo-operations/SKILL.md`
- `.claude/skills/keyword-curation/SKILL.md`

**Week 3**: Separate Agent files (if needed)
- `.claude/agents/master.md`
- `.claude/agents/content.md`
- `.claude/agents/qa.md`

**Week 4**: Session State refactor
- `.claude/sessions/2026-01-23/state.json`
- Auto-archiving after 7 days

---

**Ready to start Week 1 implementation?**
**Estimated time: 4-5 hours**
**First task: Create docs directory & backup (5분)**
