## MODIFIED Requirements

### Requirement: 태스크 생성
시스템은 팀 멤버가 태스크를 생성할 때 담당자를 팀 멤버 중에서 선택하거나 미할당으로 설정할 수 있어야 한다. 기본값은 현재 사용자(@me)다.

#### Scenario: 담당자 선택 후 카드 생성
- **WHEN** 인라인 입력에서 제목 입력 + 담당자 선택 후 Enter
- **THEN** 선택한 `assignee_id`로 `POST /teams/{id}/tasks` 호출, 카드 생성

#### Scenario: 미할당으로 카드 생성
- **WHEN** 담당자 드롭다운에서 "미할당" 선택 후 Enter
- **THEN** `assignee_id: null`로 카드 생성, 카드에 ⚠미할당 뱃지 표시

#### Scenario: 기본값 @me
- **WHEN** 인라인 입력이 열릴 때
- **THEN** 담당자 드롭다운이 현재 사용자로 기본 선택됨

---

### Requirement: 태스크 상세 조회
시스템은 카드 상세 모달에서 담당자를 팀 멤버 중에서 변경할 수 있어야 한다.

#### Scenario: 담당자 변경 후 저장
- **WHEN** 카드 모달에서 담당자 드롭다운 변경 후 저장 클릭
- **THEN** 변경된 `assignee_id`로 `PUT /tasks/{id}` 호출, 카드 업데이트

#### Scenario: 담당자 미할당으로 변경
- **WHEN** 카드 모달에서 담당자를 "미할당"으로 변경 후 저장
- **THEN** `assignee_id: null`로 업데이트, 카드에 ⚠미할당 뱃지 표시
