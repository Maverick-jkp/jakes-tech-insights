# Changelog - Hugo Operations Skill

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-01-24

### Added
- **Dependencies section** - Hugo system requirements and installation guide
- Hugo version verification command
- Python package requirements (pyyaml for validation)
- "No API costs" notice for cost transparency

### Changed
- **Hugo path emphasis** - Critical warning about full path usage
- Installation instructions with Homebrew command

### Impact
- **Setup clarity** - New users know exactly how to install Hugo
- **Error prevention** - Clear guidance on Hugo path usage prevents common errors
- **Cost transparency** - Explicitly states no API costs

## [1.1.0] - 2026-01-24

### Added
- **Skill Boundaries** section with Hugo-specific responsibilities
- "When to Use This Skill" with explicit activation triggers
- "Advanced Topics" section with references to detailed resources
- Version tracking system (CHANGELOG.md)

### Changed
- **YAML frontmatter**: Removed non-standard fields (`triggers`, `examples`)
- **description**: Enhanced with Hugo-specific details and critical path info
- **File size**: Reduced from 618 lines → 226 lines (63% reduction)
- Moved advanced content to `resources/` (on-demand loading)

### Removed
- Detailed Hugo configuration (moved to `resources/configuration.md`)
- Template customization guide (moved to `resources/templates.md`)
- Advanced troubleshooting (moved to `resources/troubleshooting.md`)
- Performance optimization details (moved to `resources/performance.md`)

### Expected Impact
- Token usage: 50% reduction for basic Hugo operations
- Faster skill loading in parallel execution
- Easier maintenance with modular structure
- On-demand access to advanced topics

## [1.0.0] - 2026-01-23

### Added
- Initial Hugo operations implementation
- Development server support (live reload)
- Production build with minification
- Multilingual site operations (EN/KO/JA)
- Hugo configuration management
- Template troubleshooting
- Cloudflare Pages deployment integration

### Features
- Full path Hugo support (`/opt/homebrew/bin/hugo`)
- Common server options documentation
- Build performance metrics
- Content structure guidelines

---

**Maintained By**: Jake's Tech Insights project
