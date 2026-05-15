from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..auth_utils import err, get_current_user

router = APIRouter(tags=["messages"])


def _assert_member(user: models.User, team_id: int):
    if user.team_id != team_id:
        err("FORBIDDEN", "권한이 없습니다", 403)


def msg_out(m: models.Message):
    return {"id": m.id, "user_id": m.user_id, "user_email": m.user.email, "content": m.content, "created_at": m.created_at}


class MessageIn(BaseModel):
    content: str


@router.get("/teams/{team_id}/messages")
def list_messages(team_id: int, since: Optional[str] = None, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    _assert_member(current_user, team_id)
    q = db.query(models.Message).filter(models.Message.team_id == team_id)
    if since:
        try:
            since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
            q = q.filter(models.Message.created_at > since_dt)
        except ValueError:
            err("VALIDATION_ERROR", "since 형식이 올바르지 않습니다")
    else:
        q = q.order_by(models.Message.created_at.desc()).limit(50)
        messages = q.all()
        return [msg_out(m) for m in reversed(messages)]
    messages = q.order_by(models.Message.created_at.asc()).all()
    return [msg_out(m) for m in messages]


@router.post("/teams/{team_id}/messages", status_code=201)
def send_message(team_id: int, body: MessageIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    _assert_member(current_user, team_id)
    if not body.content or not body.content.strip():
        err("VALIDATION_ERROR", "메시지를 입력해주세요")
    if len(body.content) > 1000:
        err("TOO_LONG", "메시지는 1000자 이내로 입력하세요", 400, limit=1000, actual=len(body.content))
    msg = models.Message(team_id=team_id, user_id=current_user.id, content=body.content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg_out(msg)


@router.delete("/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not msg:
        err("NOT_FOUND", "해당 항목을 찾을 수 없습니다", 404)
    if msg.user_id != current_user.id:
        err("NOT_OWNER", "본인의 메시지만 삭제할 수 있습니다", 403)
    db.delete(msg)
    db.commit()
    return {}
