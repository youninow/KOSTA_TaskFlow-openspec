## ADDED Requirements

### Requirement: 메시지 목록 조회 (폴링)
시스템은 팀의 채팅 메시지를 반환해야 한다. `since` 파라미터가 있으면 해당 시각 이후 메시지만 반환(증분 폴링). 없으면 최근 50개 반환.

#### Scenario: 최초 진입 조회
- **WHEN** `GET /teams/{id}/messages` 호출 (since 없음)
- **THEN** HTTP 200, 최근 50개 메시지를 `created_at ASC` 순으로 반환. `[{ id, user_id, user_email, content, created_at }]`

#### Scenario: 증분 폴링
- **WHEN** `GET /teams/{id}/messages?since=2026-05-13T14:27:00Z` 호출
- **THEN** HTTP 200, 해당 시각 이후 메시지만 반환. 없으면 `[]`

#### Scenario: 빈 채팅방
- **WHEN** 메시지가 없는 팀의 `GET /teams/{id}/messages` 호출
- **THEN** HTTP 200, `[]` 반환

---

### Requirement: 메시지 전송
시스템은 팀 멤버가 메시지를 전송할 수 있어야 한다. 메시지는 1-1000자여야 한다. 클라이언트와 서버 양쪽에서 검증한다.

#### Scenario: 정상 전송
- **WHEN** 1-1000자 content로 `POST /teams/{id}/messages` 호출
- **THEN** HTTP 201, `{ id, user_id, user_email, content, created_at }` 반환

#### Scenario: 1000자 초과
- **WHEN** 1001자 이상 content로 `POST /teams/{id}/messages` 호출
- **THEN** HTTP 400, `{ error: { code: "TOO_LONG", message: "메시지는 1000자 이내로 입력하세요", limit: 1000, actual: <실제길이> } }` 반환

#### Scenario: 빈 메시지
- **WHEN** 빈 문자열로 `POST /teams/{id}/messages` 호출
- **THEN** HTTP 400, `{ error: { code: "VALIDATION_ERROR", message: "메시지를 입력해주세요" } }` 반환

---

### Requirement: 메시지 삭제 (본인만)
시스템은 메시지 작성자 본인만 해당 메시지를 삭제할 수 있어야 한다. owner도 타인 메시지 삭제 불가.

#### Scenario: 본인 메시지 삭제
- **WHEN** `user_id = current_user_id`인 메시지에 `DELETE /messages/{id}` 호출
- **THEN** HTTP 200, `{}` 반환

#### Scenario: 타인 메시지 삭제 시도
- **WHEN** `user_id != current_user_id`인 메시지에 `DELETE /messages/{id}` 호출
- **THEN** HTTP 403, `{ error: { code: "NOT_OWNER", message: "본인의 메시지만 삭제할 수 있습니다" } }` 반환

---

### Requirement: 폴링 누락 없음 보장
`POST /messages`가 성공(201)한 메시지는 이후 모든 `GET /messages` 호출에서 반드시 노출되어야 한다. `since=` 파라미터로 재연결 시 누락 없이 동기화된다.

#### Scenario: 재연결 후 누락 메시지 수신
- **WHEN** 네트워크 끊김 후 `GET /teams/{id}/messages?since=<마지막수신시각>` 호출
- **THEN** 끊긴 동안 전송된 모든 메시지가 포함된 응답 반환
