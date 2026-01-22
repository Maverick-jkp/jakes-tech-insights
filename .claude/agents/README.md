# Agent Documentation (Version 4.0)

**Last Updated**: 2026-01-22

---

## ⚠️ IMPORTANT CHANGE

**All agent instructions have been consolidated into `/CLAUDE.md`** (root directory)

This folder now contains **archived documentation** only. The detailed agent files (DESIGNER.md, CTO.md, QA.md, MASTER.md) are kept for historical reference but are **no longer the primary source of truth**.

---

## Why This Change?

**Problem**:
- Old system had ~1500+ lines of documentation across multiple files
- Agents skipped reading documentation despite extensive warnings
- Caused cognitive overload and workflow violations

**Solution**:
- New consolidated `/CLAUDE.md` file (~450 lines)
- Single source of truth that's easier to maintain
- System-level enforcement via git hooks
- Explicit context passing (Master tells agents what they need)

---

## For Agents: Where to Look

### Master Agent
**Read at session start**:
1. `/CLAUDE.md` (single source of truth)
2. `.claude/mistakes-log.md` (past errors)
3. `.claude/session-state.json` (current state)

### Specialized Agents (Designer, CTO, QA)
**You will receive explicit context from Master**:
- Don't read documentation files on your own
- Master will tell you what you need to know
- Focus on your task and creating a report

---

## Archive Location

Old detailed documentation (Version 3.0):
- Location: `.claude/archive/agents-v3/`
- Contains: DESIGNER.md, CTO.md, QA.md, MASTER.md, and examples
- Status: Historical reference only

---

## Quick Reference

**Primary instructions**: `/CLAUDE.md` (root of project)
**Session state**: `.claude/session-state.json`
**Mistakes log**: `.claude/mistakes-log.md`
**Report templates**: `.claude/templates/`

---

**If you're an agent and confused about what to do, read `/CLAUDE.md` first.**
