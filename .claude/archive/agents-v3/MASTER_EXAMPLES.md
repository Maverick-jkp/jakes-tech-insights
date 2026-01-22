# Master Agent - Examples

This file contains detailed examples for Master agent work patterns.

## Example 1: Simple Task (Master Handles Directly)

```
User: "Change login button color"

Master Analysis:
- Simple task, no agent separation needed
- Master handles directly (no ticket needed)

Action:
1. Create feature/update-button-color branch
2. Modify CSS
3. Commit and merge
```

---

## Example 2: Parallel Work (Real Case - 2026-01-20)

```
User: "Fix category page image placeholder, show 8 categories in floating widget, and change domain to jakes-insights"

Master Analysis:
- 3 separate issues identified
- Designer work (issues 1, 2) + CTO work (issue 3)
- Parallel execution possible (no file conflicts)
- No ticket needed (simple tasks)

Action Items:

### Action Item 1: Category Page Template Fix
**Agent**: DESIGNER
**Branch**: feature/fix-category-page
**Dependencies**: None

### Action Item 2: Domain Configuration Guide
**Agent**: CTO
**Branch**: None (guide only)
**Dependencies**: None

Execution Plan:

**Phase 1 (Parallel)**:
- Designer: Fix category page
- CTO: Domain change guide

**Phase 2 (Integration)**:
- Master: Review and integrate

Prompts:

Session 1: Designer Work
```
You are the DESIGNER agent. Read your role from `.claude/agents/DESIGNER.md`.

**Your tasks**:

1. Fix category page image display (layouts/categories/list.html:315-323)
   - Change from .Params.image to .Resources.GetMatch "cover.*"
   - Apply WebP + fallback structure from main page

2. Fix floating widget grid (layouts/categories/list.html:345-363)
   - Expand from 5 to 8 categories
   - Apply 2x4 grid from main page
   - Add: Sports, Finance, Education

**Branch**: feature/fix-category-page

**Completion criteria**:
- [ ] Images display correctly
- [ ] 8 categories in 2x4 grid
- [ ] Test with hugo server

DO NOT commit or push - report back when done.
```

Session 2: CTO Work
```
You are the CTO agent. Read your role from `.claude/agents/CTO.md`.

**Your task**: Domain migration guide

**What you need to do**:
1. Provide Cloudflare Pages project rename instructions
2. Identify config files needing updates
3. Document the process

**Files to check**:
- hugo.toml (baseURL)
- static/robots.txt (sitemap URLs)

Report back with step-by-step guide for user.
```

Results:
- Designer: 1 template modified (+75, -13 lines)
- CTO: Detailed guide provided
- Master: Updated 2 config files, integrated
- Total: 3 commits created, deployed
```

---

## Example 3: Complex Task (With Ticket)

```
User: "Build user authentication system"

Master Analysis:
- Complex task, agent separation needed
- Ticket required (1+ day work)

Action:
1. Break down tasks
   - Backend API (CTO)
   - Frontend UI (DESIGNER)
   - Security review (CTO)
   - Testing (QA)

2. Create tickets
   - .claude/tasks/active/TASK_001_auth_backend.md
   - .claude/tasks/active/TASK_002_auth_frontend.md
   - .claude/tasks/active/TASK_003_auth_testing.md

3. Determine sequence
   Phase 1: Backend API (CTO)
   Phase 2: Frontend UI (DESIGNER) - after Phase 1
   Phase 3: Testing (QA) - after Phase 2

4. Provide prompts
   Each agent reads ticket file and starts work
```

---

## Example 4: Multiple Parallel Tasks

```
User: "Add dark mode, optimize performance, and increase test coverage to 70%"

Master Analysis:

Task Breakdown:

### Action Item 1: Dark Mode Implementation
**Agent**: DESIGNER
**Work**:
- Define dark mode color palette
- Design CSS variable structure
- Implement light/dark theme toggle logic
- Verify responsive and accessibility

**Justification**: UI/UX design expertise required
**Branch**: feature/dark-mode
**Dependencies**: None (independent)
**Completion Criteria**:
- [ ] Dark mode color system complete
- [ ] Theme toggle works on all pages
- [ ] Accessibility standards met (contrast 4.5:1+)

---

### Action Item 2: Performance Optimization
**Agent**: CTO
**Work**:
- Profile current performance bottlenecks
- Optimize build time (caching, compression)
- Improve runtime performance (image optimization, lazy loading)
- Measure and benchmark improvements

**Justification**: Architecture and performance expertise required
**Branch**: feature/performance
**Dependencies**: None (independent)
**Completion Criteria**:
- [ ] Build time reduced by 20%+
- [ ] Lighthouse performance score 90+
- [ ] Before/after benchmarks documented

---

### Action Item 3: Test Coverage 70%
**Agent**: QA
**Work**:
- Measure and analyze current coverage
- Identify untested areas (prioritize)
- Write tests for core modules
- Generate coverage report

**Justification**: Testing strategy and QA expertise required
**Branch**: feature/test-coverage
**Dependencies**: Action Items 1, 2 complete (integration testing needed)
**Completion Criteria**:
- [ ] Overall coverage 70%+
- [ ] All tests pass (100%)
- [ ] Coverage report documented

---

Execution Plan:

**Phase 1 (Parallel)**:
- DESIGNER: Dark mode
- CTO: Performance optimization

**Phase 2 (Sequential)**:
- QA: Test coverage (after Phase 1 complete)

**Phase 3 (Integration)**:
- MASTER: Review all branches and integrate
- MASTER: Final commit and push
```

---

## Parallel Work Execution Guide

When providing parallel work prompts to user:

```markdown
# Task Decomposition Complete

User request: "{original request}"

Total {N} action items.

---

## Action Item List

### Action Item 1: {Title}
**Agent**: {AGENT_NAME}
**Work**: {Specific description}
**Justification**: {Why this agent}
**Branch**: feature/{branch-name}
**Dependencies**: {None / After Action Item X}
**Completion Criteria**:
- [ ] {Checklist item 1}
- [ ] {Checklist item 2}

---

## Execution Plan

**Phase 1 (Parallel)** - Start now:
- {AGENT_1}: {Work summary}
- {AGENT_2}: {Work summary}

**Phase 2 (Sequential)** - After Phase 1:
- {AGENT_3}: {Work summary}

**Phase 3 (Integration)** - After all complete:
- MASTER: Integration and final commit

---

## Parallel Work Execution Guide

### Step 1: Open New Sessions (Phase 1)

Copy-paste these prompts into **separate sessions**:

---

#### Session 1: {AGENT_1} Work

```
{AGENT_1_PROMPT}
```

---

#### Session 2: {AGENT_2} Work

```
{AGENT_2_PROMPT}
```

---

### Step 2: Report Completion

When each session completes, return to Master session and report:

```
[Session 1] {AGENT_1} work complete
[Session 2] {AGENT_2} work complete
```

### Step 3: Phase 2 Execution (If applicable)

After Phase 1 completes, run in new session:

```
{AGENT_3_PROMPT}
```

### Step 4: Final Integration

When all work completes, in Master session:

```
All work complete. Begin integration and deployment.
```

---

Master will review all branches and perform final integration and commit.
```

---

## Branch vs Ticket Decision Examples

### Simple Task - Branch Only
```
Task: Update CSS styling
Complexity: 1-2 hours
Decision:
- Branch: feature/update-styles
- Ticket: Not needed
- Reason: Prompt sufficient for scope
```

### Medium Task - Branch + Optional Ticket
```
Task: Add new page section
Complexity: Half day
Decision:
- Branch: feature/new-section
- Ticket: Create if details complex
- Reason: Document if multiple steps
```

### Complex Task - Branch + Ticket Required
```
Task: Implement authentication system
Complexity: 1+ days
Decision:
- Branch: feature/auth-system
- Ticket: Required (.claude/tasks/active/TASK_001_auth.md)
- Reason: Detailed documentation needed
```

---

## Integration Completion Template

```markdown
✅ Integration and Deployment Complete

**Integrated Features**:
- ✓ Dark mode (feature/dark-mode)
- ✓ Performance optimization (feature/performance)
- ✓ Test coverage (feature/test-coverage)

**Test Results**:
- 28/28 tests passed
- Coverage: 70.2% (goal 70% achieved)

**Commit Info**:
- Commit: abc1234
- Message: "feat: Add dark mode, optimize performance, improve test coverage"

**Completed Tasks**:
- ✓ Git push complete
- ✓ Documentation updated
- ✓ Changelog updated
- ✓ Tickets archived (.claude/tasks/archive/2026-01/)

**Archive Location**:
.claude/tasks/archive/2026-01/
  - TASK_001_dark_mode.md
  - TASK_002_performance.md
  - TASK_003_test_coverage.md
```

---

**Last Updated**: 2026-01-20
**Related**: [MASTER.md](MASTER.md)
