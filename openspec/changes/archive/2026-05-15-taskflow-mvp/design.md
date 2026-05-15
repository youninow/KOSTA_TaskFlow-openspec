## Context

TaskFlow MVP는 그린필드 프로젝트. 기존 코드 없음. 목표는 3-5인 소규모 팀이 칸반 + 채팅을 한 화면에서 쓸 수 있는 최소 기능 제품을 Day 2 내에 완성하는 것. 스펙 품질이 AI 산출물 품질 상한을 결정한다는 원칙 하에 사전 정의 완료.

## Goals / Non-Goals

**Goals:**
- 인증·팀·칸반·채팅·배포 5종 기능 완성
- 로컬(SQLite) ↔ 운영(Neon) 환경 분리를 DATABASE_URL 하나로 처리
- Vercel 단일 배포로 FE + BE 동시 서빙

**Non-Goals:**
- WebSocket 실시간, 파일첨부, 검색, 다국어, 테스트 자동화
- JWT 갱신 토큰, 이메일 인증, rate limiting
- 팀 추방·역할 변경, 초대코드 재발급

## Decisions

### 1. 백엔드: FastAPI + SQLAlchemy

**선택**: FastAPI (Python, async, auto OpenAPI docs)
**이유**: SQLite ↔ PostgreSQL 전환이 DATABASE_URL 환경변수 하나로 되고, SQLAlchemy가 양쪽 dialect를 동일 코드로 처리. Pydantic으로 에러 응답 표준화 자동화.
**대안**: Django REST Framework → 설정 과다, MVP에 과함

### 2. Vercel 배포: api/index.py 진입점 방식 (방법 A)

**선택**: `api/index.py`에서 FastAPI `app`을 import, Vercel Serverless Function으로 노출
**이유**: 서비스 1개로 FE+BE 통합 배포, "학습 단순 + 실전 표준 동시" 목표에 부합
**대안**: 별도 백엔드 서비스(Railway/Render) → 서비스 2개 관리, 무료 티어 복잡
**트레이드오프**: cold start 있음(첫 요청 지연), 로컬 uvicorn과 운영 구조 다름

### 3. 프론트엔드: Vanilla JS + Tailwind CDN

**선택**: 프레임워크 없는 순수 ES6+, Tailwind CSS CDN
**이유**: 빌드 툴체인 없이 HTML 파일 직접 열기 가능 → 로컬 개발 단순화
**대안**: React/Vue → 빌드 설정 오버헤드, Day 2 범위 내 불필요

### 4. 인증: JWT (24h) + localStorage

**선택**: stateless JWT, 갱신 토큰 없음, localStorage 저장
**이유**: 서버 세션 관리 불필요, Vercel Serverless 무상태 환경에 적합
**트레이드오프**: 토큰 탈취 시 24h 내 강제 만료 불가 (MVP 범위 허용)

### 5. 실시간성: 5초 폴링 (since= 증분)

**선택**: setInterval 5초, `GET /teams/{id}/messages?since=<timestamp>` 증분 조회
**이유**: WebSocket 서버 유지 불필요, Serverless 환경과 호환, 구현 단순
**트레이드오프**: 최대 5초 지연 (MVP 허용 범위)

### 6. DB 스키마: 4테이블, 1인 1팀

**선택**: `users.team_id` (nullable FK), `tasks.assignee_id` (nullable FK)
**이유**:
- `users.team_id`: 멤버십 조회를 JOIN 없이 O(1)으로 처리
- `tasks.assignee_id`: '내 태스크' = `assignee_id = current_user` (creator 아님)

### 7. 권한 모델

| 역할 | tasks DELETE | messages DELETE |
|------|-------------|-----------------|
| owner | 모든 카드 | 본인만 |
| member (creator) | 본인 카드 | 본인만 |
| member (others) | 불가 | 본인만 |
| 비멤버 | 403 | 403 |

## Risks / Trade-offs

- **cold start**: Vercel Serverless Python cold start ~1-2s → 첫 요청 느릴 수 있음. MVP에서 허용.
- **1인 1팀 제약**: 팀 이동 불가(탈퇴 후 재가입). 명시적 범위 외.
- **owner 탈퇴**: `DELETE /teams/{id}/leave` 시 owner는 팀 삭제 처리. 멤버 데이터(tasks, messages)는 cascade 삭제 여부 명시 필요 → tasks/messages는 team에 종속되므로 CASCADE DELETE.
- **KST 가정**: Vercel 서버는 UTC 동작. DB에 UTC로 저장, 프론트에서 KST 표시 변환.
- **폴링 부하**: 동시 50명 × 5초 폴링 = 초당 10 req. Neon free tier 허용 범위.

## Migration Plan

그린필드 프로젝트이므로 마이그레이션 불필요.

배포 순서:
1. 로컬 개발 (SQLite, uvicorn)
2. Neon DB 생성 + DATABASE_URL 환경변수 설정
3. GitHub main push → Vercel 자동 배포
4. Vercel에서 환경변수 주입 확인 후 동작 검증

## Open Questions

- owner 탈퇴 시 팀 삭제 처리를 프론트에서 막을지, 서버에서 막을지? → **서버에서 409 반환, 프론트 안내**
- Tailwind CSS: CDN Play CDN(개발용)으로 시작, 빌드 필요 시 클로드코드 판단 위임
