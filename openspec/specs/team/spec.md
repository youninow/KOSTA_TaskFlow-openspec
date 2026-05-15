## MODIFIED Requirements

### Requirement: 팀 정보 조회
시스템은 팀 정보 조회 시 초대코드를 반환해야 하며, UI에서는 owner에게만 표시해야 한다.

#### Scenario: owner가 멤버 화면 진입
- **WHEN** owner 역할의 사용자가 멤버 화면에 접근
- **THEN** 팀 이름 아래에 초대코드가 표시되고 클립보드 복사 버튼이 제공됨

#### Scenario: member가 멤버 화면 진입
- **WHEN** member 역할의 사용자가 멤버 화면에 접근
- **THEN** 초대코드 섹션이 표시되지 않음

#### Scenario: 초대코드 복사
- **WHEN** owner가 복사 버튼 클릭
- **THEN** 초대코드가 클립보드에 복사되고 버튼이 "✓ 복사됨"으로 1.5초간 변경됨
