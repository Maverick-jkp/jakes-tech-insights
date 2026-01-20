# 🤖 Jake's Tech Insights - Automated Blog System

완전 자동화된 다국어 블로그 플랫폼 with AI Content Generation

[![Hugo](https://img.shields.io/badge/Hugo-0.123.0-FF4088?logo=hugo)](https://gohugo.io/)
[![Claude API](https://img.shields.io/badge/Claude-Sonnet%204.5-8B5CF6)](https://anthropic.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-2088FF?logo=github-actions)](https://github.com/features/actions)
[![Cloudflare Pages](https://img.shields.io/badge/Cloudflare-Pages-F38020?logo=cloudflare)](https://pages.cloudflare.com/)

## 🎯 Overview

**Jake's Tech Insights**는 AI 기반 콘텐츠 생성부터 품질 검증, 자동 배포까지 95% 자동화된 블로그 시스템입니다.

### Key Features

- 🌍 **3개 언어 동시 지원**: English, 한국어, 日本語
- 🤖 **완전 자동 생성**: Topic Queue → Draft → Edit → Review → PR
- ✅ **품질 보증**: Quality Gate + AI Self-Review (5-criteria scoring)
- 📊 **상세 리포트**: Word count, AI phrase detection, SEO metrics
- 🔄 **자동 배포**: GitHub Actions → Cloudflare Pages
- 📈 **확장 가능**: Priority queue, retry mechanism, stuck topic cleanup

## 🏗️ Architecture

```
┌─────────────────┐
│  Topic Queue    │  State Machine (pending → in_progress → completed)
│  (18 topics)    │  Priority-based reservation
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Content Gen     │  Draft Agent → Editor Agent (Claude Sonnet 4.5)
│ (generate_posts)│  Language-specific prompts (EN/KO/JA)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Quality Gate    │  Word count (900-1800), AI phrases, SEO
│ (quality_gate)  │  FAIL/WARN criteria
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ AI Reviewer     │  5-criteria scoring (Authenticity, Value, etc.)
│ (ai_reviewer)   │  APPROVE/REVISE/REJECT recommendations
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ GitHub PR       │  Auto-create PR with reports
│ (Actions)       │  Human approval required
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Cloudflare      │  Automatic deployment on merge
│ Pages           │  https://jakes-tech-insights.pages.dev
└─────────────────┘
```

## 🚀 Quick Start

### 1. Setup (First Time)

```bash
# Clone repository
git clone https://github.com/Maverick-jkp/jakes-tech-insights.git
cd jakes-tech-insights

# Install dependencies
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY='your-claude-api-key'

# Check queue stats
python scripts/topic_queue.py stats
```

### 2. Generate Content Locally

```bash
# Generate 1 post for testing
python scripts/generate_posts.py --count 1

# Run quality checks
python scripts/quality_gate.py

# Run AI review
python scripts/ai_reviewer.py

# View reports
cat quality_report.json
cat ai_review_report.json
```

### 3. Setup GitHub Automation

**워크플로우 설정은 [SETUP_WORKFLOWS.md](SETUP_WORKFLOWS.md) 참고** ⭐

핵심 단계:
1. GitHub → Settings → Secrets에 `ANTHROPIC_API_KEY` 추가
2. GitHub → Actions에서 `daily-content.yml` 생성
3. 수동 실행으로 테스트
4. 매일 자동 실행 활성화

## 📁 Project Structure

```
jakes-tech-insights/
├── .github/workflows/        # GitHub Actions workflows
│   └── daily-content.yml     # Daily content generation (create on GitHub)
├── content/                  # Hugo content
│   ├── en/                   # English posts
│   ├── ko/                   # Korean posts
│   └── ja/                   # Japanese posts
├── data/
│   └── topics_queue.json     # Topic queue state
├── scripts/
│   ├── topic_queue.py        # Queue management
│   ├── generate_posts.py     # Content generation (Draft + Editor)
│   ├── quality_gate.py       # Quality validation
│   ├── ai_reviewer.py        # AI self-review
│   └── test_queue.py         # Queue system tests
├── themes/PaperMod/          # Hugo theme
├── config.yml                # Hugo config
├── PROJECT_CONTEXT.md        # Detailed documentation
├── SETUP_WORKFLOWS.md        # Workflow setup guide
└── README.md                 # This file
```

## 🛠️ Scripts Usage

### Keyword Curation (Weekly)

```bash
# Generate keyword candidates (recommended: weekly)
python scripts/keyword_curator.py

# Custom count
python scripts/keyword_curator.py --count 10

# Interactive selection (5 minutes)
# - Review candidates
# - Select by number (e.g., 1,3,5,7)
# - Add to queue (Trend:Evergreen = 3:7)
```

**See [KEYWORD_CURATION_GUIDE.md](docs/KEYWORD_CURATION_GUIDE.md) for details**

### Topic Queue Management

```bash
# View statistics
python scripts/topic_queue.py stats

# Reserve topics (testing)
python scripts/topic_queue.py reserve 3

# Cleanup stuck topics (24+ hours in progress)
python scripts/topic_queue.py cleanup 24

# Add new topic (manual)
from topic_queue import add_topic
add_topic("Keyword", "tech", "en", priority=8)
```

### Content Generation

```bash
# Generate 3 posts (default)
python scripts/generate_posts.py --count 3

# Generate specific topic (testing)
python scripts/generate_posts.py --topic-id 001-en-tech-ai-coding

# Environment variable required
export ANTHROPIC_API_KEY='your-key'
```

### Quality Checks

```bash
# Run quality gate (normal mode)
python scripts/quality_gate.py

# Strict mode (warnings become failures)
python scripts/quality_gate.py --strict

# Review specific file
python scripts/ai_reviewer.py --file content/en/tech/post.md
```

### Local Development

```bash
# Start Hugo server
hugo server -D

# Build site
hugo

# View at http://localhost:1313
```

### Pre-commit Hook (Automatic Validation)

A Git pre-commit hook automatically validates `topics_queue.json` before each commit:

```bash
# The hook runs automatically when you commit
git commit -m "Update topics"

# If validation fails, commit is blocked:
🔍 Running pre-commit validation...
📋 Validating topics_queue.json...
❌ Topic 'invalid-topic' has errors:
   - Invalid keyword: Keyword contains invalid characters
❌ Error: topics_queue.json validation failed

# Fix issues and try again
```

**Hook location**: `.git/hooks/pre-commit` (already installed)

**To bypass** (emergency only): `git commit --no-verify`

## 📊 Quality Standards

### Content Requirements
- **Word count**: 800-2000 words (EN/KO), 3000-7500 chars (JA)
- **Structure**: 3-4 main sections (## headings)
- **Tone**: Professional but friendly
- **Paragraphs**: Short and concise (2-4 sentences each)
- **Links**: 2+ external references
- **SEO**: Natural keyword integration (5-7 times)

### AI Phrase Blacklist
- English: "revolutionary", "game-changer", "cutting-edge", "it's important to note"
- Korean: "물론", "혁신적", "게임체인저"
- Japanese: "もちろん", "革新的", "ゲームチェンジャー"

### AI Review Criteria
1. **Authenticity** (1-10): Natural human tone
2. **Value** (1-10): Practical insights
3. **Engagement** (1-10): Interesting structure
4. **Technical Accuracy** (1-10): Correct facts
5. **SEO Quality** (1-10): Good keywords

**Thresholds**:
- APPROVE: avg ≥ 8.0
- REVISE: avg 6.0-7.9
- REJECT: avg < 6.0

## 🔄 Automation Workflow

### Daily Schedule (GitHub Actions)
- **9 AM UTC** (6 PM KST): Auto-generate 3 posts
- Quality gate runs automatically
- AI review provides recommendations
- Creates PR for human approval

### Cost Optimization
**Token Settings**:
- Draft generation: 12000 max_tokens (ensures completion for all languages)
- Editor refinement: 12000 max_tokens
- Structure-based: 3-4 sections (no strict word count limits)
- Expected output: 800-2,000 words (EN/KO), 3,000-7,500 chars (JA)
- Est. cost: ~$0.09/post × 3 posts/day = $8.1/month

**Scaling Strategy**:
- Week 1-2: 1 post/day ($2.7/month) - Manual review
- Week 3-4: 3 posts/day ($8.1/month) - Semi-auto
- Month 2+: Adjust based on quality/budget

### Manual Trigger
1. Go to **Actions** tab on GitHub
2. Select **Daily Content Generation**
3. Click **Run workflow**
4. Set number of posts (default: 3)
5. Review PR when complete

## 📈 Current Status

### Queue Stats
- **Total topics**: 18
- **Completed**: 2 (EN AI Coding, KO AI Coding)
- **In Progress**: 7
- **Pending**: 9

### Coverage
- **Languages**: EN (6), KO (6), JA (6)
- **Categories**: Tech (6), Business (6), Lifestyle (6)
- **Priority Range**: 6-8

### Test Results
- ✅ First AI-generated post: Digital Minimalism (1,200+ words)
- ✅ Quality checks: No AI phrases detected
- ✅ Queue system: State transitions working
- ✅ Retry mechanism: Failures handled gracefully
- ✅ max_tokens optimization: 4000 → 8000 → 12000
- ✅ Tone optimization: Toss style (KO), Medium style (EN), Natural (JA)
- ✅ Quality Gate updated: 800-2,000 words, 3,000-7,500 chars (JA)
- ✅ Structure-based constraints: 3-4 sections (removed strict word counts)
- ✅ Prompt Caching: 20-25% cost reduction ($8.1 → $6.3/month)
- ✅ Unsplash API: Featured images auto-generated with credits
- ✅ Keyword Curation: Semi-automated with human filtering (5 min/week)

## 🎓 Documentation

- **[PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)**: 전체 시스템 아키텍처, 구현 세부사항
- **[SETUP_WORKFLOWS.md](SETUP_WORKFLOWS.md)**: GitHub Actions 설정 가이드
- **[KEYWORD_STRATEGY.md](docs/KEYWORD_STRATEGY.md)**: 키워드 선택 전략 (Decision-stage focus)
- **[KEYWORD_CURATION_GUIDE.md](docs/KEYWORD_CURATION_GUIDE.md)**: 주간 키워드 큐레이션 가이드
- **[WINDOWS_SETUP.md](docs/WINDOWS_SETUP.md)**: 윈도우 환경 설정 가이드 (Git, GitHub CLI, PATH)
- **[.claude/PROJECT_CONTEXT.md](.claude/PROJECT_CONTEXT.md)**: 버그 수정 이력, 자동화 전략

## 🔐 Required Secrets

GitHub Repository Settings → Secrets → Actions:

```
ANTHROPIC_API_KEY=your-claude-api-key-here
UNSPLASH_ACCESS_KEY=your-unsplash-access-key-here
```

## 🚦 Development Roadmap

### ✅ Phase 1: Foundation (Complete)
- [x] Hugo site setup with PaperMod theme
- [x] Multi-language support (EN/KO/JA)
- [x] Category system (Tech/Business/Lifestyle)
- [x] Navigation and UI fixes

### ✅ Phase 2: Automation Core (Complete)
- [x] Topic queue with state machine
- [x] Content generation (Draft + Editor agents)
- [x] Quality gate system
- [x] AI self-review agent
- [x] GitHub Actions workflow

### ✅ Phase 3: Enhancement (Complete)
- [x] Workflow setup on GitHub
- [x] Test full pipeline end-to-end
- [x] Monitor quality metrics (KO/JA word count issue identified)
- [x] max_tokens optimization (4000 → 8000 → 12000)
- [x] Tone optimization (Toss/Medium/Natural styles)
- [x] Quality Gate criteria updated (800-2,000 words for flexibility)
- [x] Structure-based prompts (removed strict word count limits)

### 📋 Phase 4: Optimization (Complete)
- [x] Prompt Caching for cost reduction (20-25% cost savings)
- [x] Image auto-generation (Unsplash API integration)
- [x] Keyword curation system (semi-automated with human filtering)
- [ ] A/B testing for titles (optional)
- [ ] n8n integration for monitoring (optional)

### 💰 Phase 5: Monetization (Future)
- [ ] Custom domain setup
- [ ] 20-30 manual quality posts
- [ ] SEO optimization
- [ ] Google AdSense application
- [ ] Gradual scaling (1→3→9 posts/day)

## 💡 Tips & Best Practices

### For Quality Content
1. Start with 1-2 posts/day
2. Review AI-generated content manually
3. Add personal touch (1-2 sentences)
4. Use real examples and data
5. Add images from Unsplash

### For SEO
1. Focus on long-tail keywords
2. Natural keyword density (5-7 times)
3. Proper meta descriptions (120-160 chars)
4. Internal linking between posts
5. Regular publishing schedule

### For Scaling
1. **Month 1-3**: 1-2 posts/day (manual review)
2. **Month 4-6**: 3-5 posts/day (semi-auto)
3. **Month 7+**: 9 posts/day (full auto)

## 🐛 Troubleshooting

### Hugo server not showing new posts
```bash
# Restart Hugo server
pkill -f hugo
hugo server -D
```

### Queue stuck topics
```bash
# Clean up topics stuck for 24+ hours
python scripts/topic_queue.py cleanup 24
```

### Workflow permission error
- Workflows must be created on GitHub directly
- See [SETUP_WORKFLOWS.md](SETUP_WORKFLOWS.md)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Maverick-jkp/jakes-tech-insights/issues)
- **Docs**: [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)
- **Live Site**: https://jakes-tech-insights.pages.dev

## 📜 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- **Hugo**: Static site generator
- **PaperMod**: Beautiful Hugo theme
- **Claude API**: AI content generation
- **GitHub Actions**: Free CI/CD
- **Cloudflare Pages**: Free hosting

---

**Built with 🤖 AI + ❤️ Human Touch**

*Last updated: 2026-01-17*
*Version: 3.3 (Day 6 - Monetization Optimization)*

## 🔍 Recent Changes

**2026-01-17 (v3.3)**:
- **Monetization Features**: Related Posts (2-3x pageviews), Table of Contents, References section
- **Category Expansion**: Added Society (🌍) and Entertainment (🎬) for broader content coverage
- **Archives Page**: Unified "All Posts" view across all 3 languages
- **Hero Images**: Featured image now displays at top of post body (Medium/Substack style)
- **6 New Posts**: Total posts 29 → 38 (EN/KO/JA Business & Lifestyle topics)
- **Result**: Ready for AdSense application with optimized engagement features

**2026-01-17 (v3.2)**:
- **Writing Quality Upgrade**: Enhanced prompts with ChatGPT's "human-touch" strategies
- **Hooking Elements**: Problem-driven openings, failure cases, authenticity markers
- **Decision-Stage Focus**: "What to avoid" as much as "What to do"
- **Real Examples**: Specific companies/stats, not abstract "many companies..."
- **All Languages**: EN/KO/JA prompts upgraded with same strategies

**2026-01-17 (v3.1)**:
- **Bug Fix**: Added timezone (+09:00) to all post dates - fixed "future post" issue on production
- **Image Upgrade**: Replaced SVG placeholders with real Unsplash photos (14 posts)
- **New Script**: fetch_images_for_posts.py for batch image downloads
- **Result**: All thumbnails now display correctly on production site

**2026-01-17 (v3.0)**:
- **Phase 4.3**: Keyword curation system (semi-automated, human-filtered)
- **keyword_curator.py**: Weekly 5-minute workflow for quality keywords
- **Strategy docs**: KEYWORD_STRATEGY.md + KEYWORD_CURATION_GUIDE.md
- **Topic queue**: Enhanced with trend/evergreen support
- **Phase 4**: Complete (Optimization phase finished)

**2026-01-17 (v2.9)**:
- **Phase 4.1**: Prompt Caching (20-25% cost reduction)
- **Phase 4.2**: Unsplash API integration (auto featured images + credits)
- **Quality Gate**: Image check added (WARNING only)
- **Cost**: $6.3/month (down from $8.1/month with caching)

**2026-01-17 (v2.8)**:
- **Structure-based prompts**: Removed strict word count limits → 3-4 sections structure
- **Editor behavior**: Changed from "increase length" to "maintain length"
- **Quality Gate**: 800-2,000 words (EN/KO), 3,000-7,500 chars (JA)
- **Rationale**: Word count limits caused AI to cut off or exceed - structure is more natural

**2026-01-17 (v2.7)**:
- **Monetization focus**: Optimized for completion rate & engagement
- **max_tokens**: 8000 → 12000 (prevents truncation)
- **Tone optimization**: Toss style (KO), Medium/Substack (EN), Natural (JA)
- **Cost**: ~$0.09/post ($8.1/month for 3 posts/day)

**2026-01-16 (v2.6)**:
- Fixed KO/JA word count issue (794 → target 1,200+)
- Increased max_tokens: 4000 → 8000
- Added cost optimization strategy

**2026-01-16 (v2.5)**:
- Completed Day 4-5 automation
- Quality Gate + AI Reviewer implemented
- GitHub Actions workflow created
- Full pipeline tested
