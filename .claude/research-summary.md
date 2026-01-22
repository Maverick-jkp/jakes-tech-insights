# Production Claude Code Patterns - Research Summary

**Date**: 2026-01-22
**Research Focus**: Extract concrete implementation patterns from production Claude Code workflows

---

## Executive Summary

Analyzed 3 production repositories with 200k+ combined stars to extract proven patterns for Claude Code workflow optimization. Key finding: **Progressive disclosure through modular architecture reduces context load by 70-84% for typical tasks**.

Current system loads 2,778 lines for every task. Production systems load 200-600 lines for simple tasks, 800-1,200 for complex tasks.

---

## Repositories Analyzed

### 1. wshobson/agents
- **Scale**: 72 plugins, 108 agents, 129 skills, 15 workflow orchestrators
- **Pattern**: Plugin-based architecture with progressive disclosure
- **Key File**: plugins/backend-development/agents/backend-architect.md (254 lines)
- **Innovation**: Three-tier model assignment (Opus/Sonnet/Haiku by task complexity)

### 2. anthropics/skills
- **Scale**: 16 official skills, 49k stars
- **Pattern**: Minimal skill definition with on-demand reference loading
- **Key File**: skills/mcp-builder/SKILL.md (1,200 lines for complex skill)
- **Innovation**: Three-tier loading (metadata → instructions → references)

### 3. catlog22/Claude-Code-Workflow
- **Scale**: 1,528 commits, 4-level workflow taxonomy
- **Pattern**: Session-based state management with difficulty-based context
- **Key File**: WORKFLOW_GUIDE.md (731 lines)
- **Innovation**: Level 1-4 workflows with escalating artifact persistence

---

## Key Patterns Extracted

### Pattern 1: Progressive Disclosure

**Production Implementation**:
```
Entry README (200 lines)
  ↓ Overview + navigation
  ↓ Links to specialized docs

Specialized Docs (300-800 lines each)
  ↓ Architecture, usage, design patterns
  ↓ Links to detailed specs

Implementation Files (200-300 lines each)
  ↓ Agent definitions, skills
  ↓ References for deep details
```

**Current System**:
```
CLAUDE.md (957 lines)
  ↓ Everything mixed together
  ↓ Must scan entire file
```

**Recommendation**: Split CLAUDE.md into:
- Entry point: 200 lines (overview + quick commands)
- 7 focused docs: 150-300 lines each
- Skills: 200-400 lines each (loaded on-demand)

**Impact**: 79% reduction in entry point size, 70%+ reduction in context per task

### Pattern 2: Skill Definition Standard

**Anthropic Official Format**:
```yaml
---
name: skill-name
description: What it does and when to use
---

# Skill Title
[Concise instructions - under 500 lines]

## When to Use
[Activation criteria]

## Guidelines
[Specific instructions]

## References
[Links to detailed resources]
```

**Progressive Loading**:
1. **Metadata** (always): 50 tokens (name, description)
2. **Instructions** (on activation): 2,000 tokens
3. **References** (on-demand): 5,000 tokens

**Guideline**: "Only add context Claude doesn't already have"

**Current System**: All instructions embedded in CLAUDE.md (no skills directory)

**Recommendation**: Create 4 core skills:
- content-generation (400 lines)
- quality-validation (300 lines)
- hugo-operations (200 lines)
- keyword-curation (250 lines)

**Impact**: Load only relevant skill per task, not entire documentation

### Pattern 3: Agent Specialization

**Production Example** (wshobson backend-architect.md, 254 lines):

**Structure**:
- Purpose: Single sentence role definition
- Capabilities: 16 subsections covering domain expertise
- Workflow Position: When this agent activates in pipeline
- Defers To: Explicit boundaries with other agents
- Response Methodology: 10-step structured approach

**Key Insight**: Each agent is 200-300 lines, **not** 582 lines mixing all agents

**Current System**: WORKFLOW.md (582 lines) mixes all 4 agents together

**Recommendation**: Split into 4 files:
- agents/master.md (300 lines) - Orchestration only
- agents/designer.md (250 lines) - UI/UX only
- agents/cto.md (250 lines) - Architecture only
- agents/qa.md (250 lines) - Testing only

**Impact**: Each agent reads only their own spec, 57% reduction per agent

### Pattern 4: Session-Based State

**Production Pattern** (catlog22/CCW):
```
.workflow/active/{session-id}/
  ├── state.json (50 lines)
  ├── tasks.json (100 lines)
  └── changes.log (50 lines)

After completion → .workflow/archive/{date}/
```

**Benefits**:
- Per-session state: 200 lines max
- No indefinite growth
- Clean context boundaries
- Easy to review past work

**Current System**: session-state.json (536 lines, growing indefinitely)

**Recommendation**: Implement sessions pattern:
```
.claude/sessions/active/{session}/
  - state.json (50 lines)
  - tasks.json (100 lines)
  - changes.log (50 lines)
```

**Impact**: 63% reduction in active state size, prevents infinite growth

### Pattern 5: Tiered Model Assignment

**Production Pattern** (wshobson):
- **Tier 1 (Opus 4.5)**: 42 critical agents (architecture, security)
- **Tier 2 (Inherit)**: 42 complex agents (user-selected model)
- **Tier 3 (Sonnet 4.5)**: 51 support agents (docs, testing)
- **Tier 4 (Haiku 4.5)**: 18 operational agents (SEO, deployment)

**Rationale**: Reserve expensive models for high-stakes decisions

**Current System**: No tiered model assignment (all use default)

**Recommendation** (future optimization):
- Master: Opus 4.5 (orchestration decisions)
- Designer/CTO/QA: Sonnet 4.5 (specialized work)
- Simple validation: Haiku 4.5 (when available)

**Impact**: Cost optimization while maintaining quality

---

## Concrete Recommendations

### Immediate (Week 1): Split CLAUDE.md

**Action**:
```bash
# Current: 957 lines monolithic
CLAUDE.md → 200 lines (overview + quick commands)

# Create 7 focused docs:
.claude/docs/
  ├── 01-architecture.md (300 lines)
  ├── 02-content-pipeline.md (250 lines)
  ├── 03-hugo-operations.md (150 lines)
  ├── 04-python-scripts.md (200 lines)
  ├── 05-troubleshooting.md (250 lines)
  ├── 06-design-system.md (150 lines)
  └── 07-git-workflow.md (150 lines)
```

**Impact**: 79% reduction in entry point, easier navigation

### Short-term (Week 2): Extract Skills

**Action**:
```bash
.claude/skills/
  ├── content-generation/
  │   ├── SKILL.md (400 lines)
  │   └── references/
  │       ├── english-prompt.txt
  │       ├── korean-prompt.txt
  │       └── japanese-prompt.txt
  │
  ├── quality-validation/
  │   ├── SKILL.md (300 lines)
  │   └── references/
  │       ├── blacklist-en.txt
  │       ├── blacklist-ko.txt
  │       └── blacklist-ja.txt
  │
  ├── hugo-operations/
  │   └── SKILL.md (200 lines)
  │
  └── keyword-curation/
      └── SKILL.md (250 lines)
```

**Impact**: Load only relevant skill per task

### Medium-term (Week 3): Separate Agents

**Action**:
```bash
# Current: WORKFLOW.md (582 lines mixing all agents)

.claude/agents/
  ├── master.md (300 lines)
  ├── designer.md (250 lines)
  ├── cto.md (250 lines)
  └── qa.md (250 lines)

.claude/workflows/
  └── sequential-coordination.md (200 lines)
```

**Impact**: Each agent reads only their spec, clearer boundaries

### Long-term (Week 4): Session-Based State

**Action**:
```bash
# Current: session-state.json (536 lines, growing)

.claude/sessions/
  ├── active/
  │   └── {session-id}/
  │       ├── state.json (50 lines)
  │       ├── tasks.json (100 lines)
  │       └── changes.log (50 lines)
  └── archive/
      └── {date}/
```

**Impact**: 63% reduction, prevents growth, clean boundaries

---

## Expected Results

### Context Reduction

| Task Type | Current | After Refactor | Reduction |
|-----------|---------|---------------|-----------|
| Simple (add keyword) | 2,778 lines | 450 lines | 84% |
| Medium (generate post) | 2,778 lines | 800 lines | 71% |
| Complex (new category) | 2,778 lines | 1,250 lines | 55% |

### File Organization

| Component | Current | After | Notes |
|-----------|---------|-------|-------|
| Entry point | 957 lines | 200 lines | Overview only |
| Agent specs | 582 lines (mixed) | 250 × 4 (separate) | Focused, no overlap |
| Skills | 0 (embedded) | 400 × 4 (modular) | On-demand loading |
| Session state | 536 (growing) | 200 per session | Stable size |
| Total files | 5 major docs | 20-25 focused files | Better organized |

### Maintainability

| Task | Current | After | Improvement |
|------|---------|-------|-------------|
| Update prompt | Edit 957-line CLAUDE.md | Edit 400-line skill | 58% smaller file |
| Add agent | Modify 582-line WORKFLOW.md | Create 250-line agent | No conflicts |
| Fix issue | Search 2,778 lines | Navigate to relevant doc | 2 clicks vs. scanning |
| Archive session | Manual cleanup | Auto-archive | Prevents bloat |

---

## Production Patterns vs. Current System

### Entry Point

**Production** (wshobson):
- README: 200 lines
- Single-sentence value prop
- Quick start: 2 steps
- Links to 5 specialized docs
- "Overview → specialized → implementation" flow

**Current**:
- CLAUDE.md: 957 lines
- Mixed content (commands, architecture, troubleshooting, design, git)
- Must scan entire file
- No clear navigation hierarchy

### Skills/Commands

**Production** (anthropic):
- Each skill: Separate file
- Frontmatter metadata (name, description, activation criteria)
- Progressive loading (metadata → instructions → references)
- "Only add context Claude doesn't already have"

**Current**:
- All instructions embedded in CLAUDE.md
- No skills directory
- No modular components
- Everything loaded always

### Agents

**Production** (wshobson):
- Each agent: 200-300 lines
- Clear role definition
- Explicit capabilities (subsections)
- "Defer to X for Y" boundaries
- Structured methodology

**Current**:
- WORKFLOW.md: 582 lines mixing all agents
- Unclear boundaries (Master does design, Designer codes)
- Report requirements mixed with roles
- Sequential rules mixed with capabilities

### State

**Production** (catlog22):
- Session-based directories
- Per-session files (state, tasks, changes)
- 200 lines max per session
- Archive completed sessions
- No single massive state file

**Current**:
- session-state.json: 536 lines, growing
- No cleanup mechanism
- Mixed recent + historical
- Indefinite growth

---

## Key Learnings

### 1. "2-8 Pattern" (Anthropic)

**Guideline**: Average 3.4 components per plugin

**Rationale**: Balance between:
- Too few: Over-generalization, monolithic
- Too many: Fragmentation, cognitive load

**Application**:
- Skills: 4-6 core skills (not 20)
- Docs: 7 focused docs (not 30)
- Agents: 4 specialized (not 15)

### 2. "Single Responsibility"

**Principle**: Each file addresses one domain

**Benefits**:
- Easy to find
- Easy to update
- Easy to test
- No conflicts

**Application**:
- content-generation skill: Only generation
- hugo-operations skill: Only Hugo
- master agent: Only orchestration
- designer agent: Only UI/UX

### 3. "Progressive Disclosure"

**Principle**: Load context incrementally

**Levels**:
1. Metadata (always)
2. Instructions (on activation)
3. References (on-demand)

**Benefits**:
- Lower token usage
- Faster loading
- Better focus
- Less noise

### 4. "Context Matching"

**Principle**: Match context detail to task complexity

**Application**:
- Simple task: Entry + skill (600 lines)
- Medium task: Entry + skill + session (800 lines)
- Complex task: Entry + skills + docs + session (1,250 lines)

**Current**: Always 2,778 lines regardless

### 5. "Session Isolation"

**Principle**: Each session is self-contained

**Benefits**:
- Clean boundaries
- Easy to review
- No state leak
- Automatic cleanup

**Application**: Active session vs. archived sessions

---

## Common Anti-Patterns (What to Avoid)

### Anti-Pattern 1: Monolithic Documentation

**Problem**: Single massive file (CLAUDE.md 957 lines)
**Issue**: Must scan entire file for every task
**Solution**: Split into entry + specialized docs

### Anti-Pattern 2: Mixed Concerns

**Problem**: WORKFLOW.md mixes agents, rules, templates
**Issue**: Hard to find, hard to update, conflicts
**Solution**: Separate files per agent, per workflow

### Anti-Pattern 3: Indefinite State Growth

**Problem**: session-state.json grows forever (536 lines → 1000+ lines)
**Issue**: Slower loading, harder to parse, never cleaned
**Solution**: Session-based directories with archiving

### Anti-Pattern 4: Report Overhead

**Problem**: Every agent creates detailed report for every task
**Issue**: Time-consuming, often not read, noise
**Solution**: Report only for significant work

### Anti-Pattern 5: Unclear Agent Boundaries

**Problem**: Master does design, Designer codes, CTO overlaps
**Issue**: Conflicts, duplication, unclear responsibility
**Solution**: Explicit "defer to X for Y" boundaries

---

## Implementation Timeline

### Week 1: Split CLAUDE.md
- **Time**: 4-6 hours
- **Files**: 1 → 8 (entry + 7 docs)
- **Impact**: 79% reduction in entry point
- **Risk**: Low (backup available)

### Week 2: Extract Skills
- **Time**: 6-8 hours
- **Files**: 0 → 4 skills
- **Impact**: 70%+ context reduction for simple tasks
- **Risk**: Low (new files, no deletion)

### Week 3: Separate Agents
- **Time**: 5-7 hours
- **Files**: 1 → 4 agents + 1 workflow
- **Impact**: 57% per-agent reduction
- **Risk**: Medium (multi-agent workflow changes)

### Week 4: Session State
- **Time**: 5-7 hours
- **Files**: 1 → session directories
- **Impact**: 63% state reduction, prevents growth
- **Risk**: Medium (state migration needed)

**Total**: 20-28 hours over 4 weeks

---

## Success Metrics

### Quantitative

- Entry point: 957 → 200 lines (79% reduction)
- Simple task context: 2,778 → 450 lines (84% reduction)
- Medium task context: 2,778 → 800 lines (71% reduction)
- Agent spec: 582 → 250 lines per agent (57% reduction)
- Session state: 536 → 200 lines stable (63% reduction)

### Qualitative

- Find info: 2 clicks (vs. scanning 957 lines)
- Update prompt: 400-line skill (vs. 957-line monolith)
- Add agent: New 250-line file (vs. modify 582-line mixed file)
- Archive session: Automatic (vs. manual cleanup)
- Understand system: 200-line overview (vs. 957-line mixed doc)

---

## Next Steps

1. **Review** this summary with user
2. **Approve** refactor plan
3. **Start Phase 1**: Split CLAUDE.md (Week 1)
4. **Validate** after each phase
5. **Adjust** based on learnings

---

## References

### Full Analysis
- `.claude/production-patterns-analysis.md` (4,338 lines)
  - Detailed comparison of all 3 repositories
  - Complete pattern extraction
  - Line-by-line recommendations
  - File size comparisons

### Implementation Plan
- `.claude/refactor-roadmap.md` (800 lines)
  - Week-by-week tasks
  - Validation checklist
  - Risk mitigation
  - Rollback procedures

### Research Sources
1. wshobson/agents: https://github.com/wshobson/agents
2. anthropics/skills: https://github.com/anthropics/skills
3. catlog22/Claude-Code-Workflow: https://github.com/catlog22/Claude-Code-Workflow

---

**Last Updated**: 2026-01-22
**Status**: Research complete, ready for Phase 1
**Owner**: Jake Park
