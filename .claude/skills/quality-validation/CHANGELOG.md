# Changelog - Quality Validation Skill

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
