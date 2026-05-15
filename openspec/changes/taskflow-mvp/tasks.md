## 1. 프로젝트 구조 및 환경 설정

- [x] 1.1 디렉토리 구조 생성: `backend/`, `frontend/`, `api/`
- [x] 1.2 `backend/requirements.txt` 작성 (fastapi, uvicorn, sqlalchemy, bcrypt, python-jose, psycopg2-binary, python-dotenv)
- [x] 1.3 `.env` 파일 생성, `DATABASE_URL=sqlite:///./taskflow.db` 설정
- [x] 1.4 `backend/database.py`: SQLAlchemy engine + SessionLocal (DATABASE_URL 환경변수 기반)
- [x] 1.5 `backend/models.py`: users, teams, tasks, messages 4테이블 + 인덱스 정의
- [x] 1.6 `backend/main.py`: FastAPI 앱 생성, CORS 설정, 라우터 등록
- [x] 1.7 `api/index.py`: Vercel 진입점 (`from backend.main import app`)
- [x] 1.8 DB 테이블 생성 확인 (`uvicorn backend.main:app --reload` 실행)

## 2. 인증 (Auth)

- [x] 2.1 `backend/routers/auth.py` 생성
- [x] 2.2 `POST /auth/signup`: 이메일 유효성 검증, 중복 체크(409), bcrypt 해시, JWT 발급, 201 반환
- [x] 2.3 `POST /auth/login`: 자격증명 검증, INVALID_CREDENTIALS(401), JWT(24h) 발급
- [x] 2.4 `POST /auth/logout`: 200 반환 (stateless)
- [x] 2.5 `GET /auth/me`: JWT 디코드, 현재 사용자 반환
- [x] 2.6 JWT 인증 미들웨어/의존성 구현 (`get_current_user`)
- [x] 2.7 에러 응답 표준 헬퍼 `{ error: { code, message } }` 구현

## 3. 팀 (Team)

- [x] 3.1 `backend/routers/teams.py` 생성
- [x] 3.2 `POST /teams`: 팀 생성, 초대코드 자동생성(`^[A-Z]{4}-[0-9]{4}$`), `users.team_id` 업데이트
- [x] 3.3 `POST /teams/join`: 초대코드 형식 검증(400), 존재 확인(404), 중복 합류(409), `users.team_id` 업데이트
- [x] 3.4 `GET /teams/{id}`: 팀 정보 반환, 비멤버 403
- [x] 3.5 `GET /teams/{id}/members`: 멤버 목록 + role(owner/member) 반환
- [x] 3.6 `DELETE /teams/{id}/leave`: owner 탈퇴 시 409, 멤버는 `team_id = null`

## 4. 칸반 (Kanban)

- [x] 4.1 `backend/routers/tasks.py` 생성
- [x] 4.2 `GET /teams/{id}/tasks`: `created_at DESC` 정렬, `filter=me/unassigned` 지원
- [x] 4.3 `POST /teams/{id}/tasks`: title 필수 검증, `status=TODO`, `creator_id=현재유저`, `assignee_id` nullable
- [x] 4.4 `GET /tasks/{id}`: 단일 태스크 반환, 존재 않으면 404
- [x] 4.5 `PUT /tasks/{id}`: title·assignee_id 수정
- [x] 4.6 `PATCH /tasks/{id}/status`: TODO/DOING/DONE 값 검증(400), 상태 업데이트
- [x] 4.7 `DELETE /tasks/{id}`: creator 또는 owner만 허용, 그 외 403

## 5. 채팅 (Chat)

- [x] 5.1 `backend/routers/messages.py` 생성
- [x] 5.2 `GET /teams/{id}/messages`: `since` 없으면 최근 50개, 있으면 이후 메시지만 반환 (`created_at ASC`)
- [x] 5.3 `POST /teams/{id}/messages`: 1-1000자 검증(400 TOO_LONG), 201 반환
- [x] 5.4 `DELETE /messages/{id}`: 본인 메시지만 허용, 타인 시도 403 NOT_OWNER

## 6. 프론트엔드 — 인증 화면

- [x] 6.1 `frontend/login.html`: 로그인 + 회원가입 링크
- [x] 6.2 `frontend/signup.html`: 회원가입 폼 (이메일 형식, 8자 이상 클라이언트 검증)
- [x] 6.3 `frontend/js/auth.js`: JWT localStorage 저장/삭제, 401 인터셉터 → `/login` redirect
- [x] 6.4 회원가입 에러 인라인 표시 (EMAIL_TAKEN, VALIDATION_ERROR)

## 7. 프론트엔드 — 팀 선택 화면

- [x] 7.1 `frontend/team.html`: 팀 만들기 + 초대코드 합류 2-panel 화면
- [x] 7.2 팀 생성 폼: POST /teams, 초대코드 표시 + 클립보드 복사
- [x] 7.3 초대코드 합류 폼: 형식 검증(`^[A-Z]{4}-[0-9]{4}$`), 에러 인라인 표시
- [x] 7.4 로그인 후 분기: `team_id == null` → `/team.html`, `team_id != null` → `/kanban.html`

## 8. 프론트엔드 — 칸반 화면

- [x] 8.1 `frontend/kanban.html`: 3컬럼(TODO/DOING/DONE) 레이아웃 + 헤더 탭(칸반/채팅/멤버)
- [x] 8.2 태스크 카드 렌더링: 제목, `#id`, `@assignee` 표시
- [x] 8.3 필터 버튼: 전체 / @me / 미할당
- [x] 8.4 `+` 버튼 → 인라인 입력 (Enter 저장, Esc 취소)
- [x] 8.5 HTML5 Drag & Drop: dragstart/dragover/drop → `PATCH /tasks/{id}/status`
- [x] 8.6 카드 클릭 → 상세 모달 (제목수정, 상태변경, assignee변경, 삭제)
- [x] 8.7 빈 컬럼 empty state 표시
- [x] 8.8 모바일 반응형: `< 768px` 1컬럼 스와이프 + 햄버거 메뉴

## 9. 프론트엔드 — 채팅 화면

- [x] 9.1 `frontend/chat.html`: 말풍선 UI, 본인/타인 구분 (우측/좌측)
- [x] 9.2 5초 폴링: `setInterval(5000)` + `?since=<마지막메시지 created_at>`
- [x] 9.3 메시지 입력창: 1000자 카운터, 초과 시 적색 + 전송 버튼 disable
- [x] 9.4 본인 메시지 호버 → 삭제 아이콘 표시, 클릭 시 `DELETE /messages/{id}`
- [x] 9.5 폴링 실패 시 헤더에 "연결 끊김" 표시, exponential backoff 재시도
- [x] 9.6 빈 채팅 empty state 표시

## 10. 프론트엔드 — 멤버 목록

- [x] 10.1 멤버 사이드 패널 또는 별도 화면: `GET /teams/{id}/members` 렌더링
- [x] 10.2 owner는 ★ 표시, 가입일 표시

## 11. 배포

- [ ] 11.1 Neon PostgreSQL 프로젝트 생성, 연결 문자열 확보
- [x] 11.2 `vercel.json` 또는 `vercel.ts` 작성: `/api/*` → `api/index.py` 라우팅
- [ ] 11.3 Vercel 프로젝트 생성 + GitHub 연동
- [ ] 11.4 Vercel 환경변수 설정: `DATABASE_URL`, `JWT_SECRET`
- [ ] 11.5 `git push origin main` → 자동 배포 확인
- [ ] 11.6 운영 URL에서 회원가입 → 팀 생성 → 칸반 → 채팅 전 기능 동작 확인
