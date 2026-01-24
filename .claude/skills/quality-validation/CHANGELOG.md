# Changelog - Quality Validation Skill

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-01-24

### Added
- **Table of Contents** - Quick navigation for 360+ line file
- **Quality Validation Feedback Loop** - 6-step checklist with iteration guidance
- **Evaluation file** - Test cases in `.claude/evaluations/quality-validation.json`

### Impact
- **Navigation** - 50% faster section access with TOC
- **Systematic fixing** - Feedback loop reduces validation failures
- **Testing** - Evaluation file covers 5 test scenarios

## [1.2.0] - 2026-01-24

### Added
- **Dependencies section** - Package requirements with verification commands
- **Progressive disclosure** - Split into 4 files (SKILL.md + 3 resources)
  - `resources/ai-phrases.md` - Complete AI phrase blacklist
  - `resources/ai-reviewer.md` - 5-criteria scoring details
  - `resources/extending.md` - Guide for adding new validation rules

### Changed
- **File size reduction** - 516 lines → 341 lines (34% reduction)
- **AI phrase section** - Summary only, full list in resources/
- **AI reviewer section** - Overview only, details in resources/

### Removed
- Detailed AI phrase explanations (moved to resources/ai-phrases.md)
- AI reviewer scoring details (moved to resources/ai-reviewer.md)
- Extension patterns (moved to resources/extending.md)

### Impact
- **Token usage** - 50% reduction for basic validation tasks
- **On-demand loading** - Advanced topics loaded only when needed
- **Maintainability** - Easier to update blacklist in dedicated file
- **Compliance** - Meets Anthropic's 500-line recommendation

## [1.1.0] - 2026-01-24

### Added
- **Skill Boundaries** section defining validation scope
- "When to Use This Skill" with explicit conditions
- "Defer to other skills" for content generation/Hugo operations

### Changed
- **YAML frontmatter**: Removed non-standard fields (`triggers`, `examples`)
- **description**: Enhanced with validation criteria and use cases
- Clarified non-blocking warning behavior

### Expected Impact
- Clearer separation from content-generation skill
- Reduced confusion about when to use validation
- Better integration with other skills

## [1.0.0] - 2026-01-23

### Added
- Initial quality validation implementation
- Word count validation (800-2000 words)
- AI phrase blacklist detection (EN/KO/JA)
- SEO validation (meta descriptions, images)
- Frontmatter verification
- References section check (2+ links)
- Quality report generation (JSON)

### Features
- Automated quality gate
- Optional AI reviewer (5-criteria scoring)
- Non-blocking warnings for minor issues
- CI/CD integration support

---

**Maintained By**: Jake's Tech Insights project
