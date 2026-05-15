## Why

소규모 팀이 태스크 진행 상황과 의사결정을 한 화면에서 추적할 수 있는 도구가 없다. TaskFlow MVP는 칸반 보드와 실시간 채팅을 결합해 3-5인 팀이 별도 도구 없이 업무를 진행할 수 있도록 한다.

## What Changes

- **인증 시스템 신규**: 이메일/비밀번호 회원가입·로그인, JWT 발급(24h), bcrypt 해싱
- **팀 관리 신규**: 팀 생성, 초대코드(`AAAA-9999` 형식) 발급·검증, 멤버 합류 (1인 1팀 원칙)
- **칸반 보드 신규**: TODO/DOING/DONE 3컬럼, 카드 추가·드래그 이동·삭제, assignee 지정
- **채팅 신규**: 팀 단위 메시지 송수신, 5초 폴링(`since=` 증분), 1000자 제한
- **배포 신규**: Vercel(FE+BE) + Neon PostgreSQL, 로컬은 SQLite로 환경 분리

## Capabilities

### New Capabilities

- `auth`: 회원가입·로그인·로그아웃·JWT 검증. 4개 엔드포인트
- `team`: 팀 생성·초대코드 발급·합류·멤버 목록·팀 정보 조회·탈퇴. 5개 엔드포인트
- `kanban`: 태스크 CRUD + 상태 변경(PATCH 별도). 6개 엔드포인트, assignee nullable
- `chat`: 메시지 송수신·삭제, 폴링 기반 실시간성. 3개 엔드포인트
- `deployment`: Vercel Serverless(api/index.py) + Neon, DATABASE_URL로 환경 전환

### Modified Capabilities

- `deployment`: 배포 방식 결정 — Vercel Serverless Function(api/index.py) 진입점 방식 채택 (기존 spec에서 구체화)

## Impact

- **Backend**: FastAPI, SQLAlchemy, bcrypt, python-jose. DB 4테이블(users·teams·tasks·messages)
- **Frontend**: Vanilla JS(ES6+), Tailwind CSS CDN. 9개 화면, HTML5 Drag API
- **API**: 18개 엔드포인트 (Auth 4 + Team 5 + Task 6 + Chat 3)
- **인프라**: Vercel(프론트+백), Neon PostgreSQL(운영), SQLite(로컬)
- **범위 외**: WebSocket, 파일첨부, 검색, 다국어, 테스트자동화, 알림, 권한세분화
