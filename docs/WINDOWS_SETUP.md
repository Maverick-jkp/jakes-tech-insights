# Windows Environment Setup Guide

이 문서는 맥북에서 윈도우로 전환 후 프로젝트 개발 환경 설정에 필요한 내용을 정리합니다.

## 목차
- [Git 설정](#git-설정)
- [GitHub CLI 설치](#github-cli-설치)
- [PATH 환경변수](#path-환경변수)
- [PowerShell 사용](#powershell-사용)
- [트러블슈팅](#트러블슈팅)

---

## Git 설정

### 사용자 정보 설정
윈도우에서 처음 Git을 사용할 때 반드시 설정해야 합니다.

```bash
git config --global user.name "Maverick-jkp"
git config --global user.email "neoclones@gmali.com"
```

**참고:** 명령어 실행 시 아무 출력도 나오지 않으면 정상입니다.

### 설정 확인
```bash
git config --global user.name
git config --global user.email
```

### 기본 에디터 설정 (선택사항)
```bash
git config --global core.editor "code --wait"  # VSCode 사용 시
```

---

## GitHub CLI 설치

### 설치 방법

#### 방법 1: winget (권장)
```bash
winget install --id GitHub.cli
```

#### 방법 2: Chocolatey
```bash
choco install gh
```

#### 방법 3: 직접 다운로드
https://cli.github.com/ 에서 Windows용 설치 파일 다운로드

### 설치 후 인증
```bash
gh auth login
```

브라우저를 통해 GitHub 계정으로 인증합니다.

### 설치 확인
```bash
gh --version
```

---

## PATH 환경변수

### 문제 상황
GitHub CLI 설치 후 `gh` 명령어가 인식되지 않는 경우:

```
gh : The term 'gh' is not recognized as the name of a cmdlet...
```

### 해결 방법

#### 1. PowerShell 재시작 (가장 간단)
PowerShell 창을 완전히 닫고 다시 열면 PATH가 업데이트됩니다.

#### 2. 현재 세션에 PATH 반영
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

#### 3. 전체 경로로 실행
PATH가 업데이트되기 전에 바로 사용해야 할 때:
```powershell
& "C:\Program Files\GitHub CLI\gh.exe" --version
```

### GitHub CLI 기본 설치 경로
- `C:\Program Files\GitHub CLI\gh.exe`

---

## PowerShell 사용

### 기본 명령어

#### 디렉토리 이동
```powershell
cd C:\Users\user\Desktop\jakes-insights
```

#### Git 작업
```powershell
git status
git add .
git commit -m "commit message"
git push
```

#### GitHub CLI 사용
프로젝트 폴더에서 실행해야 합니다:
```powershell
cd C:\Users\user\Desktop\jakes-insights
gh run list --workflow=daily-keywords.yml --limit 5
gh run view <run-id> --log
```

### 명령어 복사 시 주의사항
- PowerShell 프롬프트(`PS C:\Users\user>`)는 복사하지 마세요
- 명령어만 깨끗하게 복사해서 붙여넣기
- 에러 메시지 전체를 복사해서 실행하면 안 됩니다

---

## 트러블슈팅

### 1. Git: Author identity unknown

**문제:**
```
Author identity unknown
*** Please tell me who you are.
```

**해결:**
```bash
git config --global user.name "Maverick-jkp"
git config --global user.email "neoclones@gmali.com"
```

### 2. GitHub CLI: 명령어 인식 안 됨

**문제:**
```
gh : The term 'gh' is not recognized...
```

**해결:**
1. PowerShell 재시작
2. 또는 전체 경로 사용: `& "C:\Program Files\GitHub CLI\gh.exe" <command>`

### 3. GitHub CLI: 인증 필요

**문제:**
```
To get started with GitHub CLI, please run: gh auth login
```

**해결:**
```bash
gh auth login
```

### 4. Git repository not found

**문제:**
```
failed to determine base repo: failed to run git: fatal: not a git repository
```

**해결:**
프로젝트 폴더로 이동:
```bash
cd C:\Users\user\Desktop\jakes-insights
```

---

## 자주 사용하는 워크플로우

### GitHub Actions 로그 확인
```powershell
# 프로젝트 폴더로 이동
cd C:\Users\user\Desktop\jakes-insights

# 최근 워크플로우 실행 목록
gh run list --workflow=daily-content.yml --limit 5

# 특정 실행의 상세 로그
gh run view <run-id> --log

# 워크플로우 수동 실행
gh workflow run daily-content.yml
```

### Git 기본 워크플로우
```bash
# 변경사항 확인
git status

# 파일 추가
git add <file-path>

# 커밋
git commit -m "commit message"

# 푸시
git push
```

---

## 참고 링크

- [Git 공식 문서](https://git-scm.com/doc)
- [GitHub CLI 공식 문서](https://cli.github.com/manual/)
- [PowerShell 공식 문서](https://docs.microsoft.com/en-us/powershell/)

---

**최종 업데이트:** 2026-01-20
**작성자:** Maverick-jkp (with Claude)
