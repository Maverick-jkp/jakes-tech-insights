# Claude 작업 가이드라인

> Claude가 이 프로젝트에서 작업할 때 반드시 지켜야 할 철칙

---

## 🚨 절대 규칙 (CRITICAL)

### 1. 속도보다 정확성
- **절대 추측하지 않기**
- **파일을 직접 읽고 확인하기**
- 빠르게 답하려다 틀리는 것보다, 느려도 정확한 것이 훨씬 낫다

**나쁜 예:**
```
사용자: "이 파일이 뭐하는 거야?"
Claude: "아마 ~할 것 같습니다" (추측)
```

**좋은 예:**
```
사용자: "이 파일이 뭐하는 거야?"
Claude: [파일을 읽고] "이 파일은 정확히 ~를 합니다"
```

### 2. 확인 후 답변
- 코드를 읽고 → 이해하고 → 검증한 후 → 답변
- "~일 것 같습니다", "아마도" 금지
- 불확실하면 "확인하겠습니다"라고 말하고 파일 읽기

### 3. API/쿼리 계산 시
- 반드시 코드에서 API 호출 위치 확인
- 추측으로 계산하지 말 것
- 각 단계별로 명확히 검증

**예시:**
```
❌ 틀린 방식:
"키워드 생성이랑 콘텐츠 생성 둘 다 API 쓸 거예요" (추측)

✅ 올바른 방식:
1. keyword_curator.py 읽기 → Google API 사용 확인
2. generate_posts.py 읽기 → Claude API만 사용 확인
3. "키워드 생성만 Google API 사용합니다 (30 쿼리)"
```

### 4. 시간대 변환
- cron 표현식을 읽을 때 UTC → KST 변환 필수
- 주석만 보지 말고 실제 값도 확인
- `'0 9 * * *'` = 9:00 UTC = 18:00 KST

### 5. 불확실할 때는 즉시 확인
- 추측으로 답변하지 말 것
- "확인하겠습니다"라고 말하고 파일 읽기
- 확인 후 정확히 답변

**나쁜 예:**
```
사용자: "이게 API 쓰는 거야?"
Claude: "네, 아마 사용할 것 같습니다" (추측 → 틀림 → 사용자 정정)
```

**좋은 예:**
```
사용자: "이게 API 쓰는 거야?"
Claude: "확인하겠습니다"
        [파일 읽고 검증]
        "아니요, API를 사용하지 않습니다 (Line 42)"
```

---

## 📋 작업 전 체크리스트

작업하기 전에 반드시:

- [ ] 관련 파일을 읽었는가?
- [ ] 추측하지 않고 확인했는가?
- [ ] 계산이 정확한가?
- [ ] 시간대 변환이 맞는가?
- [ ] 코드 로직을 제대로 이해했는가?

---

## 💬 사용자 교정

### 개발 용어 설명
- 사용자가 개발 개념을 오해하면 친절히 설명
- 복잡한 개념은 숫자와 예시로 설명
- 전문 용어 최소화

**예시:**
```
사용자: "RSS도 API 쓰는 거야?"
Claude: "아니요, RSS는 무료 공개 URL입니다.
        Google Custom Search만 API 쿼리를 소비합니다.

        - RSS 가져오기 = 0 쿼리 (무료)
        - Google 검색 = 1 쿼리 (유료)"
```

---

## 🔍 검증 방법

### 파일 읽기
```python
# 항상 Read 도구 사용
Read(file_path="정확한/경로/파일.py")
```

### 코드 로직 확인
```python
# API 호출 위치 찾기
1. 파일 읽기
2. requests.get() 또는 API 호출 찾기
3. 몇 번 호출되는지 계산
4. 답변
```

### 시간 계산
```yaml
cron: '0 9 * * *'
→ 9:00 UTC
→ UTC + 9 = 18:00 KST (저녁 6시)
```

---

## ⚠️ 과거 실수 사례

### 실수 1: API 사용량 오계산
- **잘못**: "콘텐츠 생성도 Google API 쓸 것 같아요" (추측)
- **올바름**: generate_posts.py 읽고 Claude API만 사용 확인

### 실수 2: 시간대 혼동
- **잘못**: cron '0 9'를 보고 "오전 9시"라고 답변
- **올바름**: 9:00 UTC = 18:00 KST 변환 후 답변

### 실수 3: 환각 (Hallucination)
- **잘못**: 파일 안 읽고 "~일 것입니다" 답변
- **올바름**: 파일 읽고 정확히 확인 후 답변

### 실수 4: 추측으로 빠른 답변
- **잘못**: 빠르게 답변 → 틀림 → 사용자 정정 → 다시 확인 (시간 낭비)
- **올바름**: "확인하겠습니다" → 파일 읽기 → 정확한 답변 (한 번에 해결)

---

## ✅ 좋은 답변 패턴

### 패턴 1: 확인 후 답변
```
사용자: "이거 몇 개 만들어?"
Claude: [파일 읽기]
        "정확히 30개 키워드를 생성합니다 (Line 405)"
```

### 패턴 2: 계산 검증
```
사용자: "API 몇 번 써?"
Claude: [코드 확인]
        "1. RSS 가져오기: 0 쿼리
         2. 30개 키워드 검색: 30 쿼리
         3. 콘텐츠 생성: 0 쿼리
         총: 30 쿼리/일"
```

### 패턴 3: 불확실할 때
```
사용자: "이게 맞아?"
Claude: "확인하겠습니다"
        [파일 읽고 검증]
        "네, 맞습니다. 정확히 ~입니다"
```

---

## 🎯 핵심 원칙

1. **속도 < 정확성**
   - 빠르게 틀리는 것보다 느려도 정확한 게 낫다

2. **추측 금지**
   - "~일 것 같습니다" 절대 금지
   - 반드시 파일 읽고 확인

3. **검증 필수**
   - API 사용량, 시간대, 계산 등 모두 검증

4. **단순 명료**
   - 복잡한 설명보다 숫자와 예시 사용

5. **질문 먼저, 답변은 나중에**
   - 불확실하면 즉시 "확인하겠습니다"
   - 파일 읽고 검증 후 정확히 답변
   - 추측으로 빠르게 답변하지 말 것

6. **작업 내역 문서화**
   - 사용자가 "여태까지 한거 저장" 요청 시
   - **반드시 WORK_LOG.md에도 기록**
   - AUTOMATION_CONTEXT.md만 업데이트하고 끝내지 말 것

7. **배포 환경 이해**
   - **Cloudflare Pages 프로젝트 = 로컬 Hugo 서버 불필요**
   - Git Push → Cloudflare 자동 Hugo 빌드 → 자동 배포
   - `hugo server` 실행 시도 절대 금지 (이전에도 같은 실수)
   - 파일 수정 → 커밋 → 푸시 → Cloudflare 확인

---

## 📝 문서화 규칙

### 작업 완료 시 문서 업데이트

사용자가 "여태까지 한거 저장", "작업 내역 기록", "문서화" 등을 요청하면:

1. **AUTOMATION_CONTEXT.md** 업데이트 (공개 문서)
   - Recent Changes Log에 추가
   - 기술적 세부사항 기록

2. **WORK_LOG.md** 업데이트 (개인 노트, Git 제외)
   - 해당 날짜 섹션에 작업 내역 추가
   - 발견한 문제점 기록
   - 다음 할 일 체크리스트 작성
   - 교훈 기록

**둘 다 업데이트해야 합니다. 하나만 하고 끝내지 마세요.**

---

## 🚫 절대 금지 사항

### Hugo 로컬 서버 실행 시도

이 프로젝트는 **Cloudflare Pages**에 배포되어 있습니다.

**절대 하지 말 것:**
- `hugo server -D` 실행 시도
- `hugo` 명령어 실행 시도
- "로컬에서 확인해야 한다" 발언
- Hugo 설치 여부 확인

**올바른 워크플로우:**
1. 파일 수정 (layouts, content, scripts 등)
2. Git 커밋 및 푸시
3. Cloudflare Pages가 자동으로 Hugo 빌드
4. 사용자가 배포된 사이트에서 확인

**이전 실수:**
- 사용자: "전에도 한 번 로컬서버 시도했었는데 니가 필요없다고 했었어"
- Claude가 같은 실수를 반복함
- 이번에 다시 `hugo server` 실행 시도 → Hugo 미설치 에러

**기억할 것:**
- Cloudflare Pages = Serverless 빌드 플랫폼
- Git Push = 자동 배포 트리거
- 로컬 Hugo 서버 = 완전히 불필요

---

## 🖼️ Unsplash 이미지 관리

### 중복 방지 시스템

**핵심 원칙:**
- **절대 같은 이미지를 재사용하지 않음**
- `data/used_images.json`에 사용된 이미지 ID 추적
- Unsplash API 결과에서 미사용 이미지만 선택

**로직 위치**: [scripts/generate_posts.py:887-915](scripts/generate_posts.py:887-915)

```python
# 1. used_images.json 로드
used_images = set(json.load("data/used_images.json"))

# 2. Unsplash API 결과에서 미사용 이미지 찾기
for result in data['results']:
    if result['id'] not in used_images:
        photo = result
        used_images.add(result['id'])
        break

# 3. 모두 사용됐으면 랜덤 선택
if photo is None:
    photo = random.choice(data['results'])
    used_images.add(photo['id'])
```

### Placeholder 이미지 문제

**문제 상황:**
- Unsplash fetch 실패 시 → `image: "/images/placeholder-{category}.jpg"` 사용
- **그러나 placeholder 파일은 실제로 존재하지 않음** → 썸네일 깨짐

**Fallback 로직**: [scripts/generate_posts.py:1003-1005](scripts/generate_posts.py:1003-1005)
```python
if not image_path:
    # Use category-based placeholder
    image_path = f"/images/placeholder-{category}.jpg"
```

**해결 방법:**
1. **자동 수정 워크플로우** (추천):
   ```bash
   /opt/homebrew/bin/gh workflow run fix-placeholder-images.yml
   ```
   - 모든 placeholder 게시물 자동 검색
   - 각 게시물의 title/category에 맞는 이미지 가져오기
   - 자동 커밋 & 푸시

2. **수동 삭제 & 재생성**:
   ```bash
   git rm "content/xxx/problem-post.md"
   git commit -m "Remove placeholder post for regeneration"
   git push
   ```

**왜 Placeholder가 발생하나?**

1. **번역 실패** (가장 흔한 원인)
   - 일본어/한국어가 제대로 영어로 번역되지 않음
   - 예: `"sports sumo wrestlingtournament results をhighlightsた方必見！"` (잘못됨)
   - Unsplash API 410 Gone 에러 발생
   - **해결**: [scripts/replace_placeholder_images.py:59-70](scripts/replace_placeholder_images.py:59-70)에서 non-ASCII 문자 제거

2. **중복 이미지**
   - Unsplash API가 제한된 결과 반환 (예: 10개)
   - 10개 모두 `used_images.json`에 이미 존재
   - 랜덤 선택 → 다운로드 실패
   - Fallback → placeholder 경로

3. **API 실패**
   - 네트워크 오류
   - Unsplash API 장애

**실제 발생 사례 (2026-01-20):**
- 게시물: `ja/sports/2026-01-20-大相撲結果速報見逃し.md`
- 문제: 번역 로직이 일부 일본어를 남김
- 검색어: `"sports sumo wrestlingtournament results をhighlightsた方必見！"`
- 결과: 410 Gone 에러 → placeholder 사용
- 수정: non-ASCII 문자 제거 로직 추가
- 재실행 후 성공: `"sports sumo wrestling tournament results highlights"`

**예방책:**
- non-ASCII 문자 완전 제거
- 번역 사전 확장
- `per_page` 값 증가 (10 이상)
- Fallback: 카테고리만으로 검색

### API 키 설정 확인

**환경 변수:**
- `UNSPLASH_ACCESS_KEY`: GitHub Secrets에 설정됨
- GitHub Actions 워크플로우에서 자동 주입
- 로컬 실행 시에는 별도 설정 필요 (선택사항)

**확인 방법:**
```bash
# GitHub Actions 로그에서 확인
🖼️ Unsplash API enabled  # ← 정상
⚠️ Unsplash API key not found  # ← 문제
```

### 이미지 파일 배포 흐름

**올바른 흐름:**
```
1. generate_posts.py 실행
   → Unsplash에서 이미지 다운로드
   → static/images/에 저장

2. Git 커밋 & 푸시
   → static/images/*.jpg 포함

3. Cloudflare Pages 자동 빌드
   → Hugo가 static/ 폴더 복사

4. 배포 완료
   → https://jakes-tech-insights.pages.dev/images/*.jpg 접근 가능
```

**잘못된 이해 (착각하지 말 것):**
- ❌ "로컬에는 있는데 Cloudflare에 없네요"
  - → 파일이 git에 있으면 Cloudflare에도 있음
  - → 실제 문제: placeholder **경로**는 있지만 **파일**이 없음

- ❌ "API 키가 없어서 이미지를 못 가져왔나봐요"
  - → 먼저 워크플로우 로그 확인
  - → "🖼️ Unsplash API enabled" 메시지 확인

**디버깅 순서:**
1. 게시물 frontmatter 확인: `image: "/images/xxx.jpg"`
2. 파일 존재 확인: `git ls-files static/images/xxx.jpg`
3. 원격 배포 확인: `curl -I https://jakes-tech-insights.pages.dev/images/xxx.jpg`
4. Placeholder 여부: `grep -r "placeholder" content/`

---

## 🔄 토큰 효율성

### 중복 로직 방지

**문제:**
- 같은 로직을 반복 설명 → 토큰 낭비
- 가이드라인에 이미 기록된 내용을 재설명

**해결:**
1. **먼저 가이드라인 확인**
   - `docs/CLAUDE_GUIDELINES.md`
   - `docs/AUTOMATION_CONTEXT.md`
   - `docs/WORK_LOG.md`

2. **가이드라인에 있으면 참조만**
   ```
   ✅ "중복 이미지 방지는 CLAUDE_GUIDELINES.md의 '🖼️ Unsplash 이미지 관리' 섹션을 참고하세요"

   ❌ [중복 로직 전체를 다시 설명하는 긴 답변]
   ```

3. **새로운 발견은 즉시 기록**
   - 가이드라인에 없는 내용 발견 시
   - 즉시 해당 섹션에 추가
   - 다음번에는 참조만 하면 됨

**기록해야 할 것들:**
- 반복되는 질문의 답변
- 자주 발생하는 문제의 해결법
- 시스템 동작 원리
- 디버깅 체크리스트

---

**마지막 업데이트**: 2026-01-20 (개정 5회)
**작성 이유**:
1. 속도에 치중해 부정확한 답변을 반복한 문제 해결
2. 배포 환경 이해 부족으로 불필요한 로컬 서버 시도 반복
3. Unsplash 이미지 중복 방지 로직 문서화
4. Placeholder 이미지 문제 해결 방법 추가
5. 토큰 효율성 개선 (중복 설명 방지)

**이 가이드라인을 위반하면 사용자의 시간과 노력을 낭비하게 됩니다.**
