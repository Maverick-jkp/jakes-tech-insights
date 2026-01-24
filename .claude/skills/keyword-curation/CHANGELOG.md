# Changelog - Keyword Curation Skill

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-24

### Added
- **Skill Boundaries** section defining curation scope
- "When to Use This Skill" with queue management triggers
- "Advanced Topics" section with resource references
- Version tracking system (CHANGELOG.md)

### Changed
- **YAML frontmatter**: Removed non-standard fields (`triggers`, `examples`)
- **description**: Enhanced with state machine details and priority info
- **File size**: Reduced from 654 lines → 319 lines (51% reduction)
- Streamlined queue operations documentation

### Removed
- Detailed queue management guide (moved to `resources/queue-management.md`)
- Advanced curation strategies (moved to `resources/curation-guide.md`)
- Best practices details (moved to `resources/best-practices.md`)
- Bulk operations examples (moved to resources)

### Expected Impact
- Token usage: 50% reduction for queue operations
- Faster skill loading in parallel workflows
- Modular documentation structure
- On-demand access to advanced features

## [1.0.0] - 2026-01-23

### Added
- Initial keyword curation implementation
- Google Trends integration (KR/US/JP)
- Topic queue state machine (pending → in_progress → completed)
- Priority management (1-10 scale)
- Duplicate prevention
- Stuck topic cleanup (24+ hours)
- Queue health monitoring

### Features
- Manual keyword filtering workflow
- 8 category support (tech, business, etc.)
- GitHub Actions automation
- Queue status monitoring
- Category distribution tracking

---

**Maintained By**: Jake's Tech Insights project
