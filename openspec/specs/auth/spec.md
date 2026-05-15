## ADDED Requirements

### Requirement: 회원가입
시스템은 이메일과 비밀번호로 새 계정을 생성해야 한다. 이메일은 UNIQUE, 비밀번호는 bcrypt 해시 저장. 성공 시 JWT를 즉시 발급한다.

#### Scenario: 정상 회원가입
- **WHEN** 유효한 이메일과 8자 이상 비밀번호로 `POST /auth/signup` 호출
- **THEN** HTTP 201, `{ token, user: { id, email, team_id: null } }` 반환

#### Scenario: 이메일 중복
- **WHEN** 이미 가입된 이메일로 `POST /auth/signup` 호출
- **THEN** HTTP 409, `{ error: { code: "EMAIL_TAKEN", message: "이미 가입된 이메일입니다" } }` 반환

#### Scenario: 이메일 형식 오류
- **WHEN** 유효하지 않은 이메일 형식으로 `POST /auth/signup` 호출
- **THEN** HTTP 400, `{ error: { code: "VALIDATION_ERROR", message: "올바른 형식이 아닙니다" } }` 반환

#### Scenario: 비밀번호 8자 미만
- **WHEN** 7자 이하 비밀번호로 `POST /auth/signup` 호출
- **THEN** HTTP 400, `{ error: { code: "VALIDATION_ERROR", message: "비밀번호는 8자 이상이어야 합니다" } }` 반환

---

### Requirement: 로그인
시스템은 이메일·비밀번호 검증 후 JWT(24h)를 발급해야 한다. 이메일 존재 여부를 응답에서 노출해서는 안 된다.

#### Scenario: 정상 로그인
- **WHEN** 올바른 이메일·비밀번호로 `POST /auth/login` 호출
- **THEN** HTTP 200, `{ token, user: { id, email, team_id } }` 반환

#### Scenario: 자격증명 오류
- **WHEN** 잘못된 이메일 또는 비밀번호로 `POST /auth/login` 호출
- **THEN** HTTP 401, `{ error: { code: "INVALID_CREDENTIALS", message: "이메일 또는 비밀번호가 일치하지 않습니다" } }` 반환 (이메일 존재 여부 노출 금지)

---

### Requirement: 로그아웃
시스템은 stateless 로그아웃을 지원해야 한다. JWT 블랙리스트 없이 200만 반환한다.

#### Scenario: 로그아웃 호출
- **WHEN** 유효한 JWT로 `POST /auth/logout` 호출
- **THEN** HTTP 200, `{}` 반환 (서버 상태 변경 없음)

---

### Requirement: 현재 사용자 조회
시스템은 JWT로 현재 로그인 사용자 정보를 반환해야 한다.

#### Scenario: 정상 조회
- **WHEN** 유효한 JWT로 `GET /auth/me` 호출
- **THEN** HTTP 200, `{ id, email, team_id }` 반환

#### Scenario: 만료된 JWT
- **WHEN** 만료된 JWT로 `GET /auth/me` 호출
- **THEN** HTTP 401, `{ error: { code: "TOKEN_EXPIRED", message: "인증이 만료되었습니다" } }` 반환

---

### Requirement: JWT 인증 미들웨어
모든 `/teams/*`, `/tasks/*`, `/messages/*` 엔드포인트는 유효한 JWT를 요구해야 한다.

#### Scenario: JWT 없이 보호된 엔드포인트 접근
- **WHEN** Authorization 헤더 없이 보호된 엔드포인트 호출
- **THEN** HTTP 401, `{ error: { code: "TOKEN_EXPIRED", message: "인증이 만료되었습니다" } }` 반환
