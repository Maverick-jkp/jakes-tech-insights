# CLAUDE.md

**Version**: 6.0 - Progressive Disclosure
**Last Updated**: 2026-01-23
**Pattern**: 350k LOC case (production-proven)

---

## ⚠️ MANDATORY FIRST ACTION

**Before ANY work, read these in order:**

1. **CLAUDE.md** (this file) - Overview & essentials
2. **`.claude/docs/[relevant].md`** - Details on-demand (see index below)
3. **`.claude/session-state.json`** - Current project state
4. **`.claude/mistakes-log.md`** - Past errors to avoid

---

## 🔴 PRE-ACTION VERIFICATION CHECKLIST

**Before attempting to "fix" ANY reported issue:**

```bash
# Step 1: Verify problem exists locally
git status
git diff

# Step 2: Check if already fixed in remote repository
git fetch origin
git show origin/main:path/to/file | grep "search-term"

# Step 3: Verify environment files exist
ls -la .env
ls -la .git/config

# Step 4: If issue involves environment variables, verify they exist
grep "VARIABLE_NAME" .env

# Step 5: Check documented procedures FIRST
# Example: .claude/docs/commands.md line 20 shows how to load .env
# DO NOT improvise - follow documented method
```

**CRITICAL RULES**:
1. ❌ **NEVER assume** user's report means issue currently exists - verify first
2. ❌ **NEVER improvise** solutions when documented procedures exist
3. ❌ **NEVER claim** files/keys/tools are missing without checking
4. ✅ **ALWAYS verify** current state before attempting any fix
5. ✅ **ALWAYS follow** documented procedures exactly as written
6. ✅ **ALWAYS check** if issue already resolved in previous session

**If verification shows issue is already fixed**: Report findings, do NOT redo the work.

---

## Project Overview

**Jake's Tech Insights** - AI-powered multilingual blog system

- **Tech Stack**: Hugo, Python 3.x, Claude API (Sonnet 4.5), GitHub Actions
- **Languages**: English (EN), Korean (KO), Japanese (JA)
- **Deployment**: Cloudflare Pages (https://jakes-tech-insights.pages.dev)
- **Automation**: Daily content generation (configured via GitHub Actions schedule)

---

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

---

## Key Files

```
content/{en,ko,ja}/          # Blog posts (Markdown)
scripts/                     # Python automation
layouts/                     # Hugo templates
data/topics_queue.json       # Topic queue (state machine)
.claude/
  ├─ docs/                   # Detailed docs (on-demand)
  ├─ skills/                 # Task-specific (Week 2)
  └─ sessions/               # Per-session state (Week 4)
```

**Details**: `.claude/docs/architecture.md`

---

## 📚 Documentation Index

**Read on-demand based on your task:**

| Task | Read |
|------|------|
| Content pipeline details | `.claude/docs/architecture.md` |
| All command reference | `.claude/docs/commands.md` |
| Step-by-step guides | `.claude/docs/development.md` |
| Error solutions | `.claude/docs/troubleshooting.md` |
| Quality criteria | `.claude/docs/quality-standards.md` |
| UI/UX guidelines | `.claude/docs/design-system.md` |
| Security & costs | `.claude/docs/security.md` |

**Why on-demand loading?**
- Each doc is 60-200 lines (focused)
- Only load what you need
- Prevents context overload
- Based on 350k LOC production case (30-40% productivity gain)

---

## Common Tasks Quick Reference

### 1. Generate content
```bash
python scripts/generate_posts.py --count 3
```
**Details**: `.claude/docs/development.md` → Section 1

### 2. Fix stuck topics
```bash
python scripts/topic_queue.py cleanup 24
```
**Details**: `.claude/docs/development.md` → Section 2

### 3. Test locally
```bash
/opt/homebrew/bin/hugo server -D
```
**Details**: `.claude/docs/development.md` → Section 3

### 4. Troubleshoot Hugo
**Read**: `.claude/docs/troubleshooting.md` → "Hugo Not Found"

### 5. Troubleshoot API keys
**Read**: `.claude/docs/troubleshooting.md` → "API Key Issues"

---

## System Architecture (Overview)

```
Topic Queue → Draft Agent → Editor Agent → Quality Gate → AI Review → Git Commit → GitHub Actions → Cloudflare Deploy
```

**Full diagram**: `.claude/docs/architecture.md`

---

## Content Quality (Quick Reference)

| Language | Word Count | Structure |
|----------|------------|-----------|
| English | 800-2,000 | 3-4 sections |
| Korean | 800-2,000 | 3-4 sections |
| Japanese | 3,000-7,500 chars | 3-4 sections |

**Full standards**: `.claude/docs/quality-standards.md`

---

## Important Links

- **Live Site**: https://jakes-tech-insights.pages.dev
- **GitHub**: https://github.com/Maverick-jkp/jakes-tech-insights
- **Hugo Docs**: https://gohugo.io/documentation/
- **Claude API**: https://docs.anthropic.com/en/api/

---

## For Larger Projects

**Current scale**: < 10k LOC
**Pattern**: Progressive disclosure (proven at 350k LOC)
**Future**: See `.claude/real-world-cases.md` for scaling patterns

---

## Version History

- **6.0** (2026-01-23): Progressive disclosure refactor (957 → 200 lines)
- **5.0** (2026-01-23): Technical architecture split
- **4.0** (2026-01-22): Multi-agent workflow consolidation
- **3.0** (2026-01-20): Session checklists added

---

**This is the entry point. Read detailed docs on-demand.**
**Based on production-proven 350k LOC case (30-40% productivity gain).**
