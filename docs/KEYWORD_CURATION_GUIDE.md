# Keyword Curation Guide

## 개요

**keyword_curator.py**는 KEYWORD_STRATEGY.md에 정의된 전략에 따라 키워드 후보를 생성하는 스크립트입니다.

주 1회 5분 투자로 고품질 키워드를 확보하여 자동화 블로그의 품질을 유지합니다.

## 핵심 원칙

> **트렌드는 자동화의 입력값이 아니라, 사람이 해석해야 하는 원재료다.**

- Claude API가 15개 후보 생성 (자동)
- 인간이 5분 필터링 (수동, 필수)
- "자동화 냄새" 제거

## 실행 방법

### 1. 기본 실행 (주 1회)

```bash
# 15개 키워드 후보 생성 (기본값)
python scripts/keyword_curator.py
```

### 2. 실행 흐름

```
1. Claude API 호출 → 15개 후보 생성
2. 언어별 그룹화 표시 (EN 5개, KO 5개, JA 5개)
3. Interactive 선택
   - 숫자 입력 (예: 1,3,5,7,10)
   - 'all' 입력하면 전부 추가
   - 'q' 입력하면 취소
4. 선택된 키워드를 topic queue에 추가
5. 통계 표시
```

### 3. 출력 예시

```
============================================================
  📋 Keyword Candidates
============================================================

[English]
------------------------------------------------------------

1. 🔥 Cursor AI vs GitHub Copilot: 6 months later
   Category: tech | Competition: 🟢 low
   Intent: 실제 장기 사용 후 선택 기준을 찾고 있음
   Angle: 실제 사용 경험 기반 비교 + 팀 생산성 관점
   Why: Decision stage 키워드, 경쟁 낮음, 멀티툴 사용자 많음...

2. 🌲 Remote work tools that failed in Japanese companies
   Category: business | Competition: 🟢 low
   Intent: 문화적 차이로 인한 실패 사례 학습
   Angle: 언어/지역 관점 차이 (우리 강점)
   Why: 멀티언어 블로그의 차별화 포인트, 니치 키워드...

...

[Korean]
------------------------------------------------------------

6. 🔥 AI 코딩 도구가 팀 생산성을 떨어뜨린 순간
   Category: tech | Competition: 🟡 medium
   Intent: 과도한 자동화의 부작용 이해
   Angle: 트렌드의 한계/실패 케이스
   Why: 대형 미디어가 안 건드리는 영역, 결정 단계 검색...

...

============================================================

어떤 키워드를 큐에 추가할까요?
숫자를 쉼표로 구분해서 입력하세요 (예: 1,3,5,7,10)
또는 'all'을 입력하면 전부 추가됩니다.
'q'를 입력하면 취소합니다.

선택: 1,2,6,8,12
```

## 선택 가이드 (5분 필터링)

### ✅ 좋은 키워드

- "내가 읽고 싶은가?" → YES
- "자동화 냄새" 나는가? → NO
- 경쟁 수준: 🟢 low / 🟡 medium
- Decision-stage intent 명확

### ❌ 제거할 키워드

- 단순 트렌드 요약 ("2025 트렌드")
- 뉴스성 키워드
- 대형 미디어 점령 영역 (🔴 high competition)
- "혁신적", "게임체인저" 같은 AI 냄새

## 추천 주간 비율

```
Trend (🔥) : Evergreen (🌲) = 3 : 7
```

**예시 선택**:
- Trend 3개: 지금 뜨는 기술/이슈의 한계/실패 케이스
- Evergreen 2개: 지속적으로 검색되는 의사결정 키워드

## Topic Queue 구조

### Trend 키워드

```json
{
  "id": "019-ko-tech-ai-coding-inefficiency",
  "keyword": "AI coding assistant 언제 비효율적인가",
  "language": "ko",
  "category": "tech",
  "priority": 7,
  "status": "pending",
  "keyword_type": "trend",
  "expiry_days": 21,
  "search_intent": "AI 도구 도입 전 판단 기준 찾기",
  "angle": "과도한 자동화의 한계",
  "competition_level": "low",
  "created_at": "2026-01-17T..."
}
```

**특징**:
- `expiry_days`: 21일 (3주) 유통기한
- 타이밍 중요
- 짧고 날카로운 글

### Evergreen 키워드

```json
{
  "id": "020-en-business-remote-tool-selection",
  "keyword": "Remote work tool selection mistakes",
  "language": "en",
  "category": "business",
  "priority": 6,
  "status": "pending",
  "keyword_type": "evergreen",
  "search_intent": "리모트 툴 선택 시 실수 방지",
  "angle": "의사결정 실수 사례 분석",
  "competition_level": "low",
  "created_at": "2026-01-17T..."
}
```

**특징**:
- 유통기한 없음
- 업데이트 가능
- SEO 누적형

## 자주 묻는 질문

### Q1. 왜 자동 추가하지 않고 수동 선택하나요?

**A**: "자동화 냄새"는 AI가 자기 자신을 판단하기 어렵습니다. 인간의 5분 필터링이 품질 유지의 핵심입니다.

### Q2. 주 1회 말고 더 자주 실행해도 되나요?

**A**: 가능하지만 비추천. Claude API 비용과 선택 피로도 증가. 주 1회가 최적입니다.

### Q3. 15개가 너무 많으면?

**A**: `--count` 옵션으로 조절 가능:
```bash
python scripts/keyword_curator.py --count 10
```

### Q4. 선택 후 바로 글 생성되나요?

**A**: 아니요. topic queue에 추가만 됩니다. Daily workflow가 자동으로 글 생성합니다.

### Q5. Trend vs Evergreen 비율을 어떻게 맞추나요?

**A**: 선택할 때 🔥(Trend)와 🌲(Evergreen) 이모지를 보고 비율 조절하세요.

## 주간 루틴 예시

**일요일 저녁 (5분)**

```bash
# 1. 키워드 생성
python scripts/keyword_curator.py

# 2. 후보 검토 (2분)
# - "내가 읽을 만한가?" 기준
# - 자동화 냄새 체크

# 3. 선택 입력 (1분)
# 선택: 1,3,5,7,10,12,14

# 4. 통계 확인 (1분)
python scripts/topic_queue.py stats

# Done! 다음 주까지 자동 생성됨
```

## 관련 문서

- [KEYWORD_STRATEGY.md](KEYWORD_STRATEGY.md): 키워드 전략 전체 설명
- [README.md](../README.md#scripts-usage): 전체 시스템 사용법
- [PROJECT_CONTEXT.md](../PROJECT_CONTEXT.md): 시스템 아키텍처

---

**Last updated**: 2026-01-17
**Version**: 1.0
