# Agent Work Report Template

This template is used by all agents (CTO, Designer, QA) to report work completion to Master agent.

**Important**: All reports must be written in **English**.

---

## CTO Work Report Template

```markdown
# CTO Work Report: {Task Name}

**Date**: {YYYY-MM-DD}
**Agent**: CTO Agent
**Branch**: feature/{branch-name} (if applicable)

## Summary
{One-line summary of the work completed}

## Changes Made

### Modified Files
- `{file path}`: {description of changes}
- `{file path}`: {description of changes}

### Added Files
- `{file path}`: {reason for addition}

### Deleted Files
- `{file path}`: {reason for deletion}

## Technical Details

### Architecture Changes
{If architecture was modified, describe changes}

### Performance Impact
- Build time: {before} → {after} ({improvement}%)
- Memory usage: {before} → {after}
- API calls: {count and type}

### Dependencies
- Added: {package name} ({version}) - {reason}
- Updated: {package name} ({old version} → {new version})
- Removed: {package name} - {reason}

## Test Results
- Build: {Success/Failed}
- Tests: {Passed/Failed} ({N}/{Total})
- Performance benchmarks: {results if any}

## Important Notes
{Critical information Master needs to know}

### Breaking Changes
{List any breaking changes or migration steps needed}

### Configuration Updates
{List any .env, config files, or settings that need updating}

## Recommended Commit Message
```
{type}: {summary}

{detailed description}

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Next Steps
{Follow-up tasks or recommendations if any}

## Related Documentation
- {Link to ADR if applicable}
- {Link to updated docs}
```

---

## Designer Work Report Template

```markdown
# Designer Work Report: {Task Name}

**Date**: {YYYY-MM-DD}
**Agent**: Designer Agent
**Branch**: feature/{branch-name} (if applicable)

## Summary
{One-line summary of the work completed}

## Changes Made

### Modified Files
- `{file path}`: {description of changes}
- `{file path}`: {description of changes}

### Added Files
- `{file path}`: {reason for addition}

### Design Elements

#### Colors
- Added: {color name} ({hex code})
- Modified: {color name} ({old hex} → {new hex})

#### Layout
- {Component name}: {layout changes}
- Responsive breakpoints: {changes}

#### Typography
- Font family: {changes if any}
- Font sizes: {changes}
- Line heights: {changes}

#### Components
- New components: {list}
- Modified components: {list}

## Validation Results

### Responsive Testing
- Mobile (375px): {Pass/Issues}
- Mobile (414px): {Pass/Issues}
- Tablet (768px): {Pass/Issues}
- Tablet (1024px): {Pass/Issues}
- Desktop (1440px): {Pass/Issues}
- Desktop (1920px): {Pass/Issues}

### Accessibility Check
- Color contrast: {ratio} ({WCAG level})
- Keyboard navigation: {Pass/Issues}
- Screen reader: {Pass/Issues}
- Focus indicators: {Pass/Issues}
- ARIA attributes: {Pass/Issues}

### Performance Check
- Lighthouse score: {score}/100 ({before} → {after})
- First Contentful Paint (FCP): {time}s
- Cumulative Layout Shift (CLS): {score}
- Largest Contentful Paint (LCP): {time}s

### Browser Testing
- Chrome: {Pass/Issues}
- Firefox: {Pass/Issues}
- Safari: {Pass/Issues}
- Edge: {Pass/Issues}

## Screenshots
{Description of before/after or path to screenshot files}

## Important Notes
{Critical information Master needs to know}

### User Impact
{Any user-facing changes or migration notes}

### Known Issues
{Any limitations or known issues}

## Recommended Commit Message
```
{type}: {summary}

{detailed description}

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Next Steps
{Follow-up tasks or recommendations if any}

## Related Documentation
- {Link to design system updates}
- {Link to component documentation}
```

---

## QA Work Report Template

```markdown
# QA Work Report: {Task Name}

**Date**: {YYYY-MM-DD}
**Agent**: QA Agent
**Branch**: feature/{branch-name} (if applicable)

## Summary
{One-line summary of the work completed}

## Changes Made

### Added Tests
- `{test file}`: {N} tests added
  - {test_function_name}: {description}
  - {test_function_name}: {description}

### Modified Tests
- `{test file}`: {description of modifications}

### Added Fixtures
- `{fixture_name}`: {description and scope}

## Test Results

### Execution Results
- Total tests: {N}
- Passed: {N} ({percentage}%)
- Failed: {N} ({percentage}%)
- Skipped: {N}
- Execution time: {X.XX}s

### Test Details
```
{Paste pytest output summary}
```

### Coverage

#### Overall Coverage
- Before: {X}%
- After: {Y}%
- Change: +{Z}%

#### Module Coverage
- `{module name}`: {X}% (before: {Y}%)
- `{module name}`: {X}% (before: {Y}%)

#### Untested Lines
- `{file}`: Lines {line numbers}
- `{file}`: Lines {line numbers}

## Test Cases

### Happy Path Tests
- {test description}: {result}
- {test description}: {result}

### Edge Cases
- {edge case description}: {result}
- {edge case description}: {result}

### Error Handling
- {exception type}: {test result}
- {exception type}: {test result}

### Integration Tests (if applicable)
- {integration scenario}: {result}

## Important Notes
{Critical information Master needs to know}

### Test Failures (if any)
{Description of any failing tests and investigation results}

### Coverage Gaps
{Areas that still need test coverage}

### Performance Notes
{Any slow tests or performance concerns}

## Recommended Commit Message
```
{type}: {summary}

{detailed description}

Coverage: {before}% → {after}% (+{change}%)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Next Steps
{Follow-up tasks or recommendations if any}

## Related Documentation
- {Link to test documentation}
- {Link to coverage reports}
```

---

## Report File Naming Convention

### File Location
- **Active work**: `.claude/reports/active/{agent}-{task-name}-{YYYY-MM-DD}.md`
- **Archived**: `.claude/reports/archive/{YYYY-MM}/{agent}-{task-name}-{YYYY-MM-DD}.md`

### Examples
```
.claude/reports/active/cto-optimize-build-2026-01-20.md
.claude/reports/active/designer-dark-mode-2026-01-20.md
.claude/reports/active/qa-test-coverage-2026-01-20.md
```

---

## Report Lifecycle

### 1. During Work
- Agent creates report in `.claude/reports/active/`
- Updates report as work progresses
- Finalizes report when work complete

### 2. User Notification
Agent notifies user:
```
Work completed.

📋 Report: .claude/reports/active/{agent}-{task-name}-{YYYY-MM-DD}.md

Please pass this report to Master agent to decide on commit/push.
```

### 3. After Master Review
- Master reviews report
- If approved, Master commits changes
- Master archives report to `.claude/reports/archive/YYYY-MM/`

### 4. Cleanup
- Reports older than 3 months can be deleted from archive
- Active directory should be kept clean (move to archive after commit)

---

## Commit Message Format

All agents should recommend commit messages in this format:

```
{type}: {short summary}

{detailed description}

- Change 1
- Change 2
- Change 3

{Additional context if needed}

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes bug nor adds feature
- `perf`: Performance improvement
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

**CTO**:
```
perf: Optimize build time by 45% with caching

- Add pip package caching in GitHub Actions
- Implement Hugo build artifact caching
- Configure cache invalidation strategy

Build time reduced from 45s to 25s.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Designer**:
```
feat: Add dark mode support with system preference detection

- Implement CSS custom properties for theming
- Add theme toggle button in header
- Respect prefers-color-scheme media query
- Ensure WCAG AAA contrast in both modes

All color contrast ratios exceed 7:1.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**QA**:
```
test: Increase coverage to 72% (+14%)

- Add 18 new unit tests for topic_queue module
- Add integration tests for content workflow
- Improve fixture management for faster execution

Coverage breakdown:
- topic_queue.py: 60% → 75%
- content_generator.py: 45% → 70%
- image_processor.py: 50% → 65%

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

**Last Updated**: 2026-01-20
**Version**: 1.0
**Used By**: CTO, Designer, QA agents
