# Search API Setup Guide

이 프로젝트는 **Brave Search API**를 사용하여 실시간 트렌드 데이터와 레퍼런스를 가져옵니다.

## ⚠️ Important: Google Custom Search API Deprecated

**2026년 1월 기준**, Google Custom Search JSON API는 신규 사용자에게 더 이상 제공되지 않습니다.

- ❌ 기존 Google API Key: 403 Forbidden 에러 발생
- ❌ 새 프로젝트 생성해도 동일 에러
- ✅ **대안**: Brave Search API (더 저렴하고 쿼터 20배 많음)

---

## 1. Brave Search API 설정 (권장)

### 1.1 API Key 발급

1. [Brave Search API](https://api.search.brave.com/) 접속
2. **Sign Up** 클릭
3. 이메일 인증 완료
4. Dashboard → **API Keys** 섹션
5. **Create New Key** 클릭
6. API Key 복사 → 이것이 `BRAVE_API_KEY`

### 1.2 환경 변수 설정

**macOS/Linux** (`.zshrc` 또는 `.bashrc`에 추가):

```bash
# Brave Search API
export BRAVE_API_KEY="your-brave-api-key-here"
```

설정 후:
```bash
source ~/.zshrc
```

### 1.3 확인

```bash
echo $BRAVE_API_KEY
```

### 1.4 테스트

```bash
cd /Users/jakepark/projects/jakes-tech-insights
python3 scripts/keyword_curator.py --count 2 --auto
```

성공 시:
```
✅ Total 26 trending topics fetched
✅ All 2 keywords have references!
✓ Added: 🔥 Trend | 키워드1
✓ Added: 🔥 Trend | 키워드2
```

### 1.5 비용 안내

- **Free Tier**: 2,000 queries/month (~66 queries/day)
- **Overage Cost**: $0.55/1,000 queries
- **예상 사용량**: ~120 queries/month (6% of free tier)
- **추가 비용 없음** (월 2,000회 미만)

**Google과 비교**:
- Brave: 2,000/month free (66/day)
- Google: 100/day free
- **Brave가 20배 더 많은 무료 쿼터 제공**

---

## 2. Google API Key 발급 (레거시, 더 이상 작동 안 함)

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 프로젝트 생성 또는 선택
3. 왼쪽 메뉴에서 **APIs & Services** → **Credentials** 클릭
4. 상단의 **Create credentials** → **API key** 클릭
5. 생성된 키 복사 → 이것이 `GOOGLE_API_KEY`

### API 활성화

6. 왼쪽 메뉴에서 **APIs & Services** → **Library** 클릭
7. "Custom Search API" 검색
8. **Custom Search API** 클릭 → **Enable** 버튼 클릭

**⚠️ 주의**: Enable 해도 403 Forbidden 에러 발생 (신규 사용자에게 제공 안 됨)

## 3. Custom Search Engine 생성 (더 이상 사용 안 함)

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

## 4. Google 환경 변수 설정 (레거시)

### macOS/Linux (`.zshrc` 또는 `.bashrc`에 추가)

```bash
# Google Custom Search API (DEPRECATED - 더 이상 작동 안 함)
export GOOGLE_API_KEY="your-google-api-key-here"
export GOOGLE_CX="your-search-engine-id-here"
```

**⚠️ 주의**: 환경 변수 설정해도 403 Forbidden 에러 발생

---

## 5. 비용 비교

### Brave Search API (현재 사용 중) ✅
- **Free Tier**: 2,000 queries/month
- **Overage Cost**: $0.55/1,000 queries
- **예상 사용량**: ~120 queries/month
- **월 비용**: $0 (무료 범위 내)

### Google Custom Search API (더 이상 사용 불가) ❌
- **Free Tier**: 100 queries/day (3,000/month)
- **Overage Cost**: $5/1,000 queries (Brave의 9배 비쌈)
- **Status**: 신규 사용자에게 제공 안 됨 (403 Forbidden)

## 6. 문제 해결

### Brave API: "403 Forbidden" 에러

**원인**: API Key가 잘못되었거나 만료됨

**해결**:
1. [Brave Search Dashboard](https://api.search.brave.com/app/dashboard) 접속
2. API Keys 섹션에서 키 상태 확인
3. 필요시 새 키 생성

### Brave API: "429 Too Many Requests" 에러

**원인**: 월 2,000 쿼리 한도 초과

**해결**:
1. Dashboard에서 현재 사용량 확인
2. 쿼리 수 줄이기 (--count 값 감소)
3. 또는 유료 플랜 업그레이드 고려

### Brave API Key 환경 변수 미설정

**증상**:
```
⚠️  Brave Search API key not found
   Set BRAVE_API_KEY environment variable
```

**해결**:
```bash
export BRAVE_API_KEY="your-api-key"
source ~/.zshrc
echo $BRAVE_API_KEY  # 확인
```

### Google API 관련 에러 (레거시)

**Google "403 Forbidden" 에러**:
- **원인**: Google Custom Search JSON API 신규 사용자 제공 중단
- **해결**: Brave Search API로 전환 (위 섹션 1 참조)

**Google "API not enabled" 에러**:
- Enable 해도 403 에러 계속 발생 → Brave로 전환 필요

## 7. 자동화 스크립트

`BRAVE_API_KEY` 환경 변수가 설정되면 cron job이 자동으로 작동합니다:

```bash
# Weekly keyword curation (Sundays 6 PM KST)
0 18 * * 0 cd /Users/jakepark/projects/jakes-tech-insights && source ~/.zshrc && python3 scripts/keyword_curator.py --count 15
```

**주의**: `.zshrc`에 `BRAVE_API_KEY` 추가 필수

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

## 10. Migration History

### 2026-01-22: Google → Brave API 전환

**이유**:
- Google Custom Search JSON API 신규 사용자 제공 중단
- 모든 Google API 요청이 403 Forbidden 반환
- Error message: "This project does not have the access to Custom Search JSON API"

**해결**:
- Brave Search API로 완전 전환
- 테스트 결과: 2/2 키워드에 레퍼런스 정상 추출
- 87% 성공률 (26/30 쿼리)
- 비용 절감: $5/1K → $0.55/1K (11배 저렴)
- 쿼터 증가: 100/day → 2,000/month (20배 많음)

**변경 사항**:
- `scripts/keyword_curator.py`: Google API → Brave API
- `.env`: `BRAVE_API_KEY` 추가
- 환경 변수: `GOOGLE_API_KEY`, `GOOGLE_CX` 더 이상 불필요 (하지만 호환성 유지)

**상세 리포트**: [.claude/reports/active/brave-api-migration-success-2026-01-22.md](../.claude/reports/active/brave-api-migration-success-2026-01-22.md)

---

## 11. API 비교표

| Feature | Google Custom Search | Brave Search |
|---------|---------------------|--------------|
| **Free Tier** | ❌ 100/day (더 이상 신규 제공 안 됨) | ✅ 2,000/month |
| **Cost (per 1K)** | $5.00 | $0.55 (11x cheaper) |
| **Availability** | ❌ 403 Forbidden | ✅ Working |
| **Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Speed** | Fast | Fast |
| **Privacy** | Tracking | No tracking |
| **Setup** | Complex (PSE + API) | Simple (API only) |

**추천**: ✅ Brave Search API (현재 사용 중)

---

**참고**: API 키는 절대 GitHub에 커밋하지 마세요. 환경 변수로만 관리하세요.
