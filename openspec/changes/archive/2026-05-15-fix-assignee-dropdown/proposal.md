## Why

카드 생성 시 담당자를 선택할 수 없어 항상 본인(@me)으로 고정된다. 팀 리더가 다른 멤버에게 태스크를 직접 배정할 수 없어 MVP의 핵심 워크플로우가 불완전하다.

## What Changes

- **카드 생성 인라인 입력에 담당자 드롭다운 추가**: 제목 입력창 아래에 팀 멤버 선택 드롭다운 표시. 기본값 @me, 미할당(null) 선택 가능
- **카드 상세 모달 assignee 변경 기능 완성**: 현재 "다른 담당자 지정" 버튼이 있지만 실제로 멤버 선택 UI가 없음 → 드롭다운으로 구현
- **카드 목록에 assignee 이메일 전체 표시**: 현재 `@me` / `s1` 등 불명확한 축약 표시 → `s1@test.co.kr` 전체 이메일 표시

## Capabilities

### New Capabilities

_(없음 — 기존 kanban 기능의 UX 수정)_

### Modified Capabilities

- `kanban`: 태스크 생성 시 assignee 선택 요구사항 변경. 카드 상세 모달의 assignee 변경 요구사항 구체화

## Impact

- **Frontend**: `frontend/kanban.html` — 인라인 입력 박스, 카드 상세 모달
- **Backend**: 변경 없음 (API는 이미 `assignee_id` 지원)
- **API**: `GET /teams/{id}/members` 추가 활용 (멤버 목록 드롭다운용)
