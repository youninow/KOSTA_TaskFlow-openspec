import re
import random
import string
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..auth_utils import err, get_current_user

router = APIRouter(tags=["teams"])

INVITE_CODE_RE = re.compile(r"^[A-Z]{4}-[0-9]{4}$")


def _gen_invite_code(db: Session) -> str:
    while True:
        code = "".join(random.choices(string.ascii_uppercase, k=4)) + "-" + "".join(random.choices(string.digits, k=4))
        if not db.query(models.Team).filter(models.Team.invite_code == code).first():
            return code


def _assert_member(user: models.User, team_id: int):
    if user.team_id != team_id:
        err("FORBIDDEN", "권한이 없습니다", 403)


class TeamCreateIn(BaseModel):
    name: str


class JoinIn(BaseModel):
    invite_code: str


@router.post("/teams", status_code=201)
def create_team(body: TeamCreateIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not 1 <= len(body.name) <= 30:
        err("VALIDATION_ERROR", "팀 이름은 1-30자여야 합니다")
    if current_user.team_id is not None:
        err("ALREADY_IN_TEAM", "이미 다른 팀에 소속되어 있습니다", 409)
    team = models.Team(name=body.name, invite_code=_gen_invite_code(db), owner_id=current_user.id)
    db.add(team)
    db.flush()
    current_user.team_id = team.id
    db.commit()
    db.refresh(team)
    return {"id": team.id, "name": team.name, "invite_code": team.invite_code, "owner_id": team.owner_id, "created_at": team.created_at}


@router.post("/teams/join")
def join_team(body: JoinIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not INVITE_CODE_RE.match(body.invite_code):
        err("VALIDATION_ERROR", "형식이 올바르지 않습니다")
    if current_user.team_id is not None:
        err("ALREADY_IN_TEAM", "이미 다른 팀에 소속되어 있습니다", 409)
    team = db.query(models.Team).filter(models.Team.invite_code == body.invite_code).first()
    if not team:
        err("NOT_FOUND", "해당 초대코드를 찾을 수 없습니다", 404)
    current_user.team_id = team.id
    db.commit()
    member_count = db.query(models.User).filter(models.User.team_id == team.id).count()
    return {"team": {"id": team.id, "name": team.name, "member_count": member_count}, "redirect": f"/teams/{team.id}"}


@router.get("/teams/{team_id}")
def get_team(team_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    _assert_member(current_user, team_id)
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        err("NOT_FOUND", "해당 항목을 찾을 수 없습니다", 404)
    member_count = db.query(models.User).filter(models.User.team_id == team_id).count()
    return {"id": team.id, "name": team.name, "invite_code": team.invite_code, "owner_id": team.owner_id, "member_count": member_count}


@router.get("/teams/{team_id}/members")
def get_members(team_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    _assert_member(current_user, team_id)
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        err("NOT_FOUND", "해당 항목을 찾을 수 없습니다", 404)
    members = db.query(models.User).filter(models.User.team_id == team_id).all()
    return [
        {"id": m.id, "email": m.email, "role": "owner" if m.id == team.owner_id else "member", "joined_at": m.created_at}
        for m in members
    ]


@router.delete("/teams/{team_id}/leave")
def leave_team(team_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    _assert_member(current_user, team_id)
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        err("NOT_FOUND", "해당 항목을 찾을 수 없습니다", 404)
    if team.owner_id == current_user.id:
        err("OWNER_CANNOT_LEAVE", "팀 소유자는 탈퇴할 수 없습니다", 409)
    current_user.team_id = None
    db.commit()
    return {}
