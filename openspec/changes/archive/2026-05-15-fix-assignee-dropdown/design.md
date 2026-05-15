## Context

기존 `kanban.html`의 `openAddCard()` 함수는 제목 입력 후 Enter 시 `assignee_id: user.id`를 하드코딩해서 전송한다. 카드 상세 모달의 "다른 담당자 지정" 버튼은 클릭해도 아무 동작이 없다. 백엔드 API는 이미 `assignee_id`를 완전히 지원하므로 프론트엔드만 수정한다.

## Goals / Non-Goals

**Goals:**
- 인라인 카드 생성 시 담당자 선택 드롭다운 (팀 멤버 + 미할당)
- 카드 상세 모달에서 담당자 변경 가능
- assignee 표시를 이메일 전체로 개선

**Non-Goals:**
- 백엔드 API 변경
- 담당자 검색/필터링
- 다중 담당자

## Decision: 드롭다운 구현 방식

**선택**: 네이티브 `<select>` 요소 사용
**이유**: Vanilla JS 프로젝트이므로 커스텀 드롭다운 라이브러리 불필요. 팀 멤버가 5명 이하이므로 select로 충분.
**대안**: 커스텀 드롭다운 → 구현 복잡도 증가, MVP 범위 초과

## 구현 방식

### 1. 인라인 입력 박스 (openAddCard)

```
현재: 제목 input + Enter/Esc 안내
변경: 제목 input + 담당자 select + Enter/Esc 안내
```

- `members` 배열이 이미 `loadMembers()`로 로드되어 있으므로 재사용
- select 옵션: 각 멤버(이메일) + 미할당(null)
- 기본값: 현재 사용자 (`user.id`)

### 2. 카드 상세 모달 (openModal / saveModal)

```
현재: assignee 텍스트 표시 + "다른 담당자 지정" 버튼 (미작동)
변경: assignee select 드롭다운으로 교체
```

- 모달 열릴 때 현재 assignee로 select 초기화
- 저장 시 선택된 assignee_id 포함해서 `PUT /tasks/{id}` 호출

### 3. 카드 표시 개선

```
현재: #3 · s1  (이름 축약)
변경: #3 · s1@test.co.kr  (이메일 전체)
```

- `memberEmail()` 함수 수정: `m.email.split('@')[0]` → `m.email`
- 단, 현재 사용자는 여전히 `@me` 표시

## 영향 범위

`frontend/kanban.html` 내 3개 함수만 수정:
1. `openAddCard()` — 인라인 입력에 select 추가
2. `openModal()` — 모달에 assignee select 렌더링
3. `saveModal()` — select에서 assignee_id 읽어 저장
4. `memberEmail()` — 이메일 표시 방식 개선
