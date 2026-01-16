# Jake's Tech Insights - 프로젝트 컨텍스트

## 프로젝트 개요

**프로젝트명**: Jake's Tech Insights
**유형**: Hugo 기반 다국어 기술 블로그
**언어**: 한국어(KO), 일본어(JA), 영어(EN) - 3개 언어 지원
**배포**: Cloudflare Pages (https://jakes-tech-insights.pages.dev)
**테마**: PaperMod (Git Submodule로 관리)

---

## 프로젝트 구조

```
jakes-tech-insights/
├── .claude/                    # Claude Code 설정
│   └── settings.local.json
├── archetypes/                 # Hugo 아케타입
│   └── default.md
├── content/                    # 콘텐츠
│   └── posts/
│       ├── en/first-post.md   # 영어 포스트
│       ├── ja/first-post.md   # 일본어 포스트
│       └── ko/first-post.md   # 한국어 포스트
├── layouts/                    # 커스텀 레이아웃
│   ├── index.html             # 메인 홈페이지 (커스텀 벤토 그리드)
│   ├── index-old.html         # 이전 버전 백업
│   └── _default/
│       ├── baseof.html        # 기본 베이스 템플릿
│       └── single.html        # 단일 포스트 페이지
├── public/                     # Hugo 빌드 결과물
├── themes/
│   └── PaperMod/              # PaperMod 테마 (submodule)
├── hugo.toml                   # Hugo 설정 파일
└── .gitmodules                # Git 서브모듈 설정
```

---

## Hugo 설정 (hugo.toml)

```toml
baseURL = 'https://jakes-tech-insights.pages.dev'
languageCode = 'ko-kr'
title = "Jake's Tech Insights"
theme = 'PaperMod'

[languages]
  [languages.ko]
    languageName = "Korean"
    weight = 1
    contentDir = "content"

  [languages.ja]
    languageName = "Japanese"
    weight = 2
    contentDir = "content"

  [languages.en]
    languageName = "English"
    weight = 3
    contentDir = "content"

[params]
  env = "production"
  ShowReadingTime = true
  ShowShareButtons = true
  ShowBreadCrumbs = true
  homeInfoParams.Title = "Welcome"
  homeInfoParams.Content = "Tech insights and trends"
```

### 주요 설정 포인트
- **다국어 지원**: 한국어를 기본(weight=1)으로 3개 언어 지원
- **단일 contentDir**: 모든 언어가 `content/` 디렉토리 공유, 경로로 언어 구분
- **PaperMod 테마**: 기본 테마로 사용하되 커스텀 레이아웃으로 오버라이드

---

## 커스텀 디자인

### 1. 홈페이지 (layouts/index.html)

**디자인 컨셉**: 다크 모드 벤토 그리드 레이아웃

#### 주요 특징
- **12컬럼 그리드 시스템**: 반응형 벤토 그리드 레이아웃
- **다크 사이버펑크 테마**:
  - 배경색: `#1a1a1a`
  - 서피스: `#242424`
  - 악센트 컬러: `#00ff88` (네온 그린)
  - 애니메이션 그리드 배경
- **폰트**:
  - 헤딩/로고: 'Space Mono' (monospace)
  - 본문: 'Instrument Sans' (sans-serif)

#### 레이아웃 구조 (12컬럼 그리드)

```
┌─────────────────────────────────────────────┐
│         Fixed Header (언어 스위처)           │
├─────────────────────────┬───────┬───────────┤
│  Featured Post (6칸)    │Latest │ AdSense   │
│                         │ (3칸) │  (3칸)    │
├─────┬─────┬─────┬───────┴───────┴───────────┤
│Card │Card │Card │ AdSense (3칸)             │
│(3칸)│(3칸)│(3칸)│                           │
├─────┴─────┴─────┴───────────┬───────────────┤
│  Trending Section (8칸)     │ Tags (4칸)    │
│  (2x2 그리드)                │               │
└─────────────────────────────┴───────────────┘
```

#### 주요 컴포넌트

1. **Fixed Header**
   - 로고: "JAKE'S INSIGHTS" (Space Mono)
   - 언어 스위처: EN / KO / JA
   - 상단 고정, 하단 네온 그린 보더

2. **Featured Post** (6칸)
   - 썸네일 영역 (200px 높이)
   - "Featured" 배지
   - 제목, 발췌문 (150자), 날짜, 카테고리
   - 호버 시: 상승 효과 + 네온 그린 글로우

3. **Latest Widget** (3칸)
   - 최신 5개 포스트 목록
   - 썸네일 (60x60) + 제목 + 날짜
   - 호버 시 왼쪽 이동 효과

4. **Small Cards** (각 3칸)
   - Featured 다음 3개 포스트
   - 날짜, 제목, 발췌문 (100자)
   - 호버 시 상승 효과

5. **Trending Section** (8칸)
   - 2x2 그리드 (4개 포스트)
   - 넘버링 (01-04)
   - 제목 + 날짜

6. **Popular Tags** (4칸)
   - 태그 클라우드 (최대 12개)
   - 포스트 수 배지
   - 호버 시 상승 효과

7. **Floating Menu** (우하단)
   - 원형 버튼 (네온 그린)
   - 메뉴 패널: Top, About, Tags, Archive

#### 반응형 디자인
- **Desktop (>1024px)**: 12컬럼 그리드
- **Tablet (768-1024px)**: 6컬럼 그리드
- **Mobile (<768px)**: 1컬럼 스택 레이아웃

#### 언어별 필터링
```go
{{ $currentLangPages := where .Site.RegularPages "Language.Lang" .Site.Language.Lang }}
```
- 현재 언어에 해당하는 페이지만 필터링하여 표시
- 언어 스위처: `/en/`, `/ko/`, `/ja/`

### 2. 포스트 페이지 (layouts/_default/single.html)

**디자인 컨셉**: 미니멀 다크 모드 읽기 페이지

#### 주요 특징
- **최대 너비 800px**: 가독성 최적화
- **다크 배경**: `#0a0a0a`
- **타이포그래피**:
  - 제목: 3rem (48px)
  - 본문: 1.125rem (18px)
  - 줄 높이: 1.8
- **H2 헤딩**: 네온 그린 악센트
- **링크**: 하단 보더 + 호버 페이드

#### 구조
1. **헤더**: 로고 + 홈 링크
2. **Article Header**: 제목, 날짜, 읽기 시간
3. **Content**: 마크다운 콘텐츠
4. **Back Link**: 홈으로 돌아가기 버튼

---

## 콘텐츠 구조

### 포스트 예시
```markdown
---
title: "First Post - AI Trends 2025"
date: 2025-01-16
draft: false
---

# AI Trends 2025

Hello! I'm Jake.
```

### 콘텐츠 규칙
- **경로**: `content/posts/{언어}/포스트명.md`
- **프론트매터**: title, date, draft 필수
- **이미지**: `image` 파라미터로 썸네일 지정 가능
- **카테고리**: `category` 파라미터로 카테고리 지정 가능

---

## 기술 스택

### Core
- **Hugo**: 정적 사이트 생성기
- **PaperMod Theme**: Git Submodule로 관리
- **Cloudflare Pages**: 배포 플랫폼

### 디자인
- **CSS**: 바닐라 CSS (CSS Variables 사용)
- **폰트**: Google Fonts (Space Mono, Instrument Sans)
- **컬러 스킴**: 다크 모드 (사이버펑크 스타일)

### 다국어
- **Hugo i18n**: 언어별 콘텐츠 자동 필터링
- **URL 구조**: `/ko/`, `/ja/`, `/en/`

---

## Git 관리

### 현재 상태
- **브랜치**: main
- **최신 커밋**: `0184062 Initial commit: Hugo site setup`
- **서브모듈**: `themes/PaperMod` (Git Submodule)

### 변경된 파일 (스테이징 대기 중)
```
M  public/404.html
M  public/categories/index.html
M  public/index.html
M  public/ja/404.html
M  public/ja/categories/index.html
M  public/ja/index.html
M  public/ja/tags/index.html
M  public/ko/404.html
M  public/ko/categories/index.html
M  public/ko/index.html
M  public/ko/tags/index.html
M  public/posts/en/first-post/index.html
M  public/posts/index.html
M  public/posts/ja/first-post/index.html
M  public/posts/ko/first-post/index.html
M  public/tags/index.html
?? layouts/
```

**주의**: `layouts/` 디렉토리가 새로 추가됨 (커스텀 레이아웃)

---

## 개발 워크플로우

### Hugo 명령어
```bash
# 개발 서버 실행
hugo server -D

# 빌드
hugo

# 다국어 빌드
hugo --buildFuture --buildDrafts
```

### 새 포스트 작성
```bash
# 한국어
hugo new content/posts/ko/새-포스트.md

# 일본어
hugo new content/posts/ja/新しい投稿.md

# 영어
hugo new content/posts/en/new-post.md
```

### 서브모듈 업데이트
```bash
git submodule update --remote themes/PaperMod
```

---

## 주요 결정 사항 및 디자인 철학

### 1. 커스텀 레이아웃을 선택한 이유
- PaperMod 테마는 훌륭하지만 매거진 스타일 홈페이지가 필요했음
- 벤토 그리드 레이아웃으로 콘텐츠를 시각적으로 구성
- AdSense 슬롯을 자연스럽게 통합

### 2. 다크 사이버펑크 테마
- 기술 블로그에 어울리는 현대적인 느낌
- 네온 그린(`#00ff88`)으로 강조 효과
- 애니메이션 그리드 배경으로 역동성 부여

### 3. 단일 contentDir 구조
- 모든 언어가 `content/` 공유
- 경로로 언어 구분 (`posts/ko/`, `posts/ja/`, `posts/en/`)
- 유지보수 편의성

### 4. 반응형 우선 설계
- Desktop: 12컬럼 그리드
- Tablet: 6컬럼 그리드
- Mobile: 1컬럼 스택
- 모든 디바이스에서 최적의 가독성

---

## 향후 작업 예정

### 기능 추가
- [ ] AdSense 통합
- [ ] 검색 기능
- [ ] 다크/라이트 모드 토글
- [ ] 포스트 공유 기능 확장
- [ ] RSS 피드 커스터마이징
- [ ] About 페이지
- [ ] Archive 페이지
- [ ] 카테고리별 페이지

### 콘텐츠
- [ ] 다국어 콘텐츠 확충
- [ ] 카테고리 체계 정립
- [ ] 태그 시스템 구축

### 최적화
- [ ] 이미지 최적화
- [ ] 빌드 성능 개선
- [ ] SEO 메타 태그 추가
- [ ] Open Graph 설정

---

## 문제 해결 가이드

### 언어별 콘텐츠가 안 보일 때
```go
{{ $currentLangPages := where .Site.RegularPages "Language.Lang" .Site.Language.Lang }}
```
- 포스트 경로가 `/posts/{언어}/` 형식인지 확인
- 프론트매터에 `draft: false` 확인

### 스타일이 안 먹힐 때
- `layouts/index.html`이 `{{ define "main" }}`로 시작하는지 확인
- `baseof.html`과 연동 확인

### 빌드 오류
```bash
# 캐시 삭제
rm -rf public/
rm .hugo_build.lock

# 재빌드
hugo
```

---

## 참고 링크

- [Hugo 공식 문서](https://gohugo.io/documentation/)
- [PaperMod 테마](https://github.com/adityatelange/hugo-PaperMod)
- [Hugo 다국어 가이드](https://gohugo.io/content-management/multilingual/)
- [Cloudflare Pages 문서](https://developers.cloudflare.com/pages/)

---

## 마지막 업데이트

**날짜**: 2026-01-16
**작업자**: Jake
**버전**: v1.0 (초기 셋업 완료)
