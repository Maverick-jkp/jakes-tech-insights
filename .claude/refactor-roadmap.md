# Documentation Refactor Roadmap

**Goal**: Transform monolithic documentation into production-ready modular structure
**Timeline**: 4 weeks (1 phase per week)
**Success**: 70%+ context reduction for simple/medium tasks

---

## Phase 1: Split CLAUDE.md (Week 1)

**Status**: Not started
**Priority**: Critical
**Time**: 4-6 hours

### Tasks

1. **Create directory structure**
   ```bash
   mkdir -p .claude/docs
   ```

2. **Backup current file**
   ```bash
   cp CLAUDE.md CLAUDE.md.backup
   cp CLAUDE.md .claude/archive/CLAUDE-pre-refactor-2026-01-22.md
   ```

3. **Create new CLAUDE.md (200 lines)**
   - Project overview (3 paragraphs)
   - Quick command reference (Hugo, Python, Testing)
   - Navigation to specialized docs
   - Links to .claude/docs/

4. **Extract to .claude/docs/**

   **01-architecture.md (300 lines)**
   - Content generation flow diagram
   - Topic queue state machine
   - System components
   - Multi-agent workflow

   **02-content-pipeline.md (250 lines)**
   - Draft agent (system prompts high-level)
   - Editor agent
   - Quality gate rules
   - AI reviewer criteria
   - Post format requirements

   **03-hugo-operations.md (150 lines)**
   - Hugo path (/opt/homebrew/bin/hugo)
   - All Hugo commands
   - Template structure
   - Theme overrides

   **04-python-scripts.md (200 lines)**
   - topic_queue.py API
   - generate_posts.py workflow
   - quality_gate.py checks
   - ai_reviewer.py scoring
   - keyword_curator.py usage

   **05-troubleshooting.md (250 lines)**
   - Hugo not found → use full path
   - API key issues → .env loading
   - Queue stuck → cleanup command
   - Quality gate failures → specific fixes
   - GitHub Actions delays → expected behavior

   **06-design-system.md (150 lines)**
   - Colors (dark theme)
   - Typography (Space Mono, Instrument Sans)
   - Breakpoints
   - Grid system

   **07-git-workflow.md (150 lines)**
   - Pre-commit hook
   - Commit message format
   - Branch strategy
   - PR workflow

5. **Update cross-references**
   - All links in CLAUDE.md → .claude/docs/
   - README.md → CLAUDE.md navigation section
   - WORKFLOW.md → CLAUDE.md and docs links

6. **Test**
   - Read new CLAUDE.md as first-time user
   - Follow navigation links
   - Verify no broken links
   - Check all content migrated

### Success Criteria

- [ ] CLAUDE.md: 200 lines or less
- [ ] 7 docs created in .claude/docs/
- [ ] All original content preserved
- [ ] No broken links
- [ ] Backup files created

### Rollback Plan

```bash
# If issues arise
cp CLAUDE.md.backup CLAUDE.md
rm -rf .claude/docs
```

---

## Phase 2: Extract Skills (Week 2)

**Status**: Not started
**Priority**: High
**Time**: 6-8 hours

### Tasks

1. **Create skills structure**
   ```bash
   mkdir -p .claude/skills/{content-generation,quality-validation,hugo-operations,keyword-curation}/references
   ```

2. **content-generation/SKILL.md (400 lines)**

   **Frontmatter**:
   ```yaml
   ---
   name: content-generation
   description: Generate multilingual blog posts using Claude API with Draft + Editor agents.
                Use when: creating posts, updating prompts, testing generation pipeline.
   ---
   ```

   **Sections**:
   - System architecture overview
   - Draft agent workflow
   - Editor agent workflow
   - Prompt caching configuration
   - Max tokens settings
   - Language-specific considerations
   - API cost optimization

   **References** (loaded on-demand):
   - references/english-prompt.txt (800 lines from generate_posts.py)
   - references/korean-prompt.txt (750 lines)
   - references/japanese-prompt.txt (800 lines)

3. **quality-validation/SKILL.md (300 lines)**

   **Frontmatter**:
   ```yaml
   ---
   name: quality-validation
   description: Validate content quality with word counts, AI phrase detection, SEO checks.
                Use when: checking posts, debugging quality failures, updating rules.
   ---
   ```

   **Sections**:
   - Word count requirements by language
   - Structure requirements (sections, intro, conclusion)
   - AI phrase blacklist
   - SEO validation rules
   - Image requirements
   - References section checks

   **References**:
   - references/blacklist-en.txt (30 phrases)
   - references/blacklist-ko.txt (25 phrases)
   - references/blacklist-ja.txt (25 phrases)

4. **hugo-operations/SKILL.md (200 lines)**

   **Frontmatter**:
   ```yaml
   ---
   name: hugo-operations
   description: Run Hugo commands, manage templates, preview site locally.
                Use when: building site, starting dev server, debugging templates.
   ---
   ```

   **Sections**:
   - Hugo installation path
   - Common commands (server, build, version)
   - Template structure
   - Override patterns
   - Local preview workflow
   - Build error debugging

5. **keyword-curation/SKILL.md (250 lines)**

   **Frontmatter**:
   ```yaml
   ---
   name: keyword-curation
   description: Research and curate trending keywords using Google Trends API.
                Use when: adding topics, weekly curation, analyzing trends.
   ---
   ```

   **Sections**:
   - Google Trends API usage
   - Manual filtering criteria
   - Queue addition workflow
   - Priority scoring
   - Category selection
   - Language considerations

6. **Update CLAUDE.md**
   - Add "Skills" section
   - Link to each skill
   - Explain when skills are loaded

7. **Test skills**
   - Load content-generation for post generation task
   - Load quality-validation for validation task
   - Verify progressive loading works
   - Check references load on-demand

### Success Criteria

- [ ] 4 skills created with frontmatter
- [ ] Each skill: 200-400 lines main file
- [ ] References separated for on-demand loading
- [ ] Skills referenced in CLAUDE.md
- [ ] Test: Generate post using skill
- [ ] Test: Validate content using skill

---

## Phase 3: Separate Agents (Week 3)

**Status**: Not started
**Priority**: Medium
**Time**: 5-7 hours

### Tasks

1. **Create agents structure**
   ```bash
   mkdir -p .claude/agents
   mkdir -p .claude/workflows
   ```

2. **Extract from WORKFLOW.md (582 lines) to 4 agent files**

3. **agents/master.md (300 lines)**

   **Structure** (following wshobson/agents backend-architect pattern):

   **Purpose**: Orchestration agent for multi-agent workflows

   **Capabilities**:
   - Task analysis and breakdown
   - Agent delegation (Designer, CTO, QA)
   - Report review and synthesis
   - Final approval authority
   - Commit authorization
   - Context management

   **Workflow Position**: Always active in multi-agent mode, first and last

   **Defers to**:
   - Designer: UI/UX decisions, layout, visual design
   - CTO: Architecture, backend, API design
   - QA: Testing, validation, bug verification

   **Response Format**: 10-step methodology
   1. Analyze request
   2. Break into sub-tasks
   3. Identify required agents
   4. Delegate with context
   5. Review reports
   6. Synthesize findings
   7. Make final decisions
   8. Create commit plan
   9. Execute commit
   10. Document session

4. **agents/designer.md (250 lines)**

   **Purpose**: UI/UX specialist for layout and visual design

   **Capabilities**:
   - Layout recommendations
   - Color scheme proposals
   - Typography decisions
   - Accessibility compliance
   - Responsive design patterns
   - CSS architecture

   **Workflow Position**: After Master delegates, before CTO implementation

   **Defers to**:
   - CTO: Backend implementation, API design
   - QA: Testing, validation
   - Master: Final approval

   **Report Format**:
   - Visual mockups or descriptions
   - CSS code snippets
   - Accessibility notes
   - Implementation guidance

5. **agents/cto.md (250 lines)**

   **Purpose**: Architecture and backend specialist

   **Capabilities**:
   - System architecture design
   - Backend optimization
   - API design
   - Database schema changes
   - Performance optimization
   - Code refactoring

   **Workflow Position**: After Designer (if applicable), before QA

   **Defers to**:
   - Designer: UI/UX decisions
   - QA: Testing strategy
   - Master: Final approval

   **Report Format**:
   - Architecture decisions
   - Code changes
   - Performance impact
   - Migration plan (if needed)

6. **agents/qa.md (250 lines)**

   **Purpose**: Testing and validation specialist

   **Capabilities**:
   - Test strategy design
   - Quality validation
   - Bug verification
   - Regression testing
   - Performance testing
   - Security checks

   **Workflow Position**: After CTO implementation, before Master final approval

   **Defers to**:
   - Master: Final approval

   **Report Format**:
   - Test results
   - Issues found
   - Recommendations
   - Approval/rejection

7. **workflows/sequential-coordination.md (200 lines)**

   **Content from WORKFLOW.md**:
   - One agent at a time rule
   - Handoff procedures
   - Report requirements
   - Context preservation
   - Master authority

8. **Update WORKFLOW.md**
   - Reduce to 150 lines (overview only)
   - Link to agents/*.md for details
   - Link to workflows/sequential-coordination.md

9. **Test multi-agent workflow**
   - Simple task (one agent)
   - Medium task (two agents)
   - Complex task (all agents)
   - Verify handoff works
   - Check report formats

### Success Criteria

- [ ] 4 agent files created (250-300 lines each)
- [ ] Each agent: Clear role, capabilities, boundaries
- [ ] WORKFLOW.md reduced to 150 lines (overview)
- [ ] Sequential coordination extracted
- [ ] Test: Multi-agent workflow completes successfully
- [ ] Each agent reads only their own file

---

## Phase 4: Session-Based State (Week 4)

**Status**: Not started
**Priority**: Medium
**Time**: 4-5 hours

### Tasks

1. **Create sessions structure**
   ```bash
   mkdir -p .claude/sessions/{active,archive}
   ```

2. **Design session format**

   **Session directory**: `.claude/sessions/active/{session-id}/`

   **Files**:
   - `state.json` (50 lines)
     - session_id
     - started_at
     - updated_at
     - current_task
     - status (active, paused, completed)

   - `tasks.json` (100 lines)
     - tasks: [array of task objects]
     - each task: id, description, status, created, updated

   - `changes.log` (50 lines)
     - files_created: [array]
     - files_modified: [array]
     - commits: [array]

   - `notes.md` (variable)
     - Context notes
     - Decisions made
     - Open questions

3. **Migrate current session-state.json**

   **Current file**: 536 lines

   **Migration script**:
   ```python
   # scripts/migrate_session_state.py
   # Parse session-state.json
   # Extract current session info
   # Create new session directory
   # Split into state/tasks/changes files
   # Archive historical data
   ```

4. **Create session archive script**
   ```python
   # scripts/archive_session.py
   # Move .claude/sessions/active/{id} → archive/
   # Compress if large
   # Update index
   ```

5. **Update session management**
   - Create new session: Auto-generate ID
   - Update session: Append to changes.log
   - Complete session: Move to archive
   - Rotate: Keep 5 recent, archive rest

6. **Update documentation**
   - CLAUDE.md: Explain session pattern
   - .claude/docs/01-architecture.md: Session lifecycle

7. **Test session workflow**
   - Start new session
   - Make changes (tasks, files)
   - Complete session
   - Archive session
   - Start another session
   - Verify no state leak between sessions

### Success Criteria

- [ ] Session structure created
- [ ] Current state migrated to session format
- [ ] Active session: 200 lines max
- [ ] Archive mechanism working
- [ ] Test: Multiple sessions don't interfere
- [ ] Documentation updated

---

## Phase 5: Mistakes Log Rotation (Week 4)

**Status**: Not started
**Priority**: Low
**Time**: 1-2 hours

### Tasks

1. **Create mistakes structure**
   ```bash
   mkdir -p .claude/mistakes/archive
   ```

2. **Rotate current mistakes-log.md**
   - Keep recent mistakes (last 2 weeks) in `current.md`
   - Move older mistakes to `archive/2026-01.md`

3. **Create rotation script**
   ```python
   # scripts/rotate_mistakes.py
   # Read mistakes-log.md
   # Parse by date
   # Keep recent (50 lines max)
   # Archive older by month
   ```

4. **Update documentation**
   - CLAUDE.md: Explain mistakes rotation

### Success Criteria

- [ ] Mistakes structure created
- [ ] Current file rotated
- [ ] current.md: 50 lines max
- [ ] Monthly archives created
- [ ] Rotation script working

---

## Validation Checklist

After each phase, run these checks:

### Functionality Tests

```bash
# 1. Hugo still builds
/opt/homebrew/bin/hugo --minify

# 2. Python scripts still work
python scripts/topic_queue.py stats
python scripts/generate_posts.py --count 1

# 3. Tests still pass
pytest

# 4. Git still works
git status
git diff
```

### Documentation Tests

- [ ] CLAUDE.md readable in 5 minutes
- [ ] Can find relevant info in 2 clicks
- [ ] No broken links
- [ ] All original content preserved
- [ ] Progressive disclosure working

### Context Tests

**Measure with token counter**:

Simple task (add keyword):
- Before: Count tokens in full context
- After: Count tokens in entry + relevant skill
- Target: 70%+ reduction

Medium task (generate post):
- Before: Full context
- After: Entry + skill + session
- Target: 60%+ reduction

Complex task (new category):
- Before: Full context
- After: Entry + multiple skills + arch doc + session
- Target: 40%+ reduction

---

## Risk Mitigation

### Before Each Phase

1. **Backup**
   ```bash
   # Create timestamped backup
   tar -czf backup-$(date +%Y%m%d).tar.gz CLAUDE.md .claude/
   ```

2. **Test current functionality**
   ```bash
   # Ensure everything works before changes
   /opt/homebrew/bin/hugo --minify
   pytest
   python scripts/topic_queue.py stats
   ```

### During Each Phase

1. **Keep original files until phase complete**
2. **Test after each major change**
3. **Document any deviations from plan**
4. **Create rollback points**

### After Each Phase

1. **Validate functionality (checklist above)**
2. **Test with real tasks**
3. **Get user feedback**
4. **Adjust next phase if needed**

---

## Success Metrics

### Phase 1 Targets

- [ ] Entry point: 200 lines (from 957)
- [ ] 7 focused docs created
- [ ] All content preserved
- [ ] No broken links

### Phase 2 Targets

- [ ] 4 skills created
- [ ] Progressive loading working
- [ ] Simple task context: 600 lines (from 2,778)
- [ ] Medium task context: 800 lines (from 2,778)

### Phase 3 Targets

- [ ] 4 agent files created
- [ ] Each agent: Clear scope
- [ ] WORKFLOW.md: 150 lines (from 582)
- [ ] Multi-agent workflow: No conflicts

### Phase 4 Targets

- [ ] Session state: 200 lines per session (from 536 growing)
- [ ] Archive mechanism working
- [ ] No state leak between sessions

### Overall Success

**Context Reduction**:
- Simple task: 84% reduction (2,778 → 450 lines)
- Medium task: 71% reduction (2,778 → 800 lines)
- Complex task: 55% reduction (2,778 → 1,250 lines)

**Maintainability**:
- Update prompt: Edit 400-line skill (vs. 957-line CLAUDE.md)
- Add agent: Create 250-line file (vs. modify 582-line WORKFLOW.md)
- Archive session: Auto-rotate (vs. 536-line growing file)

**Discovery**:
- Find info: 2 clicks max (vs. scanning 957 lines)
- Understand system: 200-line overview (vs. 957-line mixed doc)
- Load context: Only what's needed (vs. all 2,778 lines)

---

## Timeline

| Week | Phase | Hours | Status |
|------|-------|-------|--------|
| 1 | Split CLAUDE.md | 4-6 | Not started |
| 2 | Extract Skills | 6-8 | Not started |
| 3 | Separate Agents | 5-7 | Not started |
| 4 | Session State + Mistakes | 5-7 | Not started |
| **Total** | | **20-28** | |

---

## Next Action

**Start Phase 1**: Split CLAUDE.md

```bash
# 1. Create backup
cp CLAUDE.md CLAUDE.md.backup

# 2. Create docs directory
mkdir -p .claude/docs

# 3. Begin extraction (manual editing)
# - Open CLAUDE.md
# - Create new 200-line version (overview + quick commands)
# - Extract sections to .claude/docs/01-07
# - Update cross-references
# - Test navigation

# 4. Validate
/opt/homebrew/bin/hugo --minify
pytest
```

---

**Last Updated**: 2026-01-22
**Owner**: Jake Park
**Review**: After each phase completion
