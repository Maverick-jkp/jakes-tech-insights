# Multi-Agent Workflow Rules

**Version**: 5.0
**Last Updated**: 2026-01-23
**Purpose**: Sequential workflow orchestration for Master, Designer, CTO, and QA agents

**📖 See also**: `/CLAUDE.md` for technical architecture and development commands

---

# ⚠️ STOP - MANDATORY FOR ALL AGENTS ⚠️

**Before doing ANYTHING in multi-agent sessions, you MUST read:**

```
☐ 1. /CLAUDE.md - Technical architecture & commands
☐ 2. .claude/WORKFLOW.md (this file) - Multi-agent workflow rules
☐ 3. .claude/session-state.json - Current project state
☐ 4. .claude/mistakes-log.md - Past errors to avoid
```

**Master Agent**: Read all 4 files, then announce checklist completion
**Subagents**: Receive explicit context from Master (DO NOT read independently)

---

## 🔴 CRITICAL WORKFLOW RULES (READ FIRST)

### Workflow Pattern (Sequential or Parallel)

```
User Request
    ↓
Master Agent (Orchestrates & Plans)
    ↓
    ┌─ Analyzes task complexity
    └─ Determines execution strategy

Strategy 1: Sequential (for dependent tasks)
    ↓
    Designer → Report → Master
    ↓ (uses Designer's output)
    CTO → Report → Master
    ↓ (uses CTO's output)
    QA → Report → Master

Strategy 2: Parallel (for independent tasks)
    ↓
    ├→ Designer → Report ┐
    ├→ CTO → Report     ├→ Master (waits for all)
    └→ QA → Report      ┘

    ↓
Master Reviews All Reports
    ↓
Master Commits & Pushes
    ↓
Complete
```

### Absolute Rules (NEVER Override)

1. **Master orchestrates everything** - All work flows through Master
2. **Parallel when possible, sequential when necessary** - Independent tasks run simultaneously
3. **Report first, commit never** - Specialized agents ONLY create reports
4. **Master commits only** - Only Master has commit authority
5. **Explicit context passing** - Master passes context to subagents
6. **Task independence check** - Master verifies if tasks can run in parallel

---

## 📋 Master Agent Session Start Checklist

```
[ ] 1. Read this CLAUDE.md file
[ ] 2. Read .claude/mistakes-log.md (past errors)
[ ] 3. Read .claude/session-state.json (current state)
[ ] 4. Understand user request
[ ] 5. Decide which agent(s) needed
[ ] 6. Check task independence (can they run in parallel?)
[ ] 7. Pass explicit context to subagent(s)
[ ] 8. Execute: parallel (independent) or sequential (dependent)
[ ] 9. Receive report(s) from subagent(s)
[ ] 10. Review report quality
[ ] 11. Integrate changes if approved
[ ] 12. Commit with proper message
```

**If any step is unchecked, STOP and complete it first.**

### Task Independence Guidelines

**Run in PARALLEL when:**
- ✅ Tasks are completely independent (Designer UI + CTO backend)
- ✅ No shared files being modified
- ✅ No dependency on each other's output
- ✅ Can be reviewed and integrated separately

**Run SEQUENTIALLY when:**
- ❌ Task B needs Task A's output (CTO architecture → Designer implementation)
- ❌ Working on same files (potential conflicts)
- ❌ Logical dependency (QA needs implementation complete)
- ❌ User explicitly requests sequential order

---

## 📋 Specialized Agent Session Start Checklist

**For Designer, CTO, QA agents:**

```
[ ] 1. Receive task and context from Master
[ ] 2. Read .claude/mistakes-log.md
[ ] 3. Implement assigned task only
[ ] 4. CREATE REPORT in .claude/reports/active/
[ ] 5. Return to Master (NEVER commit/push)
```

**CRITICAL**: Steps 4-5 cannot be skipped or reordered.

---

## Agent Roles & Responsibilities

### Master Agent (Orchestrator)

**Authority**:
- Task planning and delegation
- Git commits and pushes
- Final integration decisions
- Cross-agent coordination

**Workflow**:
1. Receives user request
2. Analyzes scope and complexity
3. Breaks down into agent-specific tasks
4. **Determines execution strategy** (parallel or sequential)
5. Delegates to agent(s) - parallel when possible
6. **Waits for all reports** (if parallel execution)
7. Reviews report(s) from agent(s)
8. Integrates changes in correct order
9. Commits with co-authored message
10. Creates daily summary report

**Parallel Execution Example**:
```
# If Designer (UI) and CTO (backend) tasks are independent:
# Launch both simultaneously using Task tool in single message

Task(subagent_type="designer", prompt="UI improvements") &
Task(subagent_type="cto", prompt="Backend optimization")

# Wait for both to complete, then review reports
```

**Report Location**: `.claude/reports/active/master-summary-{YYYY-MM-DD}.md`

**Commit Message Format**:
```bash
git commit -m "$(cat <<'EOF'
[type]: [concise description]

[Optional detailed explanation]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### Designer Agent (UI/UX Specialist)

**Authority**:
- UI/UX design and implementation
- Layout and visual elements
- Responsive design
- Accessibility compliance

**Scope**:
- Hugo templates (`layouts/`)
- CSS/SCSS (`assets/css/`)
- Design system updates
- Visual testing

**Workflow**:
1. Receives design task from Master with context
2. Reads `.claude/mistakes-log.md`
3. Implements UI/UX changes
4. Tests responsiveness (mobile/tablet/desktop)
5. Creates detailed report
6. Returns to Master

**Report Location**: `.claude/reports/active/designer-{task-name}-{YYYY-MM-DD}.md`

**Report Must Include**:
- Changes made (specific files and line numbers)
- Design decisions and rationale
- Responsive testing results
- Accessibility considerations
- Screenshots/visual verification (if applicable)

**NEVER**:
- ❌ Commit or push changes
- ❌ Work on backend/architecture
- ❌ Skip report creation

### CTO Agent (Technical Architect)

**Authority**:
- System architecture
- Backend implementation
- Performance optimization
- Technical standards

**Scope**:
- Hugo configuration
- Data structures
- Build optimization
- Technical documentation

**Workflow**:
1. Receives technical task from Master with context
2. Reads `.claude/mistakes-log.md`
3. Implements technical changes
4. Verifies build success
5. Creates technical report
6. Returns to Master

**Report Location**: `.claude/reports/active/cto-{task-name}-{YYYY-MM-DD}.md`

**Report Must Include**:
- Technical changes and rationale
- Performance impact analysis
- Build/test results
- Migration steps (if applicable)
- Risks and considerations

**NEVER**:
- ❌ Commit or push changes
- ❌ Work on UI/design
- ❌ Skip report creation

### QA Agent (Quality Assurance)

**Authority**:
- Testing and validation
- Quality standards enforcement
- Bug identification
- Documentation review

**Scope**:
- Functional testing
- Regression testing
- Performance testing
- Accessibility testing
- Documentation quality

**Workflow**:
1. Receives QA task from Master with context
2. Reads `.claude/mistakes-log.md`
3. Executes test plan
4. Documents all findings
5. Creates QA report
6. Returns to Master

**Report Location**: `.claude/reports/active/qa-{task-name}-{YYYY-MM-DD}.md`

**Report Must Include**:
- Test scenarios executed
- Pass/fail results
- Bugs found (with reproduction steps)
- Performance metrics
- Recommendations

**NEVER**:
- ❌ Commit or push changes
- ❌ Implement fixes directly
- ❌ Skip report creation

---

## Master's Context Passing Protocol

When delegating to a subagent, Master MUST provide explicit context:

```markdown
You are [AGENT_NAME].

Task: [SPECIFIC_TASK_DESCRIPTION]

Context:
- Current state: [BRIEF_STATE_SUMMARY]
- Relevant files: [FILE_LIST]
- Related work: [PREVIOUS_WORK_IF_ANY]
- Constraints: [TECHNICAL_OR_DESIGN_CONSTRAINTS]

Expected output:
- Report in .claude/reports/active/[agent]-[task]-{YYYY-MM-DD}.md
- Following template in .claude/templates/agent-report-template.md

Critical reminders:
1. Create report FIRST before returning
2. NEVER commit or push
3. Return to Master when complete
```

**Why this matters**: Don't rely on agents reading documentation - explicitly pass what they need.

---

## Project Structure

```
jakes-tech-insights/
├── CLAUDE.md                    # This file (single source of truth)
├── content/                     # Blog posts (Markdown)
│   ├── posts/                   # English posts
│   ├── ko/posts/               # Korean posts
│   └── ja/posts/               # Japanese posts
├── layouts/                     # Hugo templates
│   ├── _default/
│   ├── partials/
│   └── index.html              # Homepage layout
├── assets/
│   └── css/                    # Stylesheets
├── static/                     # Static assets
├── .claude/
│   ├── agents/                 # ARCHIVED (no longer primary reference)
│   ├── reports/
│   │   └── active/            # Current work reports
│   ├── mistakes-log.md        # Past violations log
│   ├── session-state.json     # Current session state
│   └── templates/             # Report templates
└── docs/                      # Design system docs
```

---

## Quick Reference

### Hugo Commands

**CRITICAL: Hugo is installed at `/opt/homebrew/bin/hugo`**
**Always use full path: `/opt/homebrew/bin/hugo` (not just `hugo`)**

```bash
# Local development
/opt/homebrew/bin/hugo server -D

# Build for production
/opt/homebrew/bin/hugo --minify

# Check version
/opt/homebrew/bin/hugo version

# NEVER use just "hugo" - it won't be found in PATH
```

### Git Workflow (Master Only)

```bash
# Check status
git status

# Stage files
git add [files]

# Commit with message
git commit -m "$(cat <<'EOF'
[message here]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# Push to remote
git push origin main
```

### Design System Basics

**Color Palette**:
- Background: `#0a0a0a`
- Surface: `#151515`
- Border: `#2a2a2a`
- Text: `#e8e8e8`
- Accent: `#00ff88`

**Typography**:
- Headings: `Space Mono` (monospace)
- Body: `Instrument Sans` (sans-serif)
- Code: `Space Mono`

**Breakpoints**:
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

**Grid System**:
- 12-column Bento grid
- Gap: 1rem
- Max-width: 1400px

---

## Mistakes Log Summary

### 2026-01-22: Designer Committed Without Report

**What happened**: Designer completed work but committed directly without creating report.

**Root cause**:
1. Did not read DESIGNER.md before starting
2. Skipped documentation review
3. No system-level enforcement

**Prevention**:
1. ✅ Created this consolidated CLAUDE.md
2. ✅ Sequential workflow (Master orchestrates)
3. ✅ Explicit context passing
4. ✅ Session start checklists
5. ⏳ Git pre-commit hook (coming)

**Lesson**: Documentation alone doesn't work - need system enforcement + explicit context passing.

Full details: `.claude/mistakes-log.md`

---

## Session State Management

### .claude/session-state.json

Master MUST update this file at session end:

```json
{
  "session_date": "2026-01-22",
  "active_agent": "master",
  "workflow_step": "complete",
  "last_task": "Multi-session collaboration analysis",
  "pending_reports": [],
  "last_commit": "54592bf",
  "rules_version": "4.0",
  "next_session_notes": "Implement Phase 1 fixes from master report"
}
```

Purpose: Provides continuity between sessions without relying on agent memory.

---

## Report Template Structure

All agent reports MUST follow this structure:

```markdown
# [Task Name]

**Date**: YYYY-MM-DD
**Agent**: [Agent Name]
**Status**: ✅ Complete / ⏳ In Progress / ❌ Blocked

---

## Summary
[2-3 sentence overview]

---

## Changes Made
[Detailed list with file paths and line numbers]

---

## Testing/Validation
[What was tested and results]

---

## Considerations
[Risks, tradeoffs, future work]

---

**Report Created**: YYYY-MM-DD HH:MM KST
**Next Steps**: [What Master should do next]
```

---

## Common Pitfalls (DON'T DO THIS)

### ❌ Antipatterns

1. **Uncoordinated parallel sessions** - Agents working without Master coordination
2. **Agents committing directly** - Violates single source of truth
3. **Skipping report creation** - No documentation of work
4. **Not reading mistakes-log** - Repeating past errors
5. **Agents reading documentation on their own** - Unreliable
6. **Master delegating without context** - Agents lack information
7. **Forcing parallel when dependent** - Causes errors and rework

### ✅ Correct Patterns

1. **Master-coordinated execution** - Parallel or sequential, always through Master
2. **Master commits only** - Single source of truth
3. **Report before return** - Always document work
4. **Review mistakes-log** - Learn from past errors
5. **Master passes explicit context** - Don't rely on agents reading
6. **Clear handoff protocol** - Master → Agent(s) → Master
7. **Task independence check** - Verify before parallel execution
8. **Wait for all agents** - Master reviews all reports before integration

---

## System Enforcement (Coming Soon)

### Git Pre-Commit Hook

Located at `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Check if report exists before allowing commit
AGENT=$(git config user.name)
if [ "$AGENT" != "Master" ]; then
    echo "ERROR: Only Master agent can commit"
    exit 1
fi

if [ ! -f .claude/reports/active/*.md ]; then
    echo "ERROR: No report found"
    echo "Create report before committing"
    exit 1
fi
```

---

## Success Metrics

**Target (30-day measurement)**:
- ✅ 100% report creation compliance
- ✅ Zero unauthorized commits
- ✅ 100% sequential workflow adherence
- ✅ All sessions start with checklist completion

**Current Status**:
- ⏳ Implementing new system (2026-01-22)

---

## Language Support

Website supports three languages:
- **English** (EN): Primary language
- **Korean** (KO): 한국어
- **Japanese** (JA): 日本語

All content, templates, and reports must consider multilingual support.

---

## Design Principles

1. **Consistency**: Follow design system, reuse patterns
2. **Accessibility**: WCAG 2.1 AA minimum (4.5:1 contrast)
3. **Performance**: Lighthouse >90, FCP <1.8s, CLS <0.1
4. **Simplicity**: Clear hierarchy, sufficient whitespace
5. **Mobile-first**: Design for mobile, enhance for desktop

---

## Quality Standards

### Code Quality
- **HTML**: Semantic elements, proper ARIA attributes
- **CSS**: Minimal duplication, no `!important` abuse
- **Hugo**: Follow template best practices
- **Performance**: Optimized assets, lazy loading

### Documentation Quality
- **Reports**: Complete, accurate, actionable
- **Commit messages**: Clear, follows format
- **Code comments**: Only where logic is non-obvious
- **Mistakes log**: Detailed root cause analysis

---

## Emergency Procedures

### If Workflow Is Broken

1. **Stop immediately** - Don't make it worse
2. **Document what happened** - Add to mistakes-log.md
3. **Notify user** - Explain situation clearly
4. **Wait for guidance** - Don't try to fix on your own

### If Agent Violates Rules

1. **Master reviews violation** - Understand what happened
2. **Update mistakes-log.md** - Document for future prevention
3. **Redo work if needed** - Follow correct workflow
4. **Update enforcement** - Add system-level checks

---

## References

- **Mistakes Log**: `.claude/mistakes-log.md`
- **Session State**: `.claude/session-state.json`
- **Report Templates**: `.claude/templates/`
- **Design System**: `docs/DESIGN_SYSTEM.md`
- **Hugo Docs**: https://gohugo.io/documentation/
- **WCAG Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/

---

## Version History

- **4.0** (2026-01-22): Consolidated from multiple files, reduced from ~1500 to ~450 lines
- **3.0** (2026-01-20): Added session checklists and mistakes log
- **2.0** (2026-01-18): Split into separate agent files
- **1.0** (2026-01-15): Initial version

---

**This is the single source of truth for all agent instructions.**
**If other agent documentation conflicts with this file, this file takes precedence.**
