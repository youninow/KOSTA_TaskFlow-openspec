## ADDED Requirements

### Requirement: 로컬 개발 환경
시스템은 로컬에서 SQLite + uvicorn으로 실행되어야 한다. 프론트엔드는 빌드 없이 정적 파일을 직접 열거나 live-server로 제공한다.

#### Scenario: 로컬 백엔드 실행
- **WHEN** `uvicorn main:app --reload` 실행
- **THEN** FastAPI 서버가 `http://localhost:8000`에서 동작, SQLite(`taskflow.db`) 연결

#### Scenario: 로컬 DB 전환
- **WHEN** `DATABASE_URL=sqlite:///./taskflow.db` 환경변수 설정 후 실행
- **THEN** SQLite 파일 기반 DB 사용

---

### Requirement: Vercel 배포 구조 (방법 A)
시스템은 `api/index.py`를 Vercel Serverless Function 진입점으로 사용해야 한다. 프론트엔드 정적 파일은 Vercel이 직접 서빙한다.

#### Scenario: 운영 배포
- **WHEN** `git push origin main` 실행
- **THEN** Vercel이 자동으로 프론트엔드 정적 파일과 `api/index.py` Serverless Function을 배포

#### Scenario: API 라우팅
- **WHEN** 브라우저가 `/api/*` 경로로 요청
- **THEN** Vercel이 `api/index.py`의 FastAPI 앱으로 라우팅

---

### Requirement: 환경변수 기반 DB 전환
`DATABASE_URL` 환경변수 하나로 로컬(SQLite) ↔ 운영(Neon PostgreSQL)을 전환해야 한다. 코드 변경 없이 환경변수만으로 전환된다.

#### Scenario: 운영 DB 연결
- **WHEN** Vercel 환경변수에 `DATABASE_URL=postgres://...neon.tech/...` 설정
- **THEN** FastAPI 앱이 Neon PostgreSQL에 연결

#### Scenario: 로컬 SQLite 연결
- **WHEN** `DATABASE_URL=sqlite:///./taskflow.db` 설정
- **THEN** FastAPI 앱이 로컬 SQLite 파일에 연결

---

### Requirement: Neon PostgreSQL 운영 DB
운영 환경은 Vercel Marketplace의 Neon PostgreSQL을 사용한다. Neon free 플랜의 자동 백업과 point-in-time recovery를 활용한다.

#### Scenario: Neon 연결 확인
- **WHEN** Vercel 배포 후 `GET /auth/me` 호출
- **THEN** HTTP 200 또는 401 반환 (DB 연결 오류 없음)
