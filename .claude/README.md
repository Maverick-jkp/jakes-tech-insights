# 🤖 Multi-Agent Development System

이 디렉토리는 Jake's Tech Insights 프로젝트의 **멀티 에이전트 개발 시스템**을 위한 문서와 템플릿을 포함합니다.

---

## 📁 디렉토리 구조

```
.claude/
├── README.md                    # 이 파일
├── agents/                      # 에이전트 역할 정의
│   ├── MASTER.md               # Master Agent (Tech Lead)
│   ├── CTO.md                  # CTO (아키텍처 + 백엔드)
│   ├── DESIGNER.md             # Designer (UI/UX)
│   └── QA.md                   # QA (테스트 + 품질)
├── workflows/                   # 워크플로우 가이드
│   └── feature-workflow.md     # 기능 개발 워크플로우
├── templates/                   # 템플릿
│   └── task-template.md        # 작업 티켓 템플릿
└── tasks/                       # 작업 티켓 (동적 생성)
    └── (작업별 MD 파일)
```

---

## 🎯 시스템 개요

### 목적
복잡한 기능 개발 시 **여러 세션에서 병렬로 작업**할 수 있도록 역할 기반 에이전트 시스템 제공

### 핵심 원칙
1. **Master가 조율**: 작업 분해, 티켓 생성, 최종 통합
2. **전문화된 에이전트**: 각 에이전트는 명확한 역할과 책임 (같은 에이전트를 여러 세션에서 사용 가능)
3. **브랜치 기반 작업**: 각 작업은 독립 브랜치에서 진행
4. **Master만 커밋**: 다른 에이전트는 커밋만, 머지는 Master가 통합

### 유연한 사용
- **역할 = 컨텍스트**: MD 파일은 "어떤 관점으로 접근할지" 가이드
- **같은 역할 멀티 세션 가능**: 여러 세션에서 모두 CTO 역할 사용 가능
- **Master 올인원도 가능**: 간단한 작업은 Master가 직접 처리

---

## 👥 에이전트 역할

### 🎯 MASTER (Tech Lead / PM)
- **역할**: 전체 조율 및 최종 통합
- **권한**: 커밋, 머지, 배포
- **주요 작업**:
  - 요구사항 분석 및 작업 분해
  - 티켓 생성 및 에이전트 할당
  - 브랜치 검토 및 통합
  - 최종 배포

### 🏗️ CTO (Chief Technology Officer)
- **역할**: 기술 전반 (아키텍처 + 백엔드)
- **권한**: 아키텍처 변경, 백엔드 개발, 성능 최적화
- **주요 작업**:
  - 아키텍처 설계 및 기술 스택 선택
  - Python 스크립트 개발
  - API 통합 (Anthropic, Google, Unsplash)
  - 성능 최적화 및 인프라 관리
  - 데이터 처리 및 에러 핸들링

### 🎨 DESIGNER (UI/UX Specialist)
- **역할**: UI/UX 디자인 및 프론트엔드
- **권한**: 디자인 시스템, 레이아웃
- **주요 작업**:
  - 페이지 레이아웃 및 컴포넌트 디자인
  - 디자인 시스템 관리
  - Hugo 템플릿 및 CSS 작성
  - 접근성 확보 (WCAG AA)
  - 반응형 디자인

### 🧪 QA (Quality Assurance)
- **역할**: 테스트 및 품질 보증
- **권한**: 테스트 전략, Coverage 관리
- **주요 작업**:
  - 유닛/통합 테스트 작성 (pytest)
  - Coverage 관리 (>50% 목표)
  - 품질 게이트 관리
  - 테스트 인프라 구축
  - 버그 재현 및 검증

---

## 🔄 워크플로우

### 1. 사용자 요청

```
예: "다크모드 추가하고, 성능 최적화하고, 테스트 커버리지 70%로 올려줘"
```

### 2. Master 분석 및 분해

```markdown
Master 세션 (세션 1):
1. 요구사항 분석
2. 작업 분해:
   - TASK_001: 다크모드 (DESIGNER)
   - TASK_002: 성능 최적화 (CTO)
   - TASK_003: 테스트 커버리지 (QA)

3. 의존성 분석:
   - 다크모드: 독립 ✓
   - 성능: 독립 ✓
   - 테스트: 다크모드 + 성능 완료 후

4. 브랜치 전략:
   Phase 1: [다크모드, 성능] 병렬
   Phase 2: [테스트] 순차

5. 티켓 생성:
   - .claude/tasks/TASK_001_dark_mode.md
   - .claude/tasks/TASK_002_performance.md
   - .claude/tasks/TASK_003_test_coverage.md
```

### 3. 병렬 작업 시작 (사용자)

```markdown
사용자가 새 세션 열기:

세션 2 (DESIGNER):
"TASK_001_dark_mode.md 읽고 작업 시작해"
→ feature/dark-mode 브랜치에서 작업
→ 커밋 및 푸시
→ "완료했습니다" 보고

세션 3 (CTO):
"TASK_002_performance.md 읽고 작업 시작해"
→ feature/performance 브랜치에서 작업
→ 커밋 및 푸시
→ "완료했습니다" 보고
```

### 4. 통합 (Master)

```markdown
세션 1 (Master):
"모든 작업 완료했으니 통합해줘"

Master 수행:
1. 각 브랜치 검토
2. 충돌 확인
3. 순차 머지:
   - feature/dark-mode
   - feature/performance
4. 통합 테스트
5. 최종 푸시
```

### 5. 순차 작업 (필요시)

```markdown
세션 4 (DEV_TESTING):
"TASK_003_test_coverage.md 읽고 작업 시작해"
→ feature/test-coverage 브랜치
→ 통합된 코드 기반 테스트 작성
→ 커밋 및 푸시

세션 1 (Master):
→ feature/test-coverage 머지
→ 최종 배포
```

---

## 📝 사용 방법

### 새 기능 개발

1. **Master 세션에서 시작**
   ```
   "새 기능 {기능명} 추가해줘"
   ```

2. **Master가 분석 및 티켓 생성**
   - `.claude/tasks/` 에 티켓 생성
   - 병렬/순차 계획 수립

3. **새 세션 열어서 작업**
   ```
   각 세션에서:
   "TASK_{ID}_{name}.md 읽고 작업 시작해"
   ```

4. **Master 세션으로 돌아와서 통합**
   ```
   "모든 작업 완료했으니 통합 및 배포해줘"
   ```

### 간단한 작업

```
Master가 직접 처리:
"로그인 버튼 색상 변경"
→ 에이전트 분리 불필요
→ 바로 처리
```

---

## 🚨 중요 규칙

### 1. 브랜치 전략
- **Master만 main 브랜치에 커밋/머지**
- 다른 에이전트는 feature 브랜치만 사용
- 브랜치명: `feature/{기능명}`, `fix/{버그명}`

### 2. 커밋 권한
- **Master**: 모든 브랜치 커밋 및 머지
- **다른 에이전트**: 자신의 feature 브랜치에만 커밋 (머지 안 함)

### 3. 테스트 필수
- 통합 전 모든 테스트 통과 필수
- CI/CD 실패 시 재작업

### 4. 충돌 해결
- Master가 충돌 감지 시 담당 에이전트와 상의
- 복잡한 충돌은 순차 작업으로 전환

---

## 📖 참고 문서

### 에이전트 가이드
- [MASTER.md](agents/MASTER.md): Master Agent 전체 가이드 (조율, 통합, 배포)
- [CTO.md](agents/CTO.md): CTO 역할 (아키텍처 + 백엔드 + 성능)
- [DESIGNER.md](agents/DESIGNER.md): Designer 역할 (UI/UX + 프론트엔드)
- [QA.md](agents/QA.md): QA 역할 (테스트 + 품질 보증)

### 워크플로우
- [feature-workflow.md](workflows/feature-workflow.md): 기능 개발 전체 흐름

### 템플릿
- [task-template.md](templates/task-template.md): 작업 티켓 템플릿

---

## 🎓 예시 시나리오

### 시나리오 1: 복잡한 기능 추가

**요청**: "사용자 인증 시스템 추가"

**Master 분석**:
```
복잡도: 높음
작업 분해:
1. 아키텍처 설계 (CTO) - 문서화
2. Backend API (DEV_BACKEND) - 1번 후
3. 테스트 (DEV_TESTING) - 2번 후

실행 계획:
Phase 1: CTO (아키텍처 문서)
Phase 2: DEV_BACKEND (API 구현)
Phase 3: DEV_TESTING (테스트)
```

**실행**:
```
세션 1 (Master): 티켓 3개 생성
세션 2 (CTO): TASK_001 → 설계 문서 작성 → 완료
세션 3 (DEV_BACKEND): TASK_002 → API 구현 → 완료
세션 4 (DEV_TESTING): TASK_003 → 테스트 작성 → 완료
세션 1 (Master): 3개 브랜치 통합 → 배포
```

### 시나리오 2: 병렬 작업

**요청**: "다크모드 추가하고 이미지 최적화해줘"

**Master 분석**:
```
작업 분해:
1. 다크모드 (DESIGNER) - 독립
2. 이미지 최적화 (DEV_BACKEND) - 독립

병렬 가능: ✓ (서로 다른 파일)
```

**실행**:
```
세션 1 (Master): 티켓 2개 생성
세션 2 (DESIGNER): TASK_001 (병렬)
세션 3 (DEV_BACKEND): TASK_002 (병렬)
→ 동시 작업
세션 1 (Master): 2개 브랜치 통합
```

---

## 🔧 유지보수

### 에이전트 추가
새로운 역할이 필요하면:
1. `agents/{에이전트명}.md` 생성
2. 역할, 책임, 워크플로우 정의
3. `README.md` 업데이트

### 워크플로우 개선
1. 실제 사용 경험 기록
2. 비효율적인 부분 파악
3. 워크플로우 문서 업데이트

---

## 📞 문의

이 시스템에 대한 질문이나 개선 제안:
- Master 세션에서 직접 질문
- 또는 이 디렉토리 문서 업데이트 요청

---

**Created**: 2026-01-20
**Version**: 1.0
**Maintained By**: Master Agent
