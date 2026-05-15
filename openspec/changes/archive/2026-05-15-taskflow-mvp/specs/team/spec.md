## ADDED Requirements

### Requirement: 팀 생성
시스템은 인증된 사용자가 팀을 생성할 수 있어야 한다. 생성자는 자동으로 owner가 되고, 초대코드(`^[A-Z]{4}-[0-9]{4}$`)가 서버에서 자동 생성된다. 생성 즉시 `users.team_id`가 업데이트된다.

#### Scenario: 정상 팀 생성
- **WHEN** 1-30자 팀 이름으로 `POST /teams` 호출
- **THEN** HTTP 201, `{ id, name, invite_code, owner_id, created_at }` 반환, `users.team_id` = 새 팀 id로 업데이트

#### Scenario: 이미 팀 소속인 사용자
- **WHEN** `team_id != null`인 사용자가 `POST /teams` 호출
- **THEN** HTTP 409, `{ error: { code: "ALREADY_IN_TEAM", message: "이미 다른 팀에 소속되어 있습니다" } }` 반환

---

### Requirement: 초대코드로 팀 합류
시스템은 초대코드 검증 후 `users.team_id`를 업데이트해야 한다.

#### Scenario: 정상 합류
- **WHEN** 유효한 초대코드로 `POST /teams/join` 호출
- **THEN** HTTP 200, `{ team: { id, name, member_count }, redirect: "/teams/{id}" }` 반환, `users.team_id` 업데이트

#### Scenario: 초대코드 형식 오류
- **WHEN** `^[A-Z]{4}-[0-9]{4}$` 패턴을 벗어난 코드로 `POST /teams/join` 호출
- **THEN** HTTP 400, `{ error: { code: "VALIDATION_ERROR", message: "형식이 올바르지 않습니다" } }` 반환

#### Scenario: 존재하지 않는 초대코드
- **WHEN** DB에 없는 초대코드로 `POST /teams/join` 호출
- **THEN** HTTP 404, `{ error: { code: "NOT_FOUND", message: "해당 초대코드를 찾을 수 없습니다" } }` 반환

#### Scenario: 이미 팀 소속인 사용자
- **WHEN** `team_id != null`인 사용자가 `POST /teams/join` 호출
- **THEN** HTTP 409, `{ error: { code: "ALREADY_IN_TEAM", message: "이미 다른 팀에 소속되어 있습니다" } }` 반환

---

### Requirement: 팀 정보 조회
시스템은 팀 멤버만 팀 정보를 조회할 수 있어야 한다.

#### Scenario: 정상 조회
- **WHEN** 해당 팀 멤버가 `GET /teams/{id}` 호출
- **THEN** HTTP 200, `{ id, name, invite_code, owner_id, member_count }` 반환

#### Scenario: 비멤버 접근
- **WHEN** 다른 팀 소속 또는 미가입 사용자가 `GET /teams/{id}` 호출
- **THEN** HTTP 403, `{ error: { code: "FORBIDDEN", message: "권한이 없습니다" } }` 반환

---

### Requirement: 팀 멤버 목록 조회
시스템은 팀 멤버 목록을 반환해야 한다. owner는 `role: "owner"`, 나머지는 `role: "member"`.

#### Scenario: 정상 조회
- **WHEN** 팀 멤버가 `GET /teams/{id}/members` 호출
- **THEN** HTTP 200, `[{ id, email, role, joined_at }]` 반환

---

### Requirement: 팀 탈퇴
시스템은 팀 멤버가 팀을 탈퇴할 수 있어야 한다. 탈퇴 시 `users.team_id = null`로 업데이트된다. owner는 탈퇴 불가(팀 삭제와 다름).

#### Scenario: 멤버 탈퇴
- **WHEN** owner가 아닌 멤버가 `DELETE /teams/{id}/leave` 호출
- **THEN** HTTP 200, `{}` 반환, `users.team_id = null` 업데이트

#### Scenario: owner 탈퇴 시도
- **WHEN** owner가 `DELETE /teams/{id}/leave` 호출
- **THEN** HTTP 409, `{ error: { code: "OWNER_CANNOT_LEAVE", message: "팀 소유자는 탈퇴할 수 없습니다" } }` 반환

---

### Requirement: 팀 미가입 사용자 접근 제한
`team_id = null`인 사용자는 `/teams/*`, `/tasks/*`, `/messages/*`에 접근할 수 없다.

#### Scenario: 미가입 사용자의 칸반 접근
- **WHEN** `team_id = null`인 사용자가 `/teams/{id}/tasks` 호출
- **THEN** HTTP 403, `{ error: { code: "FORBIDDEN", message: "팀에 소속되어야 합니다" } }` 반환
