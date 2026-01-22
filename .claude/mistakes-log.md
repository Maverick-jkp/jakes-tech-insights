# Agent Mistakes Log

## Purpose
This file records every workflow violation to prevent repeating past mistakes.
All agents MUST review this file at session start.

---

## 2026-01-22: Designer committed without creating report

**What happened**: Designer agent completed homepage layout redesign but committed changes directly without creating a work report first.

**Rule broken**:
- STEP 3: Create Work Report FIRST
- STEP 4: NEVER commit or push

**Impact**:
- Workflow disrupted
- No documentation of changes
- User had to remind about protocol
- Time wasted on process correction

**Root cause**:
1. Did not read DESIGNER.md before starting work
2. Skipped documentation review step
3. Assumed "good work = can commit immediately"
4. Confused with Master's authority (only Master commits)

**Prevention measures taken**:
1. Added CRITICAL WORKFLOW RULES section to all agent docs
2. Added ASCII warning boxes for visual emphasis
3. Added session start checklist (7 steps)
4. Created this mistakes-log.md file
5. Fixed contradictory rules in DESIGNER.md
6. Removed duplicate sections to reduce cognitive load

**Lesson learned**:
- Rules existed but were not visually prominent
- Need checklist format, not just text instructions
- Specialized agents (Designer/CTO/QA) NEVER commit
- Only Master has commit authority

---

## How to Use This File

**Before starting ANY work**:
1. Read this file completely
2. Check if your planned action appears in past mistakes
3. If similar situation exists, follow prevention measures
4. If uncertain, ASK first, don't proceed

**After making a mistake**:
1. Document it here immediately
2. Explain what happened, why, and impact
3. Identify root cause
4. List prevention measures
5. Commit this file update

---

## 2026-01-22: System Overhaul - Documentation Consolidation

**What happened**: After web research on AI agent best practices, discovered that our multi-session collaboration kept failing despite extensive documentation (~1500+ lines).

**Rule violations pattern**:
- Designer committed without report (2026-01-22)
- Agents repeatedly skipped "Before Work" sections
- Session start checklists added but compliance uncertain
- Parallel sessions caused incompatible work

**Root cause analysis**:
1. **Cognitive overload**: ~1500+ lines of documentation too long (industry standard: < 500 lines)
2. **Documentation-based enforcement**: Relying on agents to voluntarily read files (unreliable)
3. **No persistent memory**: Each session starts fresh, agents forget context
4. **Parallel sessions**: Without shared memory, multiple agents produce incompatible work

**Industry best practices research findings**:
- Claude Memory Tool: 39% performance improvement with persistent memory
- CLAUDE.md pattern: Single file < 500 lines, auto-loaded by system
- Sequential workflow: Master orchestrates one agent at a time
- Explicit context passing: Master tells agents what they need (don't rely on reading)

**Major system changes implemented**:
1. ✅ Created `/CLAUDE.md` (450 lines) - single source of truth
2. ✅ Archived old agent docs (~1500 lines) to `.claude/archive/agents-v3/`
3. ✅ Established sequential workflow pattern (Master → Agent → Master)
4. ✅ Created `.claude/session-state.json` for session continuity
5. ✅ Added git pre-commit hook (warns if no reports exist)
6. ✅ Defined explicit context passing protocol

**What changed for agents**:

**Master Agent**:
- MUST read: `/CLAUDE.md`, `.claude/mistakes-log.md`, `.claude/session-state.json`
- MUST pass explicit context to subagents (don't rely on them reading)
- MUST orchestrate sequentially (one agent at a time)
- ONLY agent with commit authority

**Specialized Agents (Designer/CTO/QA)**:
- Will RECEIVE explicit context from Master (don't read docs independently)
- Focus on assigned task only
- Create report and return to Master
- NEVER commit or push

**Lesson learned**:
- **Documentation length matters**: 1500 lines → 450 lines
- **System enforcement > agent discipline**: Git hooks + explicit context > hoping agents read
- **Sequential > parallel**: Without shared memory, sequential prevents conflicts
- **Less is more**: Consolidation improves compliance

**Success metrics** (30-day evaluation):
- Target: 100% report creation compliance
- Target: Zero unauthorized commits
- Target: 100% sequential workflow adherence
- Current: System just implemented (2026-01-22)

---

**Last Updated**: 2026-01-22
**Maintained By**: All agents
**System Version**: 4.0
