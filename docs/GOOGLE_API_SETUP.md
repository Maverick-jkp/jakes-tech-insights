# Google Custom Search API Setup Guide

Google Custom Search API를 사용하여 실시간 트렌드 데이터를 가져오는 방법입니다.

## 1. Google API Key 발급

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 프로젝트 생성 또는 선택
3. 왼쪽 메뉴에서 **APIs & Services** → **Credentials** 클릭
4. 상단의 **Create credentials** → **API key** 클릭
5. 생성된 키 복사 → 이것이 `GOOGLE_API_KEY`

### API 활성화

6. 왼쪽 메뉴에서 **APIs & Services** → **Library** 클릭
7. "Custom Search API" 검색
8. **Custom Search API** 클릭 → **Enable** 버튼 클릭

## 2. Custom Search Engine 생성

1. [Programmable Search Engine](https://programmablesearchengine.google.com/) 접속
2. **Add** 버튼 클릭
3. 검색엔진 설정:
   - **Name**: Jake's Tech Insights Trends
   - **What to search**: Search the entire web
   - **Search settings**:
     - Turn on "Search the entire web"
     - Turn off "Image search"
4. **Create** 버튼 클릭
5. 생성된 **Search Engine ID** 복사 → 이것이 `GOOGLE_CX`

## 3. 환경 변수 설정

### macOS/Linux (`.zshrc` 또는 `.bashrc`에 추가)

```bash
# Google Custom Search API
export GOOGLE_API_KEY="your-google-api-key-here"
export GOOGLE_CX="your-search-engine-id-here"
```

설정 후:
```bash
source ~/.zshrc
```

### 확인

```bash
echo $GOOGLE_API_KEY
echo $GOOGLE_CX
```

## 4. 테스트

```bash
cd /Users/jakepark/projects/jakes-tech-insights
python3 scripts/keyword_curator.py --count 15
```

성공 시:
```
============================================================
  🔍 Fetching trending topics from Google...
============================================================

  ✓ Fetched 5 results for: AI trends 2026
  ✓ Fetched 5 results for: tech news today
  ...
```

## 5. 비용 안내

- **Custom Search API**: 하루 100회 무료, 이후 $5/1000 쿼리
- **주간 키워드 수집**: 8개 쿼리 × 4주 = 32회/월 (무료 범위 내)
- **추가 비용 없음** (월 100회 미만)

## 6. 문제 해결

### API Key가 작동하지 않는 경우

1. Google Cloud Console → **APIs & Services** → **Credentials**
2. API Key 클릭 → **API restrictions**
3. "Restrict key" → "Custom Search API" 선택
4. Save

### CX ID를 찾을 수 없는 경우

1. [Programmable Search Engine](https://programmablesearchengine.google.com/)
2. 생성한 검색엔진 클릭
3. **Setup** → **Basic** → **Search engine ID** 복사

### "API not enabled" 오류

1. Google Cloud Console → **APIs & Services** → **Library**
2. "Custom Search API" 검색 → Enable

## 7. 자동화 스크립트

환경 변수가 설정되면 cron job이 자동으로 작동합니다:

```bash
# Weekly keyword curation (Sundays 6 PM KST)
0 18 * * 0 cd /Users/jakepark/projects/jakes-tech-insights && source ~/.zshrc && python3 scripts/keyword_curator.py --count 15
```

---

## 8. 검색 쿼리 전략 (Query Strategy)

### 핵심 원칙: 상태 머신 (State Machine)

트렌드는 **명사**가 아니라 **전환(transition)**이다.

```
기대 → 좌절
행동 → 거부
약속 → 침묵
```

### 5가지 트렌드 레이어

| 레이어 | 키워드 패턴 | 예시 |
|--------|------------|------|
| **상태 전환** | after X, suddenly, overnight | "after update", "갑자기", "突然" |
| **기대 붕괴** | promised but, supposed to | "promised but denied", "발표와 다름" |
| **비교 분노** | others got, only me | "others got compensated", "나만 안됨" |
| **시간 손실** | deadline passed, too late | "deadline passed", "마감 놓침" |
| **침묵** | no response, ignored | "no response", "説明なし" |

### 좋은 쿼리 vs 나쁜 쿼리

#### ❌ 나쁜 예시 (단순 명사)
- "celebrity scandal today"
- "app account banned"
- "government policy"

#### ✅ 좋은 예시 (상태 전환)
- "celebrity apology issued but backlash continues"
- "account banned after update no response"
- "government support supposed to but denied"

### 현재 적용된 쿼리 (20개)

```python
# Tech - State Transition + Silence
"account banned after update no response"
"service outage promised compensation denied"
"앱 업데이트 후 갑자기 먹통"
"アカウント停止 理由説明なし"

# Business - Deadline Loss + Others Got
"class action deadline passed too late"
"refund promised but denied suddenly"
"집단소송 신청 마감 놓침"
"返金約束したが 拒否された"

# Society - Expectation Collapse
"government support supposed to but denied"
"new policy suddenly stricter than announced"
"정부지원 조건 발표와 다름"
"政府支援 突然 条件厳しく"

# Entertainment - Action → Rejection
"celebrity apology issued but backlash continues"
"idol agency promised explanation ignored fans"
"사과문 냈지만 논란 계속"
"謝罪文出したが 炎上続く"

# Lifestyle - Safety Promise Broken
"product recall announced but no refund"
"food contamination others got compensated only me"
"리콜 발표했는데 환불 거부"
"リコール発表 返金対応なし"
```

### 왜 이 전략이 효과적인가?

1. **감정 강도 UP**: 단순 사건 < 기대 배신 = 더 강한 분노
2. **검색 의도 명확**: "왜 이런 일이?" → "왜 나만 이렇게 당했어?"
3. **긴급성 증폭**: 시간 손실 프레임 = 즉각 행동 유도
4. **CPC 최적화**: 감정 기반 검색 = 더 높은 광고 단가

---

## 9. 안전 가이드라인 (Safety & Risk Management)

### 핵심 원칙

**자동화·수익형 파이프라인에서는 실명 미사용이 기본값**

### 🔴 절대 금지

1. **실명 사용**
   - 연예인, 기업인, 정치인 실명
   - 특정 기업명, 브랜드명
   - 구체적 부처명, 기관명

2. **명예훼손 리스크**
   - 확정되지 않은 의혹·논란 프레이밍
   - "은폐", "숨긴", "거짓말" 등 강한 비난

3. **AdSense 정책 위반**
   - 가십성 실명 언급
   - 부정적 프레이밍 + 실명 조합

### ✅ 안전한 대체 표현

| 위험 | 안전 대체 |
|------|-----------|
| 아이린 | top girl group member |
| ○○배우 | A-list actor |
| ○○기획사 | major entertainment agency |
| 특정 아이돌 | K-pop idol |
| 국토부 | government ministry |
| 애플 | tech giant / major tech company |
| 네이버 | major portal / tech platform |

### 🟡 조건부 허용 (3조건 모두 충족 시)

1. ✅ 사법/행정적으로 결론 난 사건
2. ✅ 모든 서술이 팩트 나열만
3. ✅ 감정 프레이밍 제거

### 리스크 레벨 시스템

**자동 분류:**
- `safe`: AdSense/플랫폼 안전 (자동 승인)
- `caution`: 사실 확인 필수 (수동 검토)
- `high_risk`: 법적 검토 필요 (자동 차단)

### Intent Signal 중복 방지

**5가지 Signal:**
- `STATE_CHANGE`: 상태 전환
- `PROMISE_BROKEN`: 기대 붕괴
- `SILENCE`: 침묵
- `DEADLINE_LOST`: 시간 손실
- `COMPARISON`: 비교 분노

**규칙:**
- 같은 signal을 가진 키워드는 언어당 최대 2개까지만
- 5개 signal을 언어별로 균등하게 분배
- 의미 중복 키워드 자동 제거

---

**참고**: API 키는 절대 GitHub에 커밋하지 마세요. 환경 변수로만 관리하세요.
