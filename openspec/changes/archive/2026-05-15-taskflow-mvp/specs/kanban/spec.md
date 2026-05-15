## ADDED Requirements

### Requirement: 태스크 목록 조회
시스템은 팀의 태스크를 `created_at DESC` 순으로 반환해야 한다. `filter` 파라미터로 `@me`(assignee_id = 현재 유저), `unassigned`(assignee_id IS NULL) 필터링을 지원한다.

#### Scenario: 전체 조회
- **WHEN** 팀 멤버가 `GET /teams/{id}/tasks` 호출
- **THEN** HTTP 200, `[{ id, title, status, creator_id, assignee_id, created_at }]` 반환 (created_at DESC)

#### Scenario: 내 태스크 필터
- **WHEN** `GET /teams/{id}/tasks?filter=me` 호출
- **THEN** `assignee_id = current_user_id`인 태스크만 반환

#### Scenario: 미할당 필터
- **WHEN** `GET /teams/{id}/tasks?filter=unassigned` 호출
- **THEN** `assignee_id IS NULL`인 태스크만 반환

---

### Requirement: 태스크 생성
시스템은 팀 멤버가 태스크를 생성할 수 있어야 한다. 초기 status는 항상 `TODO`. `assignee_id`는 nullable.

#### Scenario: 정상 생성
- **WHEN** `POST /teams/{id}/tasks { title, assignee_id? }` 호출
- **THEN** HTTP 201, `{ id, title, status: "TODO", creator_id, assignee_id, created_at }` 반환

#### Scenario: 제목 누락
- **WHEN** title 없이 `POST /teams/{id}/tasks` 호출
- **THEN** HTTP 400, `{ error: { code: "VALIDATION_ERROR", message: "제목을 입력해주세요" } }` 반환

---

### Requirement: 태스크 상세 조회
시스템은 단일 태스크 상세 정보를 반환해야 한다.

#### Scenario: 정상 조회
- **WHEN** 팀 멤버가 `GET /tasks/{id}` 호출
- **THEN** HTTP 200, `{ id, title, status, creator_id, assignee_id, created_at }` 반환

#### Scenario: 존재하지 않는 태스크
- **WHEN** 없는 task id로 `GET /tasks/{id}` 호출
- **THEN** HTTP 404, `{ error: { code: "NOT_FOUND", message: "해당 항목을 찾을 수 없습니다" } }` 반환

---

### Requirement: 태스크 제목·담당자 수정
시스템은 팀 멤버가 태스크의 title과 assignee_id를 수정할 수 있어야 한다.

#### Scenario: 정상 수정
- **WHEN** `PUT /tasks/{id} { title?, assignee_id? }` 호출
- **THEN** HTTP 200, 수정된 태스크 반환

---

### Requirement: 태스크 상태 변경
시스템은 태스크 상태를 `TODO`, `DOING`, `DONE` 중 하나로 변경할 수 있어야 한다. 드래그 앤 드롭의 drop 이벤트에서 호출된다.

#### Scenario: 정상 상태 변경
- **WHEN** `PATCH /tasks/{id}/status { status: "DOING" }` 호출
- **THEN** HTTP 200, `{ id, status: "DOING" }` 반환

#### Scenario: 유효하지 않은 상태값
- **WHEN** `status`가 `TODO/DOING/DONE` 외 값으로 `PATCH /tasks/{id}/status` 호출
- **THEN** HTTP 400, `{ error: { code: "VALIDATION_ERROR", message: "올바른 상태값이 아닙니다" } }` 반환

---

### Requirement: 태스크 삭제 권한
creator 또는 team owner만 태스크를 삭제할 수 있다. 그 외는 403.

#### Scenario: creator가 삭제
- **WHEN** `creator_id = current_user_id`인 태스크에 `DELETE /tasks/{id}` 호출
- **THEN** HTTP 200, `{}` 반환

#### Scenario: owner가 타인 카드 삭제
- **WHEN** team owner가 타인의 태스크에 `DELETE /tasks/{id}` 호출
- **THEN** HTTP 200, `{}` 반환

#### Scenario: 권한 없는 삭제 시도
- **WHEN** creator도 owner도 아닌 멤버가 `DELETE /tasks/{id}` 호출
- **THEN** HTTP 403, `{ error: { code: "FORBIDDEN", message: "권한이 없습니다" } }` 반환
