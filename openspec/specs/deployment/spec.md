# 배포 스펙 — FastAPI + Vercel

## 결정: 방법 A (api/index.py 진입점)

FastAPI 백엔드를 Vercel Serverless Function으로 직접 배포한다.

### 구조

| 환경 | 실행 방식 | DB |
|------|----------|----|
| 로컬 | `uvicorn main:app --reload` | SQLite (`taskflow.db`) |
| 운영 | Vercel Serverless (`api/index.py`) | Neon PostgreSQL |

### 진입점 규칙

- `api/index.py` 에서 FastAPI `app` 을 import해서 Vercel이 핸들링
- 모든 `/api/*` 요청은 이 함수로 라우팅
- `DATABASE_URL` 환경변수 하나로 로컬 ↔ 운영 전환

### 이유

- "학습 단순 + 실전 표준 동시" 목표에 부합
- 서비스 1개로 FE + BE 통합 배포 가능
- 로컬과 운영 코드 분기 최소화

### 트레이드오프

- cold start 있음 (첫 요청 지연 가능)
- 로컬(`uvicorn`)과 운영(`Serverless`) 실행 구조가 다름
  → `api/index.py`와 `main.py` 분리로 해결
