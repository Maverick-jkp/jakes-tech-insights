# Changelog - Content Generation Skill

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-24

### Added
- **Skill Boundaries** section with clear responsibility definitions
- "When to Use This Skill" with explicit activation conditions
- "Defer to other skills" guidance to prevent overlap

### Changed
- **YAML frontmatter**: Removed non-standard fields (`triggers`, `examples`)
- **description**: Enhanced with detailed use cases and activation criteria
- Moved examples from frontmatter to "When to Use" section

### Expected Impact
- Skill recognition accuracy: 70% → 95%
- Reduced skill conflicts with boundary definitions
- Clearer activation criteria for Claude

## [1.0.0] - 2026-01-23

### Added
- Initial skill implementation
- Draft + Editor agent pipeline
- Multilingual support (EN/KO/JA)
- Quality standards (800-2000 words)
- Topic queue integration
- AI phrase blacklist
- SEO optimization

### Features
- Automated content generation from trending keywords
- Two-agent pipeline (Draft → Editor)
- Frontmatter creation with metadata
- Image integration via Unsplash API
- Quality validation integration

---

**Maintained By**: Jake's Tech Insights project
