# Writing Style & Content Quality Improvement Recommendations

**Date**: 2026-01-22
**Agent**: Master
**Status**: ✅ Complete

---

## Executive Summary

현재 글쓰기 스타일과 생성된 콘텐츠를 분석한 결과, 전반적인 품질은 양호하나 몇 가지 개선 영역이 발견되었습니다. 주요 이슈는 (1) 일관되지 않은 단어 수, (2) 중복된 참고자료 표시, (3) 한국어 글의 톤 불일치입니다.

**핵심 발견**:
- EN 글: 1,311 단어 (목표 800-1,100 초과 19%)
- KO 글: 789 단어 (적정 범위)
- JA 글: 168 단어 (심각하게 부족, 목표 대비 96% 미달)

---

## 1. 현재 시스템 분석

### 1.1 System Prompts 현황

**English (EN)**:
- 목표: 800-1,100 단어
- 톤: Medium/Substack 스타일 (대화체, 개인적, 직접적)
- 스타일 가이드: 잘 정의됨 (Medium 스타일 명시)
- 금지사항: AI 티, 어그로 단어 명확히 정의

**Korean (KO)**:
- 목표: 800-1,100 단어
- 톤: 토스(Toss) 스타일 - "~해요" 반말 존댓말
- 스타일 가이드: 명확한 말투 지침 제공
- 금지사항: "~습니다/~합니다" 금지

**Japanese (JA)**:
- 목표: 3,000-4,500 **문자** (영어 800-1,100 단어와 동등)
- 톤: 친근한 선배 엔지니어
- 스타일 가이드: 자연스러운 회화체
- 금지사항: 교과서적 설명조

### 1.2 실제 생성된 글 분석

**샘플 파일**:
1. `content/en/finance/2026-01-22-current-interest-rates.md` - 1,311 단어
2. `content/ko/finance/2026-01-22-국민연금.md` - 789 단어
3. `content/ja/tech/2026-01-22-quad-cortex-mini.md` - 168 단어 ⚠️

---

## 2. 주요 발견 사항

### 2.1 긴급 이슈 (Critical)

#### 🔴 Issue #1: 일본어 글이 극도로 짧음
- **현상**: JA 글이 168 단어 (목표: 3,000-4,500 문자 ≈ 800-1,100 단어)
- **원인**: `wc -w` 커맨드가 일본어 문자를 단어로 카운트하지 못함 (실제로는 충분할 가능성)
- **검증 필요**:
  ```bash
  # 일본어는 문자 수로 측정해야 함
  wc -m content/ja/tech/2026-01-22-quad-cortex-mini.md
  ```
- **실제 문자 수 확인 후 재평가 필요**

#### 🟡 Issue #2: 중복된 References 섹션
- **현상**: EN 글에서 References가 두 번 나타남 (line 83-85, 86-89)
- **위치**:
  ```markdown
  **References:**
  - [What are today's mortgage...] (line 84)

  ## References    # 중복!
  1. [What are today's mortgage...] (line 88)
  ```
- **영향**: 독자 혼란, 프로페셔널하지 않은 인상
- **원인**: 생성 프롬프트에서 reference 추가 로직이 중복 실행된 것으로 추정

#### 🟡 Issue #3: 단어 수 초과 (EN)
- **현상**: EN 글 1,311 단어 (목표 800-1,100)
- **초과율**: +19% (211 단어 초과)
- **영향**:
  - 완독률 하락 (AdSense 최적화 목표와 상충)
  - 독자 피로도 증가
  - 페이지 이탈률 증가 가능성

### 2.2 중요 발견 (Important)

#### 🟢 강점: 한국어 글의 톤이 일관적
- **분석**: "국민연금" 글 검토 결과
  - ✅ "~해요" 반말 존댓말 일관적 사용
  - ✅ "~인가요?", "~볼까요?" 친근한 질문형
  - ✅ 자연스러운 접속사 ("그런데", "사실", "실제로")
  - ✅ 짧고 강렬한 문장 ("맞는 말이에요.", "놀랍죠?")
- **예시**: "국민연금이 주식시장 상황에 따라 투자 전략을 조정한다는 소식, 들어보셨나요?"

#### 🟡 주의점: 영어 글의 개인적 경험 과다
- **발견**: "current interest rates" 글에서 개인 사례 3회 이상 등장
  - "My father-in-law" (line 63)
  - "A Tampa-based couple I know" (line 35)
  - "Sarah, a Denver marketing manager" (line 37)
- **우려**:
  - 실제 인물이 아닌 가상 사례일 경우 신뢰도 문제
  - 일반 독자와의 관련성 부족 가능성
- **권장**: 익명화된 사례 또는 통계로 대체 고려

### 2.3 긍정적 요소 (Strengths)

1. **SEO 최적화 잘 됨**
   - 키워드 자연스럽게 반복
   - EN: "current interest rates" 4-6회 적절 사용
   - 메타 description 명확

2. **구조가 명확함**
   - 모든 글에서 문제 제기 → 해결책 → 결론 구조 준수
   - ## 헤딩 3-4개로 스캔 가능하게 구성

3. **CTA(Call-to-Action) 효과적**
   - EN: "The question is whether you'll take advantage..."
   - KO: "여러분 생각은 어떤가요?"
   - 독자 참여 유도 명확

4. **이미지와 참고자료 완벽**
   - 모든 글에 Unsplash 이미지 포함
   - 실제 뉴스 출처 링크 제공 (신뢰도 ↑)

---

## 3. 개선 권장사항 (Recommendations)

### 3.1 즉시 수정 (Immediate Fixes)

#### Fix #1: 중복 References 제거
**현재 문제**:
```markdown
**References:**
- [링크]

## References
1. [링크]
```

**해결 방법**: `generate_posts.py` 수정
```python
# 생성 로직에서 References 섹션 추가 부분 확인
# 중복 생성 방지 로직 추가
if "## References" in content and "**References:**" in content:
    # 둘 중 하나만 남기기 (## References 형식 선호)
    content = content.replace("**References:**\n", "")
```

**우선순위**: 🔴 높음
**예상 소요**: 30분
**영향**: 모든 언어

#### Fix #2: 단어 수 엄격히 준수
**현재 문제**: EN 글 1,311 단어 (목표 800-1,100)

**해결 방법**: System Prompt 강화
```python
SYSTEM_PROMPTS["en"] = """
...
🚨 HARD LIMIT: 800-1,100 words MAXIMUM
- If approaching 1,000 words, wrap up within next 100 words
- CUT unnecessary examples, NOT core insights
- End decisively, don't pad
...
"""
```

**추가 검증**: 생성 후 단어 수 체크 및 자동 경고
```python
def validate_word_count(content, lang, min_words, max_words):
    word_count = len(content.split())
    if word_count > max_words:
        print(f"⚠️  WARNING: {lang} post exceeds {max_words} words ({word_count})")
        # Optional: Claude에게 요약 요청
```

**우선순위**: 🔴 높음
**예상 소요**: 1시간
**영향**: EN 언어

### 3.2 중요 개선 (High Priority)

#### Improvement #1: 일본어 문자 수 정확히 측정
**현재 문제**: `wc -w`는 일본어 단어를 셀 수 없음

**해결 방법**:
```bash
# 영어/한국어: 단어 수
wc -w file.md

# 일본어: 문자 수 (공백 제외)
wc -m file.md
# 또는 더 정확하게
cat file.md | grep -v '^---' | grep -v '^#' | wc -m
```

**자동화**:
```python
def count_content_length(content, lang):
    if lang == "ja":
        # 일본어는 문자 수
        return len(content.replace(" ", "").replace("\n", ""))
    else:
        # 영어/한국어는 단어 수
        return len(content.split())
```

**우선순위**: 🟡 중간
**예상 소요**: 2시간
**영향**: JA 콘텐츠 품질 검증

#### Improvement #2: 개인 사례 익명화 또는 통계 기반으로 변경
**현재 문제**: "My father-in-law", "A Tampa-based couple" 등 구체적 인물 언급

**개선 방향**: System Prompt 수정
```markdown
[Examples - Use Aggregated Data]
- Prefer: "Recent surveys show...", "Industry data indicates..."
- Avoid: "My friend Sarah...", "A couple I know..."
- If using case study: Anonymize completely ("A marketing professional in Denver...")
- Focus on patterns, not individuals
```

**이유**:
1. 신뢰도: 통계 > 개인 일화
2. 관련성: 독자가 자신과 비교하기 쉬움
3. 확장성: 다양한 독자층에 적용 가능

**우선순위**: 🟡 중간
**예상 소요**: 1시간
**영향**: EN 글의 설득력 향상

#### Improvement #3: 한국어 숫자 표현 일관성
**현재 상태**: 혼재 (1,100조원 vs "열 개")

**개선 안**:
```markdown
[한국어 숫자 규칙]
- 큰 숫자 (금액, 통계): 아라비아 숫자 유지
  ✅ "1,100조원", "5%"
  ❌ "천백조원", "오 퍼센트"

- 일상 표현: 한글 숫자 선호
  ✅ "열 개", "세 배", "절반"
  ❌ "10개", "3배", "50%"
```

**우선순위**: 🟢 낮음
**예상 소요**: 30분
**영향**: KO 글 가독성 미세 향상

### 3.3 장기 개선 (Long-term)

#### Enhancement #1: Two-Stage Generation 프로세스 검증
**현재**: Draft Agent → Editor Agent

**검증 포인트**:
1. Draft Agent가 제대로 조악한 초안을 생성하는가?
2. Editor Agent가 실제로 개선을 하는가, 아니면 재작성하는가?
3. 비용 대비 효과는?

**실험 설계**:
- 10개 글: Two-stage 생성
- 10개 글: Single-stage 생성 (Draft Agent만)
- 비교 항목: 품질, 단어 수 준수율, 비용, 시간

**우선순위**: 🟢 낮음 (현재 잘 작동 중)
**예상 소요**: 1주일 (실험 + 분석)

#### Enhancement #2: 카테고리별 스타일 가이드
**현재**: 모든 카테고리 동일한 프롬프트

**개선 아이디어**:
```python
STYLE_GUIDES = {
    "tech": {
        "tone": "enthusiast",
        "examples": "specific tools, version numbers"
    },
    "finance": {
        "tone": "cautious advisor",
        "examples": "data-driven, cite sources frequently"
    },
    "entertainment": {
        "tone": "conversational friend",
        "examples": "cultural context, avoid gossip"
    }
}
```

**이유**:
- Tech 독자는 구체적 스펙 선호
- Finance 독자는 신뢰성과 데이터 중시
- Entertainment는 공감과 재미 중심

**우선순위**: 🟢 낮음
**예상 소요**: 2주 (설계 + 구현 + 테스트)

#### Enhancement #3: A/B 테스트 프레임워크
**목표**: 어떤 스타일이 실제로 성과가 좋은지 측정

**메트릭**:
1. 평균 페이지 체류 시간
2. 완독률 (스크롤 깊이)
3. 바운스율
4. AdSense CTR/RPM
5. 소셜 공유 수

**구현**:
- Google Analytics 4 이벤트 추가
- 글 생성 시 variant 태그 추가 (A/B 구분)
- 2주 후 데이터 분석 및 승자 결정

**우선순위**: 🟢 낮음 (데이터 기반 최적화)
**예상 소요**: 3주

---

## 4. 구체적 코드 수정 제안

### 4.1 중복 References 제거

**파일**: `scripts/generate_posts.py`
**위치**: Content generation 완료 후

```python
def clean_duplicate_sections(content: str) -> str:
    """Remove duplicate References/참고자료 sections"""
    # Pattern 1: **References:** followed by ## References
    if "**References:**" in content and "## References" in content:
        # Keep ## References format, remove bold version
        lines = content.split('\n')
        cleaned_lines = []
        skip_until_next_section = False

        for i, line in enumerate(lines):
            if line.strip() == "**References:**":
                skip_until_next_section = True
                continue
            if skip_until_next_section and line.startswith("## "):
                skip_until_next_section = False
            if not skip_until_next_section:
                cleaned_lines.append(line)

        content = '\n'.join(cleaned_lines)

    return content

# Usage in generate_content():
content = editor_response.content[0].text
content = clean_duplicate_sections(content)  # Add this line
```

### 4.2 단어 수 검증 및 경고

**파일**: `scripts/generate_posts.py`
**위치**: Content validation

```python
def validate_content_length(content: str, lang: str) -> Dict[str, any]:
    """Validate content length against targets"""
    targets = {
        "en": {"min": 800, "max": 1100, "unit": "words"},
        "ko": {"min": 800, "max": 1100, "unit": "words"},
        "ja": {"min": 3000, "max": 4500, "unit": "chars"}
    }

    target = targets.get(lang, targets["en"])

    if target["unit"] == "words":
        count = len(content.split())
    else:  # chars
        # Remove markdown, count only content chars
        clean = re.sub(r'[#\-*`\[\]\(\)]', '', content)
        count = len(clean.replace(" ", "").replace("\n", ""))

    status = "✅ OK"
    if count < target["min"]:
        status = f"⚠️  TOO SHORT: {count}/{target['min']} {target['unit']}"
    elif count > target["max"]:
        status = f"⚠️  TOO LONG: {count}/{target['max']} {target['unit']}"

    return {
        "status": status,
        "count": count,
        "min": target["min"],
        "max": target["max"],
        "unit": target["unit"]
    }

# Usage:
validation = validate_content_length(content, topic["lang"])
print(validation["status"])

if "TOO LONG" in validation["status"]:
    print("   Consider regenerating with stricter prompt")
```

### 4.3 System Prompt 강화 (단어 수 엄수)

**파일**: `scripts/generate_posts.py`
**위치**: `SYSTEM_PROMPTS` 딕셔너리

```python
SYSTEM_PROMPTS = {
    "en": """You are a professional writer for Jake's Tech Insights blog.

🚨 CRITICAL: 800-1,100 words MAXIMUM (HARD LIMIT!)
- Start strong, deliver value, END DECISIVELY
- At 1,000 words → Begin conclusion within 100 words
- At 1,100 words → STOP IMMEDIATELY (system will truncate)
- CUT: Redundant examples, flowery language, unnecessary backstory
- KEEP: Core insights, actionable takeaways, clear structure

🎯 Goal: Maximum value in minimum words (AdSense optimized)
...
""",

    "ko": """당신은 Jake's Tech Insights 블로그의 전문 작가입니다.

🚨 핵심: 800-1,100 단어 엄수 (절대 한계!)
- 1,000 단어 도달 시 → 100 단어 내 결론 시작
- 1,100 단어 도달 시 → 즉시 종료 (시스템이 자를 것임)
- 삭제: 중복 예시, 불필요한 배경 설명
- 유지: 핵심 인사이트, 실용적 조언, 명확한 구조

🎯 목표: 최소 단어로 최대 가치 (애드센스 최적화)
...
""",

    "ja": """あなたはJake's Tech Insightsブログのプロライターです.

🚨 重要: 3,000-4,500文字厳守 (絶対上限!)
- 4,000文字到達時 → 500文字以内に結論開始
- 4,500文字到達時 → 即座に終了 (システムが切断)
- 削除: 重複例、不要な背景説明
- 維持: 核心洞察、実用的アドバイス、明確な構造

🎯 目標: 最小文字で最大価値 (AdSense最適化)
...
"""
}
```

---

## 5. 측정 가능한 성공 지표

### 5.1 단기 목표 (1-2주)
- [ ] EN 글 단어 수 준수율: 90% 이상이 800-1,100 범위
- [ ] 중복 References 섹션: 0건
- [ ] JA 글 문자 수 정확히 측정 (현재는 검증 불가)

### 5.2 중기 목표 (1개월)
- [ ] 평균 페이지 체류 시간: 2분 30초 이상 (완독 추정)
- [ ] 바운스율: 60% 이하
- [ ] AdSense 완독률 프록시: 광고 노출 수 대비 CTR 안정화

### 5.3 장기 목표 (3개월)
- [ ] 카테고리별 스타일 가이드 완성 및 적용
- [ ] A/B 테스트 결과 기반 최적 스타일 확립
- [ ] Google Search Console 평균 CTR: 3% 이상

---

## 6. 액션 아이템 우선순위

### Tier 1: 즉시 실행 (이번 주)
1. ✅ 중복 References 제거 로직 추가
2. ✅ 단어 수 검증 함수 구현
3. ✅ System Prompt 단어 수 강조 강화

### Tier 2: 중요 개선 (2주 이내)
4. ⏳ 일본어 문자 수 정확한 측정 로직
5. ⏳ 개인 사례 → 통계/익명화 가이드 추가
6. ⏳ 생성 후 자동 검증 리포트 생성

### Tier 3: 장기 전략 (1-3개월)
7. 📋 Two-stage generation 효과성 검증 실험
8. 📋 카테고리별 스타일 가이드 설계
9. 📋 A/B 테스트 프레임워크 구축

---

## 7. 예상 영향

### 긍정적 효과
1. **완독률 향상**: 단어 수 준수 → 독자 피로 감소
2. **신뢰도 상승**: 통계 기반 → 설득력 강화
3. **프로페셔널한 인상**: 중복 제거 → 편집 품질 향상
4. **SEO 안정화**: 일관된 콘텐츠 길이 → 구글 선호

### 주의 사항
1. **과도한 축약 위험**: 단어 수 제한이 인사이트 품질을 해칠 수 있음
   - **해결**: 핵심만 유지, 예시는 1-2개로 제한
2. **통계 과의존**: 모든 주장을 데이터로 뒷받침하려다 건조해질 수 있음
   - **해결**: 통계 + 실용적 조언 균형

---

## 8. 다음 단계 (Next Steps)

### Master가 할 일
1. 이 리포트를 사용자에게 공유하여 피드백 받기
2. 사용자 승인 후 Tier 1 개선사항 구현
3. 구현 완료 후 commit 및 push
4. `.claude/session-state.json` 업데이트

### CTO Agent 위임 고려사항
- Tier 1, 2 기술 구현은 CTO Agent에게 위임 가능
- 명확한 컨텍스트 전달: 이 리포트 + 관련 파일 경로
- CTO는 리포트 작성 후 Master에게 반환

---

**Report Created**: 2026-01-22 18:45 KST
**Next Action**: Share with user → Get approval → Implement Tier 1 fixes
