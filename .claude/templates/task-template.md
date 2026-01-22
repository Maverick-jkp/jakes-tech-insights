# TASK_{ID}: {간단한 제목}

## 목표
{이 작업의 목표를 1-2 문장으로 명확히 설명}

## 담당 에이전트
- **Primary**: {주 담당 에이전트} (예: DESIGNER, DEV_BACKEND, CTO)
- **Support**: {지원 에이전트 - 필요시} (예: DEV_TESTING)

## 브랜치
`{브랜치명}` (예: `feature/dark-mode`, `fix/api-timeout`)

## 의존성
- {다른 작업에 의존하는지 명시}
- 예: "TASK_001 완료 후 시작" 또는 "없음 (독립 작업)"

---

## 요구사항

### 기능 요구사항
1. [ ] {요구사항 1}
2. [ ] {요구사항 2}
3. [ ] {요구사항 3}

### 비기능 요구사항
- **성능**: {성능 목표 - 있다면}
- **보안**: {보안 고려사항 - 있다면}
- **접근성**: {접근성 요구사항 - 있다면}

---

## 기술 스펙

### 파일 수정 목록
```
{수정될 파일 목록}
예:
- scripts/topic_queue.py
- tests/test_topic_queue.py
- docs/QUEUE_DESIGN.md
```

### 기술 세부사항
```
{기술적 구현 방법}
예:
- API: Anthropic Claude 3.5 Sonnet
- 데이터 구조: JSON (topics_queue.json)
- 에러 핸들링: exponential backoff (최대 3회)
```

### 외부 의존성
- {새로운 라이브러리 설치 필요시}
- {API 키 필요시}
- {환경 변수 추가 필요시}

---

## 체크리스트

### 개발
- [ ] 브랜치 생성 (`git checkout -b {브랜치명}`)
- [ ] 코드 작성
- [ ] 로컬 테스트
- [ ] 에러 핸들링 추가
- [ ] 로깅 추가 (필요시)

### 테스트
- [ ] 유닛 테스트 작성 (pytest)
- [ ] 테스트 통과 확인
- [ ] Coverage 확인 (>50%)
- [ ] 통합 테스트 (필요시)

### 품질
- [ ] 코드 리뷰 (자체 검토)
- [ ] Linting (flake8, black - Python)
- [ ] 타입 체크 (type hints - Python)
- [ ] 문서화 (docstrings, 주석)

### 완료
- [ ] 커밋 (`git commit -m "..."`)
- [ ] 푸시 (`git push -u origin {브랜치명}`)
- [ ] Master에게 완료 보고

---

## 예상 작업 시간
{시간 추정 - 참고용}
예: 1-2시간, 30분, 1일

---

## 참고 자료

### 문서
- {관련 문서 링크}
- 예: `.claude/docs/design-system.md`
- 예: `docs/ARCHITECTURE.md`

### 관련 이슈/PR
- {관련 GitHub 이슈}
- {참고할 이전 PR}

### 외부 링크
- {API 문서}
- {라이브러리 문서}

---

## 완료 기준

### Definition of Done
- [ ] 모든 요구사항 구현
- [ ] 모든 테스트 통과
- [ ] Coverage 목표 달성
- [ ] 문서 업데이트 (필요시)
- [ ] CI/CD 통과
- [ ] 브랜치 푸시 완료

---

## 노트 (작업 중 추가)

### 진행 상황
{작업 진행하면서 메모}

### 발견한 이슈
{작업 중 발견한 문제점이나 개선사항}

### 변경사항
{계획과 다르게 변경된 사항 - 이유와 함께}

---

**Created**: {날짜}
**Assigned**: {담당 에이전트}
**Status**: Pending / In Progress / Completed
**Updated**: {마지막 업데이트}
