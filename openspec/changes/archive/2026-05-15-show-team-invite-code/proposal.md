## Why

팀에 합류한 후 초대코드를 다시 확인할 방법이 없다. 팀 리더가 새 멤버를 초대하려면 초대코드를 기억하거나 앱을 재설치해야 한다. 멤버 화면에 초대코드를 표시하면 언제든 공유할 수 있다.

## What Changes

- **멤버 화면(`members.html`)에 초대코드 섹션 추가**: 팀 이름 아래에 초대코드 표시 + 클립보드 복사 버튼
- **초대코드는 owner에게만 표시**: member 역할은 보안상 숨김. `GET /teams/{id}` 응답의 `invite_code` 활용

## Capabilities

### New Capabilities

_(없음)_

### Modified Capabilities

- `team`: 팀 정보 조회 시 초대코드 노출 범위 요구사항 구체화 (owner만 표시)

## Impact

- **Frontend**: `frontend/members.html` 수정
- **Backend**: 변경 없음 (`GET /teams/{id}` 이미 `invite_code` 반환 중)
- **API**: 기존 `GET /teams/{id}` 재활용
