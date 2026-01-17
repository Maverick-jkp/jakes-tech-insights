# ChatGPT Code Review Setup Guide

자동으로 ChatGPT가 코드를 Engineer와 Designer 관점에서 리뷰하도록 설정하는 가이드입니다.

---

## 🚀 Quick Start

### 1. 필수 패키지 설치

```bash
pip install openai
```

### 2. OpenAI API Key 설정

```bash
export OPENAI_API_KEY='your-openai-api-key-here'
```

영구적으로 설정하려면 `~/.bashrc` 또는 `~/.zshrc`에 추가:

```bash
echo 'export OPENAI_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### 3. 리뷰 실행 (수동)

```bash
# 변경사항을 stage
git add .

# ChatGPT 리뷰 실행
python3 scripts/chatgpt-review.py
```

### 4. 자동 리뷰 설정 (Git Hook)

```bash
# Hook 설치
./scripts/setup-review-hook.sh

# 이제 git commit 할 때마다 자동으로 리뷰 실행됨
git commit -m "your message"

# Hook 스킵하려면
git commit --no-verify -m "your message"
```

---

## 📋 리뷰 내용

### 👨‍💻 Senior Software Engineer Review

**검토 항목:**
- ✅ Code Quality (clean code, best practices)
- ✅ Architecture & Design (scalability, maintainability)
- ✅ Performance (bottlenecks, optimization)
- ✅ Security (vulnerabilities, data exposure)
- ✅ Testing (coverage, edge cases)

### 🎨 Senior Frontend Developer & Designer Review

**검토 항목:**
- ✅ Visual Design (layout, typography, colors)
- ✅ User Experience (flow, interactions, accessibility)
- ✅ Frontend Best Practices (CSS, HTML, performance)
- ✅ Component Design (reusability, consistency)
- ✅ Responsive Design (mobile-first, breakpoints)

---

## 📁 리뷰 파일 저장

리뷰 결과는 `reviews/` 디렉토리에 자동 저장됩니다:

```
reviews/
  CHATGPT_REVIEW_2026-01-17_14-30-00.md
  CHATGPT_REVIEW_2026-01-17_15-45-00.md
```

---

## 🔄 Workflow Integration

### Option A: Manual Review (추천 - 배포 전)

```bash
# 1. 코드 작성 완료
git add .

# 2. ChatGPT 리뷰 실행
python3 scripts/chatgpt-review.py

# 3. 리뷰 확인 및 수정
cat reviews/CHATGPT_REVIEW_*.md

# 4. 수정 후 커밋
git commit -m "Fix issues from ChatGPT review"
```

### Option B: Automatic Review (Git Hook)

```bash
# 1. Hook 설치 (한 번만)
./scripts/setup-review-hook.sh

# 2. 이후 모든 커밋에서 자동 리뷰
git add .
git commit -m "your message"
# → ChatGPT 리뷰 자동 실행
# → 리뷰 확인 후 y/n 선택
```

### Option C: CI/CD Integration

`.github/workflows/review.yml`:

```yaml
name: ChatGPT Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install openai

      - name: Run ChatGPT Review
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python3 scripts/chatgpt-review.py

      - name: Upload Review
        uses: actions/upload-artifact@v3
        with:
          name: chatgpt-review
          path: reviews/
```

---

## ⚙️ 설정 커스터마이즈

### Model 변경

`scripts/chatgpt-review.py`에서:

```python
# GPT-4 (느리지만 정확)
model="gpt-4"

# GPT-3.5 Turbo (빠르고 저렴)
model="gpt-3.5-turbo"

# GPT-4 Turbo (빠르고 정확)
model="gpt-4-turbo-preview"
```

### 리뷰 상세도 조정

```python
# 간단한 리뷰
temperature=0.3
max_tokens=1000

# 상세한 리뷰
temperature=0.5
max_tokens=3000
```

---

## 💰 비용 예상

**GPT-4 기준:**
- Input: $0.03 / 1K tokens
- Output: $0.06 / 1K tokens

**예상 비용 (1회 리뷰):**
- 작은 변경 (< 500 lines): ~$0.10
- 중간 변경 (500-1000 lines): ~$0.30
- 큰 변경 (> 1000 lines): ~$0.50

**GPT-3.5 Turbo (저렴한 대안):**
- Input: $0.0015 / 1K tokens
- Output: $0.002 / 1K tokens
- 약 20배 저렴!

---

## 🔒 보안 고려사항

1. **API Key 보호**
   - .env 파일에 저장 (gitignore)
   - 환경변수로 관리
   - CI/CD secrets 사용

2. **민감한 코드**
   - 민감한 정보가 포함된 커밋은 수동 리뷰
   - `--no-verify` 플래그로 Hook 스킵

3. **데이터 전송**
   - OpenAI는 API 데이터를 학습에 사용하지 않음 (2023년 3월 이후)
   - 프라이빗 코드도 안전

---

## 🐛 트러블슈팅

### "OPENAI_API_KEY not set" 에러

```bash
# API Key 설정 확인
echo $OPENAI_API_KEY

# 설정되지 않았다면
export OPENAI_API_KEY='your-key-here'
```

### "openai package not installed" 에러

```bash
pip install openai
# 또는
pip3 install openai
```

### Hook이 실행되지 않음

```bash
# Hook 파일 권한 확인
ls -la .git/hooks/pre-commit

# 실행 권한 추가
chmod +x .git/hooks/pre-commit
```

### API Rate Limit 에러

```bash
# 잠시 대기 후 재시도
sleep 10
python3 scripts/chatgpt-review.py
```

---

## 📊 리뷰 예시

### Engineer Review 출력:

```markdown
## 👨‍💻 Senior Software Engineer Review

✅ APPROVED with minor suggestions

### Code Quality
- Clean code principles followed
- Proper error handling in place
- Good variable naming

### Architecture
⚠️ layouts/index.html:142
- Consider extracting inline styles to CSS classes
- Improves maintainability

### Performance
✅ No performance concerns
- Images properly optimized
- CSS minification recommended

### Security
✅ No security vulnerabilities detected
- No exposed secrets
- Proper input sanitization
```

### Designer Review 출력:

```markdown
## 🎨 Senior Frontend Developer & Designer Review

✅ APPROVED

### Visual Design
✅ Excellent spacing and layout
- Featured card height reduced appropriately
- Better visual hierarchy

### User Experience
✅ Navigation improvements
- Logo now clickable (industry standard)
- Category links fixed

⚠️ layouts/index.html:242
- Consider custom scrollbar styling for .latest-items-container
- Default scrollbar may look inconsistent

### Responsive Design
✅ Mobile-first approach maintained
- Breakpoints at 768px work well
- Touch targets adequate (50px thumbnails)
```

---

## 🎯 Best Practices

1. **배포 전 필수 리뷰**
   - 모든 production 배포 전 ChatGPT 리뷰 실행
   - 리뷰 결과를 PR에 첨부

2. **리뷰 결과 보관**
   - `reviews/` 디렉토리를 Git에 커밋
   - 히스토리 추적 가능

3. **팀과 공유**
   - 리뷰 결과를 팀 채널에 공유
   - 공통 이슈 패턴 파악

4. **점진적 개선**
   - ChatGPT 피드백을 체크리스트에 반영
   - 반복되는 이슈는 린팅 룰로 자동화

---

## 🔗 관련 문서

- [PRE_DEPLOYMENT_CHECKLIST.md](PRE_DEPLOYMENT_CHECKLIST.md)
- [DEPLOYMENT_REVIEW_2026-01-17.md](DEPLOYMENT_REVIEW_2026-01-17.md)

---

**Created:** 2026-01-17
**Updated:** 2026-01-17
**Author:** Jake Park
**AI Assistant:** Claude Sonnet 4.5
