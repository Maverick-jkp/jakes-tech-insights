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

## 2026-01-22: Master Agent Failed to Verify State Before Acting

**What happened**: User reported missing thumbnails in Korean + Japanese posts. Master agent immediately started "fixing" without verifying:
1. Whether the problem still existed in remote repository
2. Whether `.env` file existed and contained API keys
3. Whether git was available

**Specific failures**:
1. **Fabricated root cause**: Claimed `UNSPLASH_ACCESS_KEY` was missing from environment
   - Reality: `.env` file clearly contained `UNSPLASH_ACCESS_KEY=dDi7...`
   - Never checked `.env` file before making claim

2. **Ignored documented procedures**: CLAUDE.md lines 80-82 show exact method to load .env with `load_dotenv()`
   - Instead tried: direct file parsing, `source .env`, various improvised workarounds
   - Read documentation but didn't apply it

3. **Did unnecessary work**:
   - Fetched 4 Unsplash images via API
   - Used Edit tool to update files
   - Git showed "nothing to commit, working tree clean"
   - Files were already fixed in remote repository from previous session

4. **Failed to verify before acting**:
   - Never ran `git show origin/main:filename` to check remote state
   - Never ran `git status` before assuming changes needed
   - Assumed user report meant current issue without verification

**Rule broken**:
- **Master Agent Checklist Step 4**: "Understand user request" - but didn't verify current state
- **CLAUDE.md mandate**: Read documentation and FOLLOW procedures (not just read)
- **Basic workflow**: Verify problem exists before attempting fix

**Impact**:
- Wasted 15+ minutes of user's time
- User had to send 6 increasingly frustrated messages
- Repeated same error patterns despite System 5.0 improvements
- User explicitly asked: "어떻게 아무리 md를 업그레이드해도 5일 내내 이지랄이냐" (How can you keep doing this for 5 days despite documentation upgrades?)

**Root cause**:
1. **Reading ≠ Following**: Read CLAUDE.md but didn't follow documented procedures
2. **Failed to verify assumptions**: User said "thumbnails missing" → assumed it's currently broken → didn't check remote state
3. **Improvisation over documentation**: When encountering issues, improvised solutions instead of following documented methods
4. **No pre-action verification**: Didn't check current state before attempting "fixes"

**Pattern identified**:
This is the THIRD incident of "documentation exists but agent doesn't follow it":
- 2026-01-22: Designer committed without report (didn't read docs)
- 2026-01-22: System overhaul (agents skipped "Before Work" sections)
- **2026-01-22: Master claimed missing .env despite documentation (didn't follow docs)**

**The actual systemic issue**:
Documentation reading is happening, but **application of documented procedures is not happening**.

**Prevention measures needed**:

1. **Mandatory pre-action verification checklist**:
   ```bash
   # Before ANY "fix", MUST run these:
   [ ] git status
   [ ] git diff
   [ ] git show origin/main:path/to/file
   [ ] Verify problem actually exists locally
   [ ] Check .env file exists (ls -la .env)
   ```

2. **When documented procedure exists, MUST use it**:
   - ❌ "I'll try to parse .env manually"
   - ✅ "CLAUDE.md line 82 says: `python -c 'from dotenv import load_dotenv; load_dotenv()'`"

3. **Assume remote repository may already have fix**:
   - User reports historical issue
   - Check if already fixed in previous session
   - Report findings instead of re-doing work

4. **Update CLAUDE.md to add verification requirements**:
   - Add "Verify Problem Exists" as mandatory Step 1
   - Add "Check Remote State First" as mandatory Step 2
   - Make following documented procedures non-negotiable

**Lesson learned**:
- System 5.0 documentation exists and is comprehensive
- The failure is in **EXECUTION**, not documentation
- Master agent must treat documented procedures as mandatory, not optional
- "Read and understand" must become "Read and APPLY EXACTLY"

**Success metrics update** (30-day evaluation):
- Target: 100% documented procedure compliance (not just reading)
- Target: Zero assumption-based actions (verify first)
- Target: Pre-action verification checklist completed every time
- Current: FAILING - 5 days of repeated execution failures despite documentation

---

**Last Updated**: 2026-01-22
**Maintained By**: All agents
**System Version**: 5.0
