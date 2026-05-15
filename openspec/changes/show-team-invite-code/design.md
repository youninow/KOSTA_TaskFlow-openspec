## Context

`members.html`은 현재 `GET /teams/{id}/members`로 멤버 목록만 가져온다. `GET /teams/{id}`는 이미 `invite_code`를 반환하지만 멤버 화면에서 사용하지 않는다. 두 API를 모두 호출해서 팀 정보와 멤버 목록을 함께 표시한다.

## Goals / Non-Goals

**Goals:**
- 멤버 화면 상단에 초대코드 표시 + 복사 버튼
- owner만 초대코드 노출 (member는 숨김)

**Non-Goals:**
- 초대코드 재발급 기능
- 초대 링크 생성

## 구현 방식

### 레이아웃

```
┌──────────────────────────────┐
│  팀 이름                      │
│                              │
│  초대코드 (owner만 표시)       │
│  ┌────────────────────────┐  │
│  │  FRNT-2026    📋 복사   │  │
│  └────────────────────────┘  │
│                              │
│  팀 멤버 (3)                  │
│  ─────────────────────────   │
│  L leader@ex.com  ★ owner   │
│  U user@ex.com    member    │
└──────────────────────────────┘
```

### 권한 체크 방법

`GET /teams/{id}/members` 응답에서 현재 사용자의 role을 확인:
```javascript
const me = members.find(m => m.id === user.id);
if (me?.role === 'owner') { // 초대코드 섹션 표시 }
```

### 복사 버튼

`navigator.clipboard.writeText(code)` 사용. 복사 성공 시 버튼 텍스트를 "✓ 복사됨"으로 1.5초간 변경 후 원복.

## 영향 범위

`frontend/members.html`의 `load()` 함수와 HTML 섹션만 수정.
