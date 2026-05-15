from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..auth_utils import err, get_current_user

router = APIRouter(tags=["tasks"])

VALID_STATUSES = {"TODO", "DOING", "DONE"}


def _assert_member(user: models.User, team_id: int):
    if user.team_id != team_id:
        err("FORBIDDEN", "권한이 없습니다", 403)


def task_out(task: models.Task):
    return {
        "id": task.id, "title": task.title, "status": task.status,
        "team_id": task.team_id, "creator_id": task.creator_id,
        "assignee_id": task.assignee_id, "created_at": task.created_at,
    }


class TaskCreateIn(BaseModel):
    title: str
    assignee_id: Optional[int] = None


class TaskUpdateIn(BaseModel):
    title: Optional[str] = None
    assignee_id: Optional[int] = None


class StatusUpdateIn(BaseModel):
    status: str


@router.get("/teams/{team_id}/tasks")
def list_tasks(team_id: int, filter: Optional[str] = None, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    _assert_member(current_user, team_id)
    q = db.query(models.Task).filter(models.Task.team_id == team_id)
    if filter == "me":
        q = q.filter(models.Task.assignee_id == current_user.id)
    elif filter == "unassigned":
        q = q.filter(models.Task.assignee_id.is_(None))
    tasks = q.order_by(models.Task.created_at.desc()).all()
    return [task_out(t) for t in tasks]


@router.post("/teams/{team_id}/tasks", status_code=201)
def create_task(team_id: int, body: TaskCreateIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    _assert_member(current_user, team_id)
    if not body.title or not body.title.strip():
        err("VALIDATION_ERROR", "제목을 입력해주세요")
    task = models.Task(team_id=team_id, title=body.title.strip(), status="TODO", creator_id=current_user.id, assignee_id=body.assignee_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task_out(task)


@router.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        err("NOT_FOUND", "해당 항목을 찾을 수 없습니다", 404)
    _assert_member(current_user, task.team_id)
    return task_out(task)


@router.put("/tasks/{task_id}")
def update_task(task_id: int, body: TaskUpdateIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        err("NOT_FOUND", "해당 항목을 찾을 수 없습니다", 404)
    _assert_member(current_user, task.team_id)
    if body.title is not None:
        task.title = body.title.strip()
    if body.assignee_id is not None:
        task.assignee_id = body.assignee_id
    db.commit()
    db.refresh(task)
    return task_out(task)


@router.patch("/tasks/{task_id}/status")
def update_status(task_id: int, body: StatusUpdateIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if body.status not in VALID_STATUSES:
        err("VALIDATION_ERROR", "올바른 상태값이 아닙니다")
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        err("NOT_FOUND", "해당 항목을 찾을 수 없습니다", 404)
    _assert_member(current_user, task.team_id)
    task.status = body.status
    db.commit()
    return {"id": task.id, "status": task.status}


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        err("NOT_FOUND", "해당 항목을 찾을 수 없습니다", 404)
    _assert_member(current_user, task.team_id)
    team = db.query(models.Team).filter(models.Team.id == task.team_id).first()
    is_creator = task.creator_id == current_user.id
    is_owner = team and team.owner_id == current_user.id
    if not is_creator and not is_owner:
        err("FORBIDDEN", "권한이 없습니다", 403)
    db.delete(task)
    db.commit()
    return {}
